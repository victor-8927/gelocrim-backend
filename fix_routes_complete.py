import os, sys
sys.path.insert(0, r'C:\fleet-cloud')

content = '''from datetime import date
from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user
from app.config import DEPOT_LAT, DEPOT_LNG, VRP_TIME_LIMIT

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from vrp_solver import VRPSolver, Vehicle, Delivery, DepotLocation

import os, sys

router = APIRouter(prefix="/api/v1/routes", tags=["Rotas"])


class OptimizeRequest(BaseModel):
    route_date: date
    vehicle_ids: Optional[list[str]] = None
    order_ids: Optional[list[str]] = None
    time_limit_sec: int = 30
    reoptimize: bool = False


def _min(t) -> int:
    if not t:
        return 450  # 07:30
    s = str(t)[:5]
    try:
        h, m = map(int, s.split(":"))
        return h * 60 + m
    except:
        return 450


def _hhmm(minutes: int) -> str:
    minutes = minutes % 1440
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _in_clause(ids: list[str]) -> tuple[str, dict]:
    placeholders = ", ".join(f":p{i}" for i in range(len(ids)))
    params = {f"p{i}": v for i, v in enumerate(ids)}
    return f"({placeholders})", params


@router.get("")
def list_routes(
    date_: Optional[date] = Query(None, alias="date"),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """
        SELECT r.id AS route_id, v.plate AS vehicle_plate,
               d.name AS driver_name, r.status,
               r.total_stops, r.total_distance_km,
               r.planned_start, r.planned_end, r.route_date,
               COUNT(CASE WHEN s.status=\'completed\' THEN 1 END) AS stops_completed,
               COUNT(CASE WHEN s.status=\'failed\' THEN 1 END) AS stops_failed
        FROM routes r
        JOIN vehicles v ON v.id = r.vehicle_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        LEFT JOIN stops s ON s.route_id = r.id
    """
    params = {}
    if date_:
        q += " WHERE r.route_date = :d"
        params["d"] = str(date_)
    q += " GROUP BY r.id, v.plate, d.name ORDER BY r.created_at DESC"
    rows = db.execute(text(q), params).fetchall()
    return [dict(r._mapping) for r in rows]


@router.get("/{rid}/stops")
def get_route_stops(rid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    route = db.execute(text("SELECT id FROM routes WHERE id=:id"), {"id": rid}).fetchone()
    if not route:
        raise HTTPException(status_code=404, detail="Rota nao encontrada.")
    rows = db.execute(text("""
        SELECT s.id AS stop_id, s.sequence, s.eta, s.ata, s.atd, s.status, s.failure_reason,
               o.id AS order_id, o.external_id, r.name AS recipient_name,
               r.address, r.phone, o.weight_kg, o.volume_m3,
               s.lat, s.lng
        FROM stops s
        JOIN orders o ON o.id = s.order_id
        JOIN recipients r ON r.id = o.recipient_id
        WHERE s.route_id = :rid
        ORDER BY s.sequence
    """), {"rid": rid}).fetchall()
    return [dict(r._mapping) for r in rows]


@router.post("/optimize", status_code=202)
def optimize(
    body: OptimizeRequest,
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ts = now_str()

    # Veiculos
    if body.vehicle_ids:
        ph, ph_params = _in_clause(body.vehicle_ids)
        rows = db.execute(
            text(f"SELECT id,plate,capacity_kg,capacity_m3 FROM vehicles WHERE id IN {ph} AND status=\'active\'"),
            ph_params
        ).fetchall()
    else:
        rows = db.execute(
            text("SELECT id,plate,capacity_kg,capacity_m3 FROM vehicles WHERE status=\'active\'")
        ).fetchall()

    raw_v = [dict(r._mapping) for r in rows]
    if not raw_v:
        raise HTTPException(status_code=422, detail="Nenhum veiculo ativo.")

    # Pedidos
    if body.order_ids:
        ph, ph_params = _in_clause(body.order_ids)
        rows = db.execute(text(f"""
            SELECT o.id, o.lat, o.lng, o.weight_kg, o.volume_m3,
                   o.tw_start, o.tw_end,
                   r.address, r.name AS recipient_name
            FROM orders o JOIN recipients r ON r.id = o.recipient_id
            WHERE o.id IN {ph} AND o.status IN (\'pending\',\'queued\')
        """), ph_params).fetchall()
    else:
        rows = db.execute(text("""
            SELECT o.id, o.lat, o.lng, o.weight_kg, o.volume_m3,
                   o.tw_start, o.tw_end,
                   r.address, r.name AS recipient_name
            FROM orders o JOIN recipients r ON r.id = o.recipient_id
            WHERE o.status IN (\'pending\',\'queued\')
              AND o.nfe_status != \'rejected\'
              AND date(o.created_at) <= :d
        """), {"d": str(body.route_date)}).fetchall()

    raw_o = [dict(r._mapping) for r in rows]
    if not raw_o:
        raise HTTPException(status_code=422, detail="Nenhum pedido pendente.")

    if body.reoptimize:
        db.execute(text("""
            UPDATE routes SET status=\'cancelled\', updated_at=:ts
            WHERE route_date=:d AND status IN (\'draft\',\'optimized\')
        """), {"d": str(body.route_date), "ts": ts})
        db.commit()

    depot = DepotLocation(lat=DEPOT_LAT, lng=DEPOT_LNG)
    vehicles = [
        Vehicle(id=str(v["id"]), capacity_kg=float(v["capacity_kg"]), capacity_m3=float(v["capacity_m3"]))
        for v in raw_v
    ]
    deliveries = [
        Delivery(
            id=str(o["id"]), lat=float(o["lat"]), lng=float(o["lng"]),
            weight_kg=float(o["weight_kg"]), volume_m3=float(o["volume_m3"]),
            tw_start=_min(o["tw_start"]), tw_end=_min(o["tw_end"])
        )
        for o in raw_o
    ]

    solver = VRPSolver(time_limit_sec=body.time_limit_sec)
    result = solver.solve(vehicles, deliveries, depot)

    if result.status == "infeasible":
        raise HTTPException(status_code=422, detail="Solver nao encontrou solucao viavel.")

    vm = {str(v["id"]): v for v in raw_v}
    om = {str(o["id"]): o for o in raw_o}
    routes_out = []

    for r in result.routes:
        if not r.stops:
            continue
        rid = str(uuid4())
        ps = r.stops[0].arrival_min
        pe = r.stops[-1].departure_min
        v = vm[r.vehicle_id]

        db.execute(text("""
            INSERT INTO routes (id,vehicle_id,route_date,status,total_distance_km,
                total_stops,planned_start,planned_end,optimized_at,created_at,updated_at)
            VALUES (:id,:vid,:d,\'optimized\',:dist,:ns,:ps,:pe,:ts,:ts,:ts)
        """), {"id": rid, "vid": str(v["id"]), "d": str(body.route_date),
               "dist": r.total_distance_km, "ns": len(r.stops),
               "ps": _hhmm(ps), "pe": _hhmm(pe), "ts": ts})

        stops_out = []
        for stop in r.stops:
            sid = str(uuid4())
            o = om[stop.delivery_id]
            db.execute(text("""
                INSERT INTO stops (id,route_id,order_id,sequence,lat,lng,eta,status,created_at,updated_at)
                VALUES (:id,:rid,:oid,:seq,:lat,:lng,:eta,\'pending\',:ts,:ts)
            """), {"id": sid, "rid": rid, "oid": str(o["id"]), "seq": stop.sequence,
                   "lat": o["lat"], "lng": o["lng"], "eta": _hhmm(stop.arrival_min), "ts": ts})
            db.execute(
                text("UPDATE orders SET status=\'routed\', updated_at=:ts WHERE id=:id"),
                {"ts": ts, "id": str(o["id"])}
            )
            stops_out.append({
                "stop_id": sid, "order_id": str(o["id"]),
                "sequence": stop.sequence, "eta": _hhmm(stop.arrival_min),
                "address": o["address"], "recipient_name": o["recipient_name"],
                "weight_kg": o["weight_kg"]
            })

        score = getattr(r, "score", None)
        routes_out.append({
            "route_id": rid, "vehicle_plate": v["plate"],
            "total_distance_km": r.total_distance_km, "total_stops": len(r.stops),
            "planned_start": "07:30", "planned_end": _hhmm(pe),
            "score": score, "stops": stops_out
        })

    db.commit()
    return {
        "status": result.status,
        "route_date": str(body.route_date),
        "routes_created": len(routes_out),
        "total_stops": sum(len(r["stops"]) for r in routes_out),
        "unassigned_orders": result.unassigned,
        "wall_time_ms": result.wall_time_ms,
        "routes": routes_out,
    }


@router.patch("/{rid}")
def update_route(rid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"status", "driver_id", "actual_start", "actual_end"}
    updates = {k: v for k, v in body.items() if k in allowed}
    if updates:
        updates["updated_at"] = now_str()
        updates["id"] = rid
        sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
        db.execute(text(f"UPDATE routes SET {sets} WHERE id=:id"), updates)
        db.commit()
    return {"ok": True}


@router.patch("/stops/{sid}")
def update_stop(sid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"status", "failure_reason", "ata", "atd"}
    updates = {k: v for k, v in body.items() if k in allowed}
    if updates:
        updates["updated_at"] = now_str()
        updates["id"] = sid
        sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
        db.execute(text(f"UPDATE stops SET {sets} WHERE id=:id"), updates)
        if body.get("status") in ("completed", "failed"):
            row = db.execute(text("SELECT order_id FROM stops WHERE id=:id"), {"id": sid}).fetchone()
            if row:
                new_status = "delivered" if body["status"] == "completed" else "failed"
                db.execute(
                    text("UPDATE orders SET status=:st, updated_at=:ts WHERE id=:id"),
                    {"st": new_status, "ts": now_str(), "id": str(row.order_id)}
                )
        db.commit()
    return {"ok": True}
'''

path = r'C:\fleet-cloud\app\routers\routes.py'
# Adiciona imports necessarios no inicio
final = 'import os, sys\n' + content

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('routes.py reescrito com sucesso!')
