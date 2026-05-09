# Reescreve o router de rotas com todos os endpoints que o app precisa
content = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
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
    """Gera numero sequencial: VGM-YYMMDD-NNN"""
    data = data_str.replace("-","")[2:]  # 250425
    count = db.execute(text(
        "SELECT COUNT(*) FROM routes WHERE date = :d"
    ), {"d": data_str}).scalar() or 0
    return f"VGM-{data}-{str(count+1).zfill(3)}"

@router.get("")
def list_routes(date: Optional[str] = None, status: Optional[str] = None,
                db: Session = Depends(get_db)):
    where = []
    params = {}
    if date:
        where.append("r.date = :date")
        params["date"] = date
    if status:
        where.append("r.status = :status")
        params["status"] = status
    w = ("WHERE " + " AND ".join(where)) if where else ""
    rows = db.execute(text(f"""
        SELECT r.route_id, r.trip_number, r.date, r.status,
               r.planned_start, r.planned_end, r.total_distance_km,
               v.plate as vehicle_plate, v.vda,
               d.name as driver_name, d.phone as driver_phone,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.route_id) as total_stops,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.route_id AND s.status = 'completed') as delivered_stops
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
        INSERT INTO routes (route_id, trip_number, vehicle_id, driver_id, date, planned_start, status)
        VALUES (:route_id, :trip_number, :vehicle_id, :driver_id, :date, :planned_start, 'optimized')
    """), {
        "route_id": route_id,
        "trip_number": trip_number,
        "vehicle_id": body.vehicle_id,
        "driver_id": body.driver_id,
        "date": body.date,
        "planned_start": body.planned_start,
    })

    # Cria stops a partir dos orders
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
                 :lat, :lng, :kg, 'pending', :codparc)
        """), {
            "stop_id": stop_id,
            "route_id": route_id,
            "order_id": order_id,
            "seq": i,
            "name": order.get("recipient_name",""),
            "addr": order.get("address",""),
            "lat": order.get("lat"),
            "lng": order.get("lng"),
            "kg": order.get("weight_kg", 0),
            "codparc": order.get("codparc"),
        })
        # Atualiza status do pedido para routed
        db.execute(text(
            "UPDATE orders SET status = 'routed' WHERE id = :id"
        ), {"id": order_id})

    db.commit()
    return {"route_id": route_id, "trip_number": trip_number, "status": "optimized"}

@router.get("/{route_id}/stops")
def get_stops(route_id: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT s.stop_id, s.route_id, s.sequence, s.recipient_name, s.address,
               s.lat, s.lng, s.weight_kg, s.status, s.eta,
               s.ata, s.atd, s.failure_reason, s.codparc
        FROM route_stops s
        WHERE s.route_id = :rid
        ORDER BY s.sequence
    """), {"rid": route_id}).mappings().all()
    return [dict(r) for r in rows]

@router.post("/{route_id}/liberar")
def liberar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status = 'released' WHERE route_id = :id"
    ), {"id": route_id})
    db.commit()
    return {"status": "released"}

@router.post("/{route_id}/iniciar")
def iniciar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status = 'executing', started_at = :now WHERE route_id = :id"
    ), {"id": route_id, "now": datetime.now().isoformat()})
    db.commit()
    return {"status": "executing"}

@router.post("/{route_id}/finalizar")
def finalizar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status = 'done', finished_at = :now WHERE route_id = :id"
    ), {"id": route_id, "now": datetime.now().isoformat()})
    db.commit()
    return {"status": "done"}

@router.patch("/{route_id}/stops/{stop_id}")
def update_stop(route_id: str, stop_id: str, body: StopUpdate,
                db: Session = Depends(get_db)):
    fields = []
    params = {"stop_id": stop_id, "route_id": route_id}
    if body.status:
        fields.append("status = :status")
        params["status"] = body.status
    if body.ata:
        fields.append("ata = :ata")
        params["ata"] = body.ata
    if body.atd:
        fields.append("atd = :atd")
        params["atd"] = body.atd
    if body.lat_confirmacao:
        fields.append("lat_confirmacao = :lat_confirmacao")
        params["lat_confirmacao"] = body.lat_confirmacao
    if body.lng_confirmacao:
        fields.append("lng_confirmacao = :lng_confirmacao")
        params["lng_confirmacao"] = body.lng_confirmacao
    if body.failure_reason:
        fields.append("failure_reason = :failure_reason")
        params["failure_reason"] = body.failure_reason
    if not fields:
        raise HTTPException(400, "Nenhum campo para atualizar")
    db.execute(text(f"""
        UPDATE route_stops SET {", ".join(fields)}
        WHERE stop_id = :stop_id AND route_id = :route_id
    """), params)
    # Se confirmado, atualiza order para delivered
    if body.status == "completed":
        stop = db.execute(text(
            "SELECT order_id FROM route_stops WHERE stop_id = :id"
        ), {"id": stop_id}).fetchone()
        if stop and stop[0]:
            db.execute(text(
                "UPDATE orders SET status = 'delivered' WHERE id = :id"
            ), {"id": stop[0]})
    elif body.status == "failed":
        stop = db.execute(text(
            "SELECT order_id FROM route_stops WHERE stop_id = :id"
        ), {"id": stop_id}).fetchone()
        if stop and stop[0]:
            db.execute(text(
                "UPDATE orders SET status = 'failed' WHERE id = :id"
            ), {"id": stop[0]})
    db.commit()
    return {"updated": True}
'''

with open(r'C:\fleet-cloud\app\routers\routes.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('routes.py reescrito!')

# Agora verifica se as colunas existem na tabela routes
import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cols = [r[1] for r in conn.execute("PRAGMA table_info(routes)").fetchall()]
print(f'Colunas routes: {cols}')

needed = ['trip_number','started_at','finished_at']
for col in needed:
    if col not in cols:
        tipo = 'TEXT'
        conn.execute(f"ALTER TABLE routes ADD COLUMN {col} {tipo}")
        print(f'  + Coluna {col} adicionada!')

# Verifica route_stops
cols2 = [r[1] for r in conn.execute("PRAGMA table_info(route_stops)").fetchall()]
print(f'Colunas route_stops: {cols2}')

needed2 = ['eta','ata','atd','failure_reason','lat_confirmacao','lng_confirmacao','codparc']
for col in needed2:
    if col not in cols2:
        tipo = 'REAL' if 'lat' in col or 'lng' in col else 'TEXT'
        conn.execute(f"ALTER TABLE route_stops ADD COLUMN {col} {tipo}")
        print(f'  + Coluna {col} adicionada!')

conn.commit()
conn.close()
print('Banco atualizado! Reinicie o servidor.')
