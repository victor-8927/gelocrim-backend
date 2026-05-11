from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers.auth import get_current_user
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
    foto_nf_base64: Optional[str] = None
    foto_boleto_base64: Optional[str] = None
    foto_comodato_base64: Optional[str] = None
    foto_outros_base64: Optional[str] = None
    km_final: Optional[int] = None

def haversine(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

def gerar_numero_viagem(db, data_str):
    data = data_str.replace("-","")[2:]
    row = db.execute(text(
        "SELECT trip_number FROM routes WHERE route_date = :d ORDER BY trip_number DESC LIMIT 1"
    ), {"d": data_str}).fetchone()
    if row and row[0]:
        try: last = int(row[0].split("-")[-1])
        except: last = 0
    else:
        last = 0
    return f"VGM-{data}-{str(last+1).zfill(3)}"

# ── Endpoints ─────────────────────────────────────────────────
@router.get("")
def list_routes(date: Optional[str] = None, status: Optional[str] = None,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user)):
    where, params = [], {}
    if date:   where.append("r.route_date = :date");   params["date"] = date
    if status: where.append("r.status = :status");     params["status"] = status
    if current_user.get("role") == "driver":
        cpf = current_user.get("id")
        where.append("REPLACE(REPLACE(REPLACE(d.cpf,'.',''),'-',''),'/','') = :cpf")
        params["cpf"] = cpf
    w = ("WHERE " + " AND ".join(where)) if where else ""
    rows = db.execute(text(f"""
        SELECT r.id as route_id, r.trip_number, r.route_date as date,
               r.status, r.planned_start, r.planned_end, r.total_distance_km, r.km_inicial, r.km_final,
               v.plate as vehicle_plate, v.vda,
               d.name as driver_name, d.phone as driver_phone,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.id) as total_stops,
               (SELECT COUNT(*) FROM route_stops s WHERE s.route_id = r.id
                AND s.status = 'completed') as delivered_stops
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
        VALUES (:id, :trip, :vid, :did, :date, :ps, 'optimized')
    """), {"id":route_id,"trip":trip_number,"vid":body.vehicle_id,
           "did":body.driver_id,"date":body.date,"ps":body.planned_start})

    orders = []
    for oid in body.order_ids:
        o = db.execute(text("SELECT * FROM orders WHERE id = :id"),{"id":oid}).mappings().fetchone()
        if o: orders.append(dict(o))

    # CORRIGIDO: agrupar por CODPARC somando peso de todos os pedidos do mesmo cliente
    clientes = {}
    for o in orders:
        codparc = o.get("codparc")
        nome    = o.get("recipient_name") or ""
        addr    = o.get("address") or ""
        lat     = o.get("lat")
        lng     = o.get("lng")

        # Chave primaria: CODPARC. Fallback: nome. Fallback final: id unico
        key = codparc if codparc else (nome.strip() if nome.strip() else o["id"])

        if key not in clientes:
            clientes[key] = {
                "codparc": codparc,
                "recipient_name": nome,
                "address": addr,
                "lat": lat,
                "lng": lng,
                "weight_kg": 0,
                "order_ids": []
            }
        else:
            # Preencher campos vazios com dados de outros pedidos do mesmo cliente
            if not clientes[key]["recipient_name"] and nome:
                clientes[key]["recipient_name"] = nome
            if not clientes[key]["address"] and addr:
                clientes[key]["address"] = addr
            if not clientes[key]["lat"] and lat:
                clientes[key]["lat"] = lat
            if not clientes[key]["lng"] and lng:
                clientes[key]["lng"] = lng

        clientes[key]["weight_kg"] += float(o.get("weight_kg") or 0)
        clientes[key]["order_ids"].append(o["id"])

    # Filtrar entradas sem nome e sem codparc (pedidos com dados incompletos)
    clientes_validos = {
        k: v for k, v in clientes.items()
        if v["recipient_name"] or v["codparc"]
    }

    for i, (key, cli) in enumerate(clientes_validos.items()):
        stop_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO route_stops
                (stop_id,route_id,order_id,sequence,recipient_name,address,
                 lat,lng,weight_kg,status,codparc)
            VALUES (:sid,:rid,:oid,:seq,:name,:addr,:lat,:lng,:kg,'pending',:cp)
        """), {"sid":stop_id,"rid":route_id,"oid":cli["order_ids"][0],"seq":i,
               "name":cli["recipient_name"],"addr":cli["address"],
               "lat":cli["lat"],"lng":cli["lng"],"kg":cli["weight_kg"],"cp":cli["codparc"]})
        for oid in cli["order_ids"]:
            db.execute(text("UPDATE orders SET status='routed' WHERE id=:id"),{"id":oid})

    db.commit()
    return {"route_id":route_id,"trip_number":trip_number,"status":'optimized',"total_stops":len(clientes_validos)}

@router.get("/{route_id}/stops")
def get_stops(route_id: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT rs.stop_id, rs.route_id, rs.sequence, rs.recipient_name, rs.address,
               rs.lat, rs.lng, rs.weight_kg, rs.status, rs.eta, rs.ata, rs.atd,
               rs.failure_reason, rs.codparc, rs.foto_url,
               c.segmento
        FROM route_stops rs
        LEFT JOIN clientes c ON c.codparc = rs.codparc
        WHERE rs.route_id = :rid ORDER BY rs.sequence
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
        AND o.status IN ('routed','pending','delivered')
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
    return {"status":'released'}

class IniciarBody(BaseModel):
    km_inicial: Optional[int] = None

@router.post("/{route_id}/iniciar")
def iniciar_rota(route_id: str, body: IniciarBody = IniciarBody(), db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='executing', started_at=:now, km_inicial=:km WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat(),"km":body.km_inicial})
    db.commit()
    return {"status":'executing'}

class FinalizarBody(BaseModel):
    km_final: Optional[int] = None

@router.post("/{route_id}/finalizar")
def finalizar_rota(route_id: str, body: FinalizarBody = FinalizarBody(), db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='done', finished_at=:now, km_final=:km WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat(),"km":body.km_final})
    db.commit()
    return {"status":'done'}

@router.delete("/{route_id}")
def delete_route(route_id: str, db: Session = Depends(get_db)):
    route = db.execute(text("SELECT status FROM routes WHERE id=:id"),{"id":route_id}).fetchone()
    if not route: raise HTTPException(404,"Rota não encontrada")
    if route[0] in ('executing','done'): raise HTTPException(400,"Não pode excluir rota ativa")
    stops = db.execute(text("SELECT order_id FROM route_stops WHERE route_id=:id"),{"id":route_id}).fetchall()
    for s in stops:
        if s[0]: db.execute(text("UPDATE orders SET status='pending' WHERE id=:id"),{"id":s[0]})
    db.execute(text("DELETE FROM route_stops WHERE route_id=:id"),{"id":route_id})
    db.execute(text("DELETE FROM routes WHERE id=:id"),{"id":route_id})
    db.commit()
    return {'deleted':True}

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

    def salvar_foto(base64_str, nome_arquivo, lat=None, lng=None):
        try:
            import base64 as b64, os, io
            from PIL import Image, ImageDraw, ImageFont
            from datetime import datetime
            header, data = base64_str.split(",",1)
            img_bytes = b64.b64decode(data)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            draw = ImageDraw.Draw(img)
            w, h = img.size
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            gps_txt = f"GPS: {lat:.6f}, {lng:.6f}" if lat and lng else "GPS: indisponivel"
            texto = f"GELOCRIM  {agora}  {gps_txt}"
            font_size = max(16, w // 40)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
            margin = 10
            bbox = draw.textbbox((0,0), texto, font=font)
            tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
            x = w - tw - margin; y = h - th - margin
            draw.rectangle([x-5, y-5, x+tw+5, y+th+5], fill=(0,0,0,180))
            draw.text((x, y), texto, fill=(0,255,136), font=font)
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=80)
            buf.seek(0)
            b64_final = b64.b64encode(buf.read()).decode()
            return f"data:image/jpeg;base64,{b64_final}"
        except Exception as e:
            import logging
            logging.error(f'Erro marca dagua: {e}')
            return base64_str

    lat = body.lat_confirmacao
    lng = body.lng_confirmacao

    if body.foto_base64:
        url = salvar_foto(body.foto_base64, f"{stop_id}.jpg", lat, lng)
        if url: fields.append("foto_url=:foto_url"); params["foto_url"] = url

    if hasattr(body, "foto_nf_base64") and body.foto_nf_base64:
        url = salvar_foto(body.foto_nf_base64, f"{stop_id}_nf.jpg", lat, lng)
        if url: fields.append("foto_url=:foto_url"); params["foto_url"] = url

    if hasattr(body, "foto_boleto_base64") and body.foto_boleto_base64:
        url = salvar_foto(body.foto_boleto_base64, f"{stop_id}_boleto.jpg", lat, lng)
        if url: fields.append("foto_boleto_url=:foto_boleto_url"); params["foto_boleto_url"] = url

    if hasattr(body, "foto_comodato_base64") and body.foto_comodato_base64:
        url = salvar_foto(body.foto_comodato_base64, f"{stop_id}_comodato.jpg", lat, lng)
        if url: fields.append("foto_comodato_url=:foto_comodato_url"); params["foto_comodato_url"] = url

    if hasattr(body, "foto_outros_base64") and body.foto_outros_base64:
        url = salvar_foto(body.foto_outros_base64, f"{stop_id}_outros.jpg", lat, lng)
        if url: fields.append("foto_outros_url=:foto_outros_url"); params["foto_outros_url"] = url

    if not fields: raise HTTPException(400,"Nenhum campo")
    db.execute(text(f"UPDATE route_stops SET {', '.join(fields)} WHERE stop_id=:stop_id AND route_id=:route_id"), params)

    if body.status in ('completed','failed'):
        stop = db.execute(text("SELECT order_id FROM route_stops WHERE stop_id=:id"),{"id":stop_id}).fetchone()
        if stop and stop[0]:
            novo = 'delivered' if body.status=='completed' else 'failed'
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
 


class GpsBody(BaseModel):
    lat: float
    lng: float
    speed: Optional[float] = 0
    heading: Optional[float] = 0
    ts: Optional[str] = None

@router.post("/{route_id}/gps")
def registrar_gps(route_id: str, body: GpsBody, db: Session = Depends(get_db)):
    db.execute(text("""
        INSERT INTO route_gps (route_id, lat, lng, speed, heading, ts)
        VALUES (:rid, :lat, :lng, :speed, :heading, :ts)
    """), {"rid": route_id, "lat": body.lat, "lng": body.lng,
           "speed": body.speed or 0, "heading": body.heading or 0,
           "ts": body.ts or datetime.now().isoformat()})
    db.execute(text("""
        UPDATE routes SET last_lat=:lat, last_lng=:lng, last_seen=:ts WHERE id=:rid
    """), {"lat": body.lat, "lng": body.lng,
           "ts": body.ts or datetime.now().isoformat(), "rid": route_id})
    db.commit()
    return {"ok": True}

@router.get("/{route_id}/gps")
def listar_gps(route_id: str, limit: int = 100, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT lat, lng, speed, heading, ts
        FROM route_gps WHERE route_id = :rid
        ORDER BY ts DESC LIMIT :lim
    """), {"rid": route_id, "lim": limit}).mappings().all()
    return [dict(r) for r in rows]

class GPSBody(BaseModel):
    lat: float
    lng: float
    speed: Optional[float] = 0
    heading: Optional[float] = 0
    ts: Optional[str] = None

@router.post("/{route_id}/gps")
async def receber_gps(route_id: str, body: GPSBody, db: Session = Depends(get_db)):
    try:
        db.execute(text("""
            INSERT INTO route_gps
                (route_id, lat, lng, speed, heading, ts)
            VALUES (:rid, :lat, :lng, :spd, :hdg, :ts)
        """), {
            "rid": route_id,
            "lat": body.lat,
            "lng": body.lng,
            "spd": body.speed or 0,
            "hdg": body.heading or 0,
            "ts": body.ts or __import__("datetime").datetime.now().isoformat()
        })
        db.commit()
    except: pass
    try:
        await manager.broadcast(route_id, {
            "type": "gps_update",
            "route_id": route_id,
            "lat": body.lat,
            "lng": body.lng,
            "speed": body.speed,
            "heading": body.heading,
            "ts": body.ts
        })
    except: pass
    return {"ok": True}

@router.get("/{route_id}/gps")
def get_gps(route_id: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT lat, lng, speed, heading, ts
        FROM route_gps WHERE route_id = :rid
        ORDER BY ts DESC LIMIT 1
    """), {"rid": route_id}).mappings().all()
    return [dict(r) for r in rows]

@router.get("/{route_id}/stops/{stop_id}/proximidade")
def verificar_proximidade(route_id: str, stop_id: str, lat: float, lng: float, db: Session = Depends(get_db)):
    stop = db.execute(text("SELECT lat, lng, recipient_name FROM route_stops WHERE stop_id=:id"), {"id": stop_id}).fetchone()
    if not stop or not stop[0] or not stop[1]:
        return {"dentro": False, "distancia_m": None, "mensagem": "Coordenadas do cliente nao disponiveis"}
    distancia = haversine(lat, lng, float(stop[0]), float(stop[1]))
    dentro = distancia <= 200
    return {
        "dentro": dentro,
        "distancia_m": round(distancia),
        "limite_m": 200,
        "cliente": stop[2],
        "mensagem": f"Voce esta a {round(distancia)}m do cliente" if not dentro else "Voce esta no local!"
    }

@router.get("/gps/todos")
def get_gps_todos(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT g.route_id, g.lat, g.lng, g.speed, g.heading, g.ts,
               d.name as driver_name, r.trip_number, r.status
        FROM route_gps g
        JOIN routes r ON r.id = g.route_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        WHERE g.ts = (
            SELECT MAX(g2.ts) FROM route_gps g2
            WHERE g2.route_id = g.route_id
        )
        AND (r.status = 'executing' OR r.status = 'executando')
    """)).mappings().all()
    return [dict(r) for r in rows]
