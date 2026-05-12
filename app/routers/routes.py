from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers.auth import get_current_user
from app.db_compat import now_str
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid

router    = APIRouter(prefix="/api/v1/routes", tags=["Routes"])
router_ws = APIRouter(tags=["WebSocket"])


# ─────────────────────────────────────────────
# WebSocket manager
# ─────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, route_id: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(route_id, []).append(ws)

    def disconnect(self, route_id: str, ws: WebSocket):
        try:
            self.active.get(route_id, []).remove(ws)
        except ValueError:
            pass

    async def broadcast(self, route_id: str, data: dict):
        dead = []
        for ws in self.active.get(route_id, []):
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(route_id, ws)


manager = ConnectionManager()


@router_ws.websocket("/ws/routes/{route_id}")
async def websocket_route(route_id: str, ws: WebSocket):
    await manager.connect(route_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(route_id, ws)


# ─────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────
class RouteCreate(BaseModel):
    vehicle_id:    str
    driver_id:     str
    date:          str
    planned_start: Optional[str]       = "07:30"
    order_ids:     List[str]           = []
    km_start:      Optional[int]       = None


class StopUpdate(BaseModel):
    status:              Optional[str]   = None
    ata:                 Optional[str]   = None
    atd:                 Optional[str]   = None
    lat_confirmed:       Optional[float] = None
    lng_confirmed:       Optional[float] = None
    failure_reason:      Optional[str]   = None
    foto_base64:         Optional[str]   = None
    foto_nf_base64:      Optional[str]   = None
    foto_boleto_base64:  Optional[str]   = None
    foto_comodato_base64:Optional[str]   = None
    foto_outros_base64:  Optional[str]   = None
    km_end:              Optional[int]   = None


class IniciarBody(BaseModel):
    km_inicial: Optional[int] = None


class FinalizarBody(BaseModel):
    km_final: Optional[int] = None


class GpsBody(BaseModel):
    lat:     float
    lng:     float
    speed:   Optional[float] = 0
    heading: Optional[float] = 0
    ts:      Optional[str]   = None


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2) -> float:
    from math import radians, sin, cos, sqrt, atan2
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def gerar_numero_viagem(db: Session, data_str: str) -> str:
    data = data_str.replace("-", "")[2:]
    row = db.execute(text(
        "SELECT trip_number FROM routes WHERE route_date = :d ORDER BY trip_number DESC LIMIT 1"
    ), {"d": data_str}).fetchone()
    last = 0
    if row and row[0]:
        try:
            last = int(row[0].split("-")[-1])
        except Exception:
            last = 0
    return f"VGM-{data}-{str(last + 1).zfill(3)}"


def processar_foto(base64_str: str, lat=None, lng=None) -> str:
    try:
        import base64 as b64, io
        from PIL import Image, ImageDraw, ImageFont
        header, data = base64_str.split(",", 1)
        img = Image.open(io.BytesIO(b64.b64decode(data))).convert("RGB")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        agora   = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        gps_txt = f"GPS: {lat:.6f}, {lng:.6f}" if lat and lng else "GPS: unavailable"
        texto   = f"GELOCRIM  {agora}  {gps_txt}"
        font_size = max(16, w // 40)
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
            )
        except Exception:
            font = ImageFont.load_default()
        margin = 10
        bbox = draw.textbbox((0, 0), texto, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = w - tw - margin, h - th - margin
        draw.rectangle([x - 5, y - 5, x + tw + 5, y + th + 5], fill=(0, 0, 0, 180))
        draw.text((x, y), texto, fill=(0, 255, 136), font=font)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=80)
        buf.seek(0)
        return f"data:image/jpeg;base64,{b64.b64encode(buf.read()).decode()}"
    except Exception as e:
        import logging
        logging.error(f"Photo watermark error: {e}")
        return base64_str


# ─────────────────────────────────────────────
# GET /  — lista rotas
# ─────────────────────────────────────────────
@router.get("")
def list_routes(
    date:   Optional[str] = None,
    status: Optional[str] = None,
    db:     Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    where, params = [], {}

    if date:
        where.append("r.route_date = :date")
        params["date"] = date
    if status:
        where.append("r.status = :status")
        params["status"] = status
    if current_user.get("role") == "driver":
        where.append("REPLACE(REPLACE(REPLACE(d.cpf,'.',''),'-',''),'/','') = :cpf")
        params["cpf"] = current_user.get("id")

    w = ("WHERE " + " AND ".join(where)) if where else ""

    rows = db.execute(text(f"""
        SELECT
            r.id            AS route_id,
            r.trip_number,
            r.route_date::text AS date,
            r.status,
            r.planned_start,
            r.planned_end,
            r.total_distance_km,
            r.km_start      AS km_inicial,
            r.km_end        AS km_final,
            v.plate         AS vehicle_plate,
            v.vda,
            d.name          AS driver_name,
            d.phone         AS driver_phone,
            (SELECT COUNT(*) FROM stops s WHERE s.route_id = r.id) AS total_stops,
            (SELECT COUNT(*) FROM stops s WHERE s.route_id = r.id
             AND s.status = 'completed') AS delivered_stops
        FROM routes r
        LEFT JOIN vehicles v ON v.id = r.vehicle_id
        LEFT JOIN drivers  d ON d.id = r.driver_id
        {w}
        ORDER BY r.created_at DESC
    """), params).mappings().all()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# POST /  — criar rota
# ─────────────────────────────────────────────
@router.post("")
def create_route(body: RouteCreate, db: Session = Depends(get_db)):
    route_id    = str(uuid.uuid4())
    trip_number = gerar_numero_viagem(db, body.date)

    db.execute(text("""
        INSERT INTO routes (id, trip_number, vehicle_id, driver_id,
                            route_date, planned_start, status)
        VALUES (:id, :trip, :vid, :did, :date, :ps, 'optimized')
    """), {
        "id":   route_id,
        "trip": trip_number,
        "vid":  body.vehicle_id,
        "did":  body.driver_id,
        "date": body.date,
        "ps":   body.planned_start,
    })

    # Busca pedidos e agrupa por cliente
    orders = []
    for oid in body.order_ids:
        o = db.execute(
            text("SELECT * FROM orders WHERE id = :id"), {"id": oid}
        ).mappings().fetchone()
        if o:
            orders.append(dict(o))

    clientes: dict = {}
    for o in orders:
        codparc = o.get("codparc")
        nome    = o.get("recipient_name") or ""
        addr    = o.get("address") or ""
        lat     = o.get("lat")
        lng     = o.get("lng")
        key     = codparc if codparc else (nome.strip() or o["id"])

        if key not in clientes:
            clientes[key] = {
                "codparc": codparc, "recipient_name": nome,
                "address": addr, "lat": lat, "lng": lng,
                "weight_kg": 0, "order_ids": [],
            }
        else:
            c = clientes[key]
            if not c["recipient_name"] and nome: c["recipient_name"] = nome
            if not c["address"] and addr:        c["address"] = addr
            if not c["lat"] and lat:             c["lat"] = lat
            if not c["lng"] and lng:             c["lng"] = lng

        clientes[key]["weight_kg"]  += float(o.get("weight_kg") or 0)
        clientes[key]["order_ids"].append(o["id"])

    clientes_validos = {
        k: v for k, v in clientes.items() if v["recipient_name"] or v["codparc"]
    }

    for i, (key, cli) in enumerate(clientes_validos.items()):
        stop_id = str(uuid.uuid4())
        seg = db.execute(
            text("SELECT segment FROM clients WHERE codparc = :cp"),
            {"cp": cli["codparc"]}
        ).fetchone()
        segmento = seg[0] if seg else None

        db.execute(text("""
            INSERT INTO stops
                (stop_id, route_id, order_id, sequence,
                 recipient_name, address, lat, lng,
                 weight_kg, status, codparc, segment)
            VALUES
                (:sid, :rid, :oid, :seq,
                 :name, :addr, :lat, :lng,
                 :kg, 'pending', :cp, :seg)
        """), {
            "sid":  stop_id,
            "rid":  route_id,
            "oid":  cli["order_ids"][0],
            "seq":  i,
            "name": cli["recipient_name"],
            "addr": cli["address"],
            "lat":  cli["lat"],
            "lng":  cli["lng"],
            "kg":   cli["weight_kg"],
            "cp":   cli["codparc"],
            "seg":  segmento,
        })
        for oid in cli["order_ids"]:
            db.execute(
                text("UPDATE orders SET status = 'routed' WHERE id = :id"), {"id": oid}
            )

    db.commit()
    return {
        "route_id":    route_id,
        "trip_number": trip_number,
        "status":      "optimized",
        "total_stops": len(clientes_validos),
    }


# ─────────────────────────────────────────────
# GET /{route_id}/stops
# ─────────────────────────────────────────────
@router.get("/{route_id}/stops")
def get_stops(route_id: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT
            s.stop_id, s.route_id, s.sequence,
            s.recipient_name, s.address, s.lat, s.lng,
            s.weight_kg, s.status, s.eta, s.ata, s.atd,
            s.failure_reason, s.codparc,
            s.photo_nf       AS foto_url,
            s.photo_receipt  AS foto_boleto_url,
            s.photo_loan     AS foto_comodato_url,
            s.photo_other    AS foto_outros_url,
            s.segment        AS segmento
        FROM stops s
        WHERE s.route_id = :rid
        ORDER BY s.sequence
    """), {"rid": route_id}).mappings().all()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# POST /{route_id}/liberar
# ─────────────────────────────────────────────
@router.post("/{route_id}/liberar")
def liberar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text("UPDATE routes SET status = 'released' WHERE id = :id"), {"id": route_id})
    db.commit()
    return {"status": "released"}


# ─────────────────────────────────────────────
# POST /{route_id}/iniciar
# ─────────────────────────────────────────────
@router.post("/{route_id}/iniciar")
def iniciar_rota(
    route_id: str,
    body: IniciarBody = IniciarBody(),
    db: Session = Depends(get_db),
):
    db.execute(text("""
        UPDATE routes
        SET status = 'executing', started_at = :now, km_start = :km
        WHERE id = :id
    """), {"id": route_id, "now": now_str(), "km": body.km_inicial})
    db.commit()
    return {"status": "executing"}


# ─────────────────────────────────────────────
# POST /{route_id}/finalizar
# ─────────────────────────────────────────────
@router.post("/{route_id}/finalizar")
def finalizar_rota(
    route_id: str,
    body: FinalizarBody = FinalizarBody(),
    db: Session = Depends(get_db),
):
    db.execute(text("""
        UPDATE routes
        SET status = 'done', finished_at = :now, km_end = :km
        WHERE id = :id
    """), {"id": route_id, "now": now_str(), "km": body.km_final})
    db.commit()
    return {"status": "done"}


# ─────────────────────────────────────────────
# DELETE /{route_id}
# ─────────────────────────────────────────────
@router.delete("/{route_id}")
def delete_route(route_id: str, db: Session = Depends(get_db)):
    route = db.execute(
        text("SELECT status FROM routes WHERE id = :id"), {"id": route_id}
    ).fetchone()
    if not route:
        raise HTTPException(404, "Route not found")
    if route[0] in ("executing", "done"):
        raise HTTPException(400, "Cannot delete active route")

    stops = db.execute(
        text("SELECT order_id FROM stops WHERE route_id = :id"), {"id": route_id}
    ).fetchall()
    for s in stops:
        if s[0]:
            db.execute(
                text("UPDATE orders SET status = 'pending' WHERE id = :id"), {"id": s[0]}
            )

    db.execute(text("DELETE FROM stops WHERE route_id = :id"),  {"id": route_id})
    db.execute(text("DELETE FROM routes WHERE id = :id"),        {"id": route_id})
    db.commit()
    return {"deleted": True}


# ─────────────────────────────────────────────
# PATCH /{route_id}/stops/{stop_id}
# ─────────────────────────────────────────────
@router.patch("/{route_id}/stops/{stop_id}")
async def update_stop(
    route_id: str,
    stop_id:  str,
    body:     StopUpdate,
    db:       Session = Depends(get_db),
):
    fields, params = [], {"stop_id": stop_id, "route_id": route_id}

    if body.status:         fields.append("status = :status");           params["status"] = body.status
    if body.ata:            fields.append("ata = :ata");                  params["ata"]    = body.ata
    if body.atd:            fields.append("atd = :atd");                  params["atd"]    = body.atd
    if body.lat_confirmed:  fields.append("lat_confirmed = :lat_c");     params["lat_c"]  = body.lat_confirmed
    if body.lng_confirmed:  fields.append("lng_confirmed = :lng_c");     params["lng_c"]  = body.lng_confirmed
    if body.failure_reason: fields.append("failure_reason = :fr");       params["fr"]     = body.failure_reason

    lat = body.lat_confirmed
    lng = body.lng_confirmed

    foto_map = [
        ("foto_base64",          "photo_nf",      "photo_nf"),
        ("foto_nf_base64",       "photo_nf",      "photo_nf"),
        ("foto_boleto_base64",   "photo_receipt", "photo_receipt"),
        ("foto_comodato_base64", "photo_loan",    "photo_loan"),
        ("foto_outros_base64",   "photo_other",   "photo_other"),
    ]
    for attr, col, param_key in foto_map:
        raw = getattr(body, attr)
        if raw:
            foto = processar_foto(raw, lat, lng)
            fields.append(f"{col} = :{param_key}")
            params[param_key] = foto

    if body.km_end:
        db.execute(
            text("UPDATE routes SET km_end = :km WHERE id = :id"),
            {"km": body.km_end, "id": route_id},
        )

    if not fields:
        raise HTTPException(400, "No fields to update")

    db.execute(
        text(f"UPDATE stops SET {', '.join(fields)} WHERE stop_id = :stop_id AND route_id = :route_id"),
        params,
    )

    if body.status in ("completed", "failed"):
        stop = db.execute(
            text("SELECT order_id FROM stops WHERE stop_id = :id"), {"id": stop_id}
        ).fetchone()
        if stop and stop[0]:
            novo = "delivered" if body.status == "completed" else "failed"
            db.execute(
                text("UPDATE orders SET status = :s WHERE id = :id"),
                {"s": novo, "id": stop[0]},
            )

    db.commit()

    try:
        await manager.broadcast(
            route_id,
            {"type": "stop_update", "stop_id": stop_id, "status": body.status},
        )
    except Exception:
        pass

    return {"updated": True}


# ─────────────────────────────────────────────
# POST /{route_id}/gps
# ─────────────────────────────────────────────
@router.post("/{route_id}/gps")
async def registrar_gps(
    route_id: str,
    body:     GpsBody,
    db:       Session = Depends(get_db),
):
    ts = body.ts or now_str()
    try:
        db.execute(text("""
            INSERT INTO gps_logs (route_id, lat, lng, speed, heading, ts)
            VALUES (:rid, :lat, :lng, :spd, :hdg, :ts)
        """), {
            "rid": route_id, "lat": body.lat, "lng": body.lng,
            "spd": body.speed or 0, "hdg": body.heading or 0, "ts": ts,
        })
        db.execute(text("""
            UPDATE routes
            SET last_lat = :lat, last_lng = :lng, last_seen = :ts
            WHERE id = :rid
        """), {"lat": body.lat, "lng": body.lng, "ts": ts, "rid": route_id})
        db.commit()
    except Exception:
        pass

    try:
        await manager.broadcast(
            route_id,
            {"type": "gps_update", "route_id": route_id, "lat": body.lat, "lng": body.lng},
        )
    except Exception:
        pass

    return {"ok": True}


# ─────────────────────────────────────────────
# GET /gps/todos
# ─────────────────────────────────────────────
@router.get("/gps/todos")
def get_gps_todos(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT
            g.route_id, g.lat, g.lng, g.speed, g.heading, g.ts::text,
            d.name      AS driver_name,
            r.trip_number,
            r.status
        FROM gps_logs g
        JOIN routes r ON r.id = g.route_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        WHERE g.ts = (
            SELECT MAX(g2.ts) FROM gps_logs g2 WHERE g2.route_id = g.route_id
        )
        AND r.status IN ('executing', 'executando')
    """)).mappings().all()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# GET /{route_id}/stops/{stop_id}/proximidade
# ─────────────────────────────────────────────
@router.get("/{route_id}/stops/{stop_id}/proximidade")
def verificar_proximidade(
    route_id: str,
    stop_id:  str,
    lat:      float,
    lng:      float,
    db:       Session = Depends(get_db),
):
    stop = db.execute(
        text("SELECT lat, lng, recipient_name FROM stops WHERE stop_id = :id"),
        {"id": stop_id},
    ).fetchone()

    if not stop or not stop[0] or not stop[1]:
        return {"dentro": False, "distancia_m": None, "mensagem": "Client coordinates unavailable"}

    distancia = haversine(lat, lng, float(stop[0]), float(stop[1]))
    dentro    = distancia <= 200
    return {
        "dentro":      dentro,
        "distancia_m": round(distancia),
        "limite_m":    200,
        "cliente":     stop[2],
        "mensagem":    "You are on site!" if dentro else f"You are {round(distancia)}m from client",
    }
