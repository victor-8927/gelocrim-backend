content = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/routes", tags=["Rotas"])

class RouteCreate(BaseModel):
    vehicle_id: str
    driver_id: str
    date: str
    planned_start: Optional[str] = "07:30"
    order_ids: List[str] = []

class StopUpdate(BaseModel):
    status: Optional[str] = None
    ata: Optional[str] = None
    atd: Optional[str] = None
    lat_confirmacao: Optional[float] = None
    lng_confirmacao: Optional[float] = None
    failure_reason: Optional[str] = None

def gerar_numero_viagem(db, data_str):
    data = data_str.replace("-","")[2:]
    count = db.execute(text(
        "SELECT COUNT(*) FROM routes WHERE route_date = :d"
    ), {"d": data_str}).scalar() or 0
    return f"VGM-{data}-{str(count+1).zfill(3)}"

@router.get("")
def list_routes(date: Optional[str] = None, status: Optional[str] = None,
                db: Session = Depends(get_db)):
    where = []
    params = {}
    if date:
        where.append("r.route_date = :date")
        params["date"] = date
    if status:
        where.append("r.status = :status")
        params["status"] = status
    w = ("WHERE " + " AND ".join(where)) if where else ""
    rows = db.execute(text(f"""
        SELECT r.id as route_id, r.trip_number, r.route_date as date,
               r.status, r.planned_start, r.planned_end, r.total_distance_km,
               v.plate as vehicle_plate, v.vda,
               d.name as driver_name, d.phone as driver_phone,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.id) as total_stops,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.id AND s.status = "completed") as delivered_stops
        FROM routes r
        LEFT JOIN vehicles v ON v.id = r.vehicle_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        {w}
        ORDER BY r.created_at DESC
    """), params).mappings().all()
    return [dict(r) for r in rows]

@router.post("")
def create_route(body: RouteCreate, db: Session = Depends(get_db)):
    route_id = str(uuid.uuid4())
    trip_number = gerar_numero_viagem(db, body.date)

    db.execute(text("""
        INSERT INTO routes (id, trip_number, vehicle_id, driver_id, route_date, planned_start, status)
        VALUES (:id, :trip_number, :vehicle_id, :driver_id, :date, :planned_start, "optimized")
    """), {
        "id": route_id,
        "trip_number": trip_number,
        "vehicle_id": body.vehicle_id,
        "driver_id": body.driver_id,
        "date": body.date,
        "planned_start": body.planned_start,
    })

    for i, order_id in enumerate(body.order_ids):
        order = db.execute(text(
            "SELECT * FROM orders WHERE id = :id"
        ), {"id": order_id}).mappings().fetchone()
        if not order:
            continue
        stop_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO route_stops
                (stop_id, route_id, order_id, sequence, recipient_name, address,
                 lat, lng, weight_kg, status, codparc)
            VALUES
                (:stop_id, :route_id, :order_id, :seq, :name, :addr,
                 :lat, :lng, :kg, "pending", :codparc)
        """), {
            "stop_id": stop_id, "route_id": route_id, "order_id": order_id,
            "seq": i, "name": order.get("recipient_name",""),
            "addr": order.get("address",""), "lat": order.get("lat"),
            "lng": order.get("lng"), "kg": order.get("weight_kg", 0),
            "codparc": order.get("codparc"),
        })
        db.execute(text("UPDATE orders SET status = 'routed' WHERE id = :id"), {"id": order_id})

    db.commit()
    return {"route_id": route_id, "trip_number": trip_number, "status": "optimized"}

@router.get("/{route_id}/stops")
def get_stops(route_id: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT stop_id, route_id, sequence, recipient_name, address,
               lat, lng, weight_kg, status, eta, ata, atd, failure_reason, codparc
        FROM route_stops
        WHERE route_id = :rid
        ORDER BY sequence
    """), {"rid": route_id}).mappings().all()
    return [dict(r) for r in rows]

@router.post("/{route_id}/liberar")
def liberar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text("UPDATE routes SET status = 'released' WHERE id = :id"), {"id": route_id})
    db.commit()
    return {"status": "released"}

@router.post("/{route_id}/iniciar")
def iniciar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status = 'executing', started_at = :now WHERE id = :id"
    ), {"id": route_id, "now": datetime.now().isoformat()})
    db.commit()
    return {"status": "executing"}

@router.post("/{route_id}/finalizar")
def finalizar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status = 'done', finished_at = :now WHERE id = :id"
    ), {"id": route_id, "now": datetime.now().isoformat()})
    db.commit()
    return {"status": "done"}

@router.patch("/{route_id}/stops/{stop_id}")
def update_stop(route_id: str, stop_id: str, body: StopUpdate,
                db: Session = Depends(get_db)):
    fields = []
    params = {"stop_id": stop_id, "route_id": route_id}
    if body.status:       fields.append("status = :status");             params["status"] = body.status
    if body.ata:          fields.append("ata = :ata");                   params["ata"] = body.ata
    if body.atd:          fields.append("atd = :atd");                   params["atd"] = body.atd
    if body.lat_confirmacao: fields.append("lat_confirmacao = :lat_c"); params["lat_c"] = body.lat_confirmacao
    if body.lng_confirmacao: fields.append("lng_confirmacao = :lng_c"); params["lng_c"] = body.lng_confirmacao
    if body.failure_reason:  fields.append("failure_reason = :fr");     params["fr"] = body.failure_reason
    if not fields:
        raise HTTPException(400, "Nenhum campo")
    db.execute(text(f"""
        UPDATE route_stops SET {", ".join(fields)}
        WHERE stop_id = :stop_id AND route_id = :route_id
    """), params)
    if body.status in ("completed", "failed"):
        stop = db.execute(text(
            "SELECT order_id FROM route_stops WHERE stop_id = :id"
        ), {"id": stop_id}).fetchone()
        if stop and stop[0]:
            novo = "delivered" if body.status == "completed" else "failed"
            db.execute(text("UPDATE orders SET status = :s WHERE id = :id"),
                       {"s": novo, "id": stop[0]})
    db.commit()
    return {"updated": True}
'''

with open(r'C:\fleet-cloud\app\routers\routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('routes.py corrigido com id como PK!')
print('Reinicie o servidor.')
