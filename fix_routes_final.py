content = '''from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1/routes", tags=["Rotas"])

# ── WebSocket Manager ─────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, route_id: str, ws: WebSocket):
        await ws.accept()
        if route_id not in self.active:
            self.active[route_id] = []
        self.active[route_id].append(ws)

    def disconnect(self, route_id: str, ws: WebSocket):
        if route_id in self.active:
            try: self.active[route_id].remove(ws)
            except: pass

    async def broadcast(self, route_id: str, data: dict):
        if route_id in self.active:
            dead = []
            for ws in self.active[route_id]:
                try: await ws.send_json(data)
                except: dead.append(ws)
            for d in dead:
                try: self.active[route_id].remove(d)
                except: pass

manager = ConnectionManager()
router_ws = APIRouter(tags=["WebSocket"])

@router_ws.websocket("/ws/routes/{route_id}")
async def websocket_rota(route_id: str, ws: WebSocket):
    await manager.connect(route_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(route_id, ws)

# ── Models ────────────────────────────────────────────────────
class RouteCreate(BaseModel):
    vehicle_id: str
    driver_id: str
    date: str
    planned_start: Optional[str] = "07:30"
    order_ids: List[str] = []
    km_inicial: Optional[int] = None

class StopUpdate(BaseModel):
    status: Optional[str] = None
    ata: Optional[str] = None
    atd: Optional[str] = None
    lat_confirmacao: Optional[float] = None
    lng_confirmacao: Optional[float] = None
    failure_reason: Optional[str] = None
    foto_base64: Optional[str] = None
    km_final: Optional[int] = None

def gerar_numero_viagem(db, data_str):
    data = data_str.replace("-","")[2:]
    count = db.execute(text(
        "SELECT COUNT(*) FROM routes WHERE route_date = :d"
    ), {"d": data_str}).scalar() or 0
    return f"VGM-{data}-{str(count+1).zfill(3)}"

# ── Endpoints ─────────────────────────────────────────────────
@router.get("")
def list_routes(date: Optional[str] = None, status: Optional[str] = None,
                db: Session = Depends(get_db)):
    where, params = [], {}
    if date:   where.append("r.route_date = :date");   params["date"] = date
    if status: where.append("r.status = :status");     params["status"] = status
    w = ("WHERE " + " AND ".join(where)) if where else ""
    rows = db.execute(text(f"""
        SELECT r.id as route_id, r.trip_number, r.route_date as date,
               r.status, r.planned_start, r.planned_end, r.total_distance_km,
               v.plate as vehicle_plate, v.vda,
               d.name as driver_name, d.phone as driver_phone,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.id) as total_stops,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.id
                AND s.status = "completed") as delivered_stops
        FROM routes r
        LEFT JOIN vehicles v ON v.id = r.vehicle_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        {w}
        ORDER BY r.created_at DESC
    """), params).mappings().all()
    return [dict(r) for r in rows]

@router.post("")
def create_route(body: RouteCreate, db: Session = Depends(get_db)):
    route_id    = str(uuid.uuid4())
    trip_number = gerar_numero_viagem(db, body.date)
    db.execute(text("""
        INSERT INTO routes (id, trip_number, vehicle_id, driver_id,
            route_date, planned_start, status)
        VALUES (:id, :trip, :vid, :did, :date, :ps, "optimized")
    """), {"id":route_id,"trip":trip_number,"vid":body.vehicle_id,
           "did":body.driver_id,"date":body.date,"ps":body.planned_start})

    orders = []
    for oid in body.order_ids:
        o = db.execute(text("SELECT * FROM orders WHERE id = :id"),{"id":oid}).mappings().fetchone()
        if o: orders.append(dict(o))

    clientes = {}
    for o in orders:
        key = o.get("codparc") or o.get("recipient_name") or o["id"]
        if key not in clientes:
            clientes[key] = {"codparc":o.get("codparc"),"recipient_name":o.get("recipient_name",""),
                "address":o.get("address",""),"lat":o.get("lat"),"lng":o.get("lng"),
                "weight_kg":0,"order_ids":[]}
        clientes[key]["weight_kg"] += float(o.get("weight_kg") or 0)
        clientes[key]["order_ids"].append(o["id"])

    for i, (key, cli) in enumerate(clientes.items()):
        stop_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO route_stops
                (stop_id,route_id,order_id,sequence,recipient_name,address,
                 lat,lng,weight_kg,status,codparc)
            VALUES (:sid,:rid,:oid,:seq,:name,:addr,:lat,:lng,:kg,"pending",:cp)
        """), {"sid":stop_id,"rid":route_id,"oid":cli["order_ids"][0],"seq":i,
               "name":cli["recipient_name"],"addr":cli["address"],
               "lat":cli["lat"],"lng":cli["lng"],"kg":cli["weight_kg"],"cp":cli["codparc"]})
        for oid in cli["order_ids"]:
            db.execute(text("UPDATE orders SET status='routed' WHERE id=:id"),{"id":oid})

    db.commit()
    return {"route_id":route_id,"trip_number":trip_number,"status":"optimized","total_stops":len(clientes)}

@router.get("/{route_id}/stops")
def get_stops(route_id: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT stop_id, route_id, sequence, recipient_name, address,
               lat, lng, weight_kg, status, eta, ata, atd,
               failure_reason, codparc, foto_url
        FROM route_stops WHERE route_id = :rid ORDER BY sequence
    """), {"rid":route_id}).mappings().all()
    return [dict(r) for r in rows]

@router.get("/{route_id}/stops/{stop_id}/notas")
def get_notas_stop(route_id: str, stop_id: str, db: Session = Depends(get_db)):
    stop = db.execute(text(
        "SELECT codparc FROM route_stops WHERE stop_id = :id"
    ), {"id":stop_id}).mappings().fetchone()
    if not stop:
        raise HTTPException(404, "Stop não encontrado")

    orders = db.execute(text("""
        SELECT o.id, o.external_id, o.weight_kg, o.status,
               oi.item_tipo, oi.item_nome, oi.qtd, oi.peso_unit, oi.top_app
        FROM orders o
        LEFT JOIN order_items oi ON oi.codparc = o.codparc
        WHERE o.codparc = :cp
        AND o.status IN ("routed","pending","delivered")
        ORDER BY o.external_id, oi.item_tipo
    """), {"cp":stop["codparc"]}).mappings().all()

    notas = {}
    for r in orders:
        oid = r["external_id"] or r["id"]
        if oid not in notas:
            notas[oid] = {"external_id":oid,"top_app":r["top_app"] or "1000",
                "weight_kg":float(r["weight_kg"] or 0),"status":r["status"],"itens":[]}
        if r["item_nome"]:
            notas[oid]["itens"].append({
                "nome":r["item_nome"],"qtd":r["qtd"],"peso_unit":r["peso_unit"]
            })
    return list(notas.values())

@router.post("/{route_id}/liberar")
def liberar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text("UPDATE routes SET status='released' WHERE id=:id"),{"id":route_id})
    db.commit()
    return {"status":"released"}

@router.post("/{route_id}/iniciar")
def iniciar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='executing', started_at=:now WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat()})
    db.commit()
    return {"status":"executing"}

@router.post("/{route_id}/finalizar")
def finalizar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='done', finished_at=:now WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat()})
    db.commit()
    return {"status":"done"}

@router.delete("/{route_id}")
def delete_route(route_id: str, db: Session = Depends(get_db)):
    route = db.execute(text("SELECT status FROM routes WHERE id=:id"),{"id":route_id}).fetchone()
    if not route: raise HTTPException(404,"Rota não encontrada")
    if route[0] in ("executing","done"): raise HTTPException(400,"Não pode excluir rota ativa")
    stops = db.execute(text("SELECT order_id FROM route_stops WHERE route_id=:id"),{"id":route_id}).fetchall()
    for s in stops:
        if s[0]: db.execute(text("UPDATE orders SET status='pending' WHERE id=:id"),{"id":s[0]})
    db.execute(text("DELETE FROM route_stops WHERE route_id=:id"),{"id":route_id})
    db.execute(text("DELETE FROM routes WHERE id=:id"),{"id":route_id})
    db.commit()
    return {"deleted":True}

@router.patch("/{route_id}/stops/{stop_id}")
async def update_stop(route_id: str, stop_id: str, body: StopUpdate,
                      db: Session = Depends(get_db)):
    fields, params = [], {"stop_id":stop_id,"route_id":route_id}
    if body.status:          fields.append("status=:status");          params["status"]=body.status
    if body.ata:             fields.append("ata=:ata");                 params["ata"]=body.ata
    if body.atd:             fields.append("atd=:atd");                 params["atd"]=body.atd
    if body.lat_confirmacao: fields.append("lat_confirmacao=:lat_c");  params["lat_c"]=body.lat_confirmacao
    if body.lng_confirmacao: fields.append("lng_confirmacao=:lng_c");  params["lng_c"]=body.lng_confirmacao
    if body.failure_reason:  fields.append("failure_reason=:fr");      params["fr"]=body.failure_reason

    if body.foto_base64:
        try:
            import base64 as b64, os
            header, data = body.foto_base64.split(",",1)
            img = b64.b64decode(data)
            pasta = r"C:\\fleet-cloud\\fotos"
            os.makedirs(pasta, exist_ok=True)
            nome = f"{stop_id}.jpg"
            with open(os.path.join(pasta, nome),"wb") as f: f.write(img)
            fields.append("foto_url=:foto_url")
            params["foto_url"] = f"/fotos/{nome}"
        except: pass

    if not fields: raise HTTPException(400,"Nenhum campo")
    db.execute(text(f"UPDATE route_stops SET {', '.join(fields)} WHERE stop_id=:stop_id AND route_id=:route_id"), params)

    if body.status in ("completed","failed"):
        stop = db.execute(text("SELECT order_id FROM route_stops WHERE stop_id=:id"),{"id":stop_id}).fetchone()
        if stop and stop[0]:
            novo = "delivered" if body.status=="completed" else "failed"
            db.execute(text("UPDATE orders SET status=:s WHERE id=:id"),{"s":novo,"id":stop[0]})

    db.commit()

    # Broadcast WebSocket
    try:
        await manager.broadcast(route_id, {
            "type": "stop_update",
            "stop_id": stop_id,
            "status": body.status
        })
    except: pass

    return {"updated":True}
'''

with open(r'C:\fleet-cloud\app\routers\routes.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\routes.py', doraise=True)
    print('routes.py VÁLIDO!')
except Exception as e:
    print(f'ERRO: {e}')
