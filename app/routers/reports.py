from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/reports", tags=["Relatórios"])


def _pct(a, b):
    return round(a / b * 100, 1) if b else 0.0


@router.get("/dashboard")
def dashboard(_=Depends(get_current_user), db: Session = Depends(get_db)):
    """Resumo rápido do dia atual para o painel operacional."""
    today = str(date.today())

    totals = db.execute(text("""
        SELECT
            COUNT(CASE WHEN status='pending' THEN 1 END) AS orders_pending,
            COUNT(CASE WHEN status='routed'  THEN 1 END) AS orders_routed,
            COUNT(CASE WHEN status='delivered' THEN 1 END) AS orders_delivered,
            COUNT(CASE WHEN status='failed'  THEN 1 END) AS orders_failed
        FROM orders
        WHERE date(created_at) = :today
    """), {"today": today}).fetchone()

    routes_today = db.execute(text("""
        SELECT COUNT(*) AS count,
               COALESCE(SUM(total_distance_km), 0) AS total_km,
               COALESCE(SUM(total_stops), 0) AS total_stops
        FROM routes
        WHERE route_date = :today AND status NOT IN ('cancelled','draft')
    """), {"today": today}).fetchone()

    vehicles_active = db.execute(
        text("SELECT COUNT(*) AS count FROM vehicles WHERE status='active'")
    ).fetchone()

    drivers_active = db.execute(
        text("SELECT COUNT(*) AS count FROM drivers WHERE status='active'")
    ).fetchone()

    t = dict(totals._mapping)
    r = dict(routes_today._mapping)
    return {
        "date": today,
        "orders": {
            "pending": int(t["orders_pending"]),
            "routed": int(t["orders_routed"]),
            "delivered": int(t["orders_delivered"]),
            "failed": int(t["orders_failed"]),
        },
        "routes_today": {
            "count": int(r["count"]),
            "total_km": round(float(r["total_km"]), 1),
            "total_stops": int(r["total_stops"]),
        },
        "fleet": {
            "vehicles_active": int(dict(vehicles_active._mapping)["count"]),
            "drivers_active": int(dict(drivers_active._mapping)["count"]),
        },
    }


@router.get("/summary")
def summary(
    start: date = Query(default_factory=date.today),
    end:   date = Query(default_factory=date.today),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.execute(text("""
        SELECT COUNT(DISTINCT r.id) AS total_routes,
               COALESCE(SUM(r.total_stops), 0) AS total_stops_planned,
               COUNT(CASE WHEN s.status='completed' THEN 1 END) AS total_stops_completed,
               COUNT(CASE WHEN s.status='failed'    THEN 1 END) AS total_stops_failed,
               COALESCE(SUM(r.total_distance_km), 0) AS total_distance_km,
               COALESCE(AVG(r.total_distance_km), 0) AS avg_distance_km,
               COALESCE(AVG(r.total_stops), 0)       AS avg_stops_per_route
        FROM routes r
        LEFT JOIN stops s ON s.route_id = r.id
        WHERE r.route_date BETWEEN :s AND :e
          AND r.status NOT IN ('cancelled','draft')
    """), {"s": str(start), "e": str(end)}).fetchone()

    agg = dict(row._mapping)

    orow = db.execute(text("""
        SELECT
            COUNT(CASE WHEN status='routed'  THEN 1 END) AS routed,
            COUNT(CASE WHEN status='pending' THEN 1 END) AS pending
        FROM orders
        WHERE date(created_at) BETWEEN :s AND :e
    """), {"s": str(start), "e": str(end)}).fetchone()

    orders = dict(orow._mapping)
    comp = int(agg["total_stops_completed"])
    plan = int(agg["total_stops_planned"]) or (comp + int(agg["total_stops_failed"]))

    return {
        "period_start": str(start),
        "period_end": str(end),
        "total_routes": int(agg["total_routes"]),
        "total_stops_planned": plan,
        "total_stops_completed": comp,
        "total_stops_failed": int(agg["total_stops_failed"]),
        "delivery_rate_pct": _pct(comp, plan),
        "total_distance_km": round(float(agg["total_distance_km"]), 1),
        "avg_distance_km": round(float(agg["avg_distance_km"]), 1),
        "avg_stops_per_route": round(float(agg["avg_stops_per_route"]), 1),
        "total_orders_routed": int(orders["routed"]),
        "total_orders_pending": int(orders["pending"]),
    }


@router.get("/vehicles")
def vehicles_perf(
    start: date = Query(default_factory=date.today),
    end:   date = Query(default_factory=date.today),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = db.execute(text("""
        SELECT v.id AS vehicle_id, v.plate,
               COUNT(DISTINCT r.id) AS routes_count,
               COUNT(CASE WHEN s.status='completed' THEN 1 END) AS stops_completed,
               COUNT(CASE WHEN s.status='failed'    THEN 1 END) AS stops_failed,
               COALESCE(SUM(r.total_distance_km), 0) AS total_distance_km
        FROM vehicles v
        JOIN routes r ON r.vehicle_id = v.id
        LEFT JOIN stops s ON s.route_id = r.id
        WHERE r.route_date BETWEEN :s AND :e
          AND r.status NOT IN ('cancelled','draft')
        GROUP BY v.id, v.plate
        ORDER BY stops_completed DESC
    """), {"s": str(start), "e": str(end)}).fetchall()

    result = []
    for r in rows:
        d = dict(r._mapping)
        total = int(d["stops_completed"]) + int(d["stops_failed"])
        result.append({
            **d,
            "delivery_rate_pct": _pct(int(d["stops_completed"]), total),
            "total_distance_km": round(float(d["total_distance_km"]), 1),
        })
    return result


@router.get("/orders/failures")
def failures(
    start: date = Query(default_factory=date.today),
    end:   date = Query(default_factory=date.today),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = db.execute(text("""
        SELECT COALESCE(s.failure_reason, 'não informado') AS failure_reason,
               COUNT(*) AS count
        FROM stops s
        JOIN routes r ON r.id = s.route_id
        WHERE s.status = 'failed'
          AND r.route_date BETWEEN :s AND :e
        GROUP BY failure_reason
        ORDER BY count DESC
    """), {"s": str(start), "e": str(end)}).fetchall()

    data = [dict(r._mapping) for r in rows]
    total = sum(d["count"] for d in data)
    return [
        {
            "failure_reason": d["failure_reason"],
            "count": int(d["count"]),
            "pct_of_failures": _pct(int(d["count"]), total),
        }
        for d in data
    ]
