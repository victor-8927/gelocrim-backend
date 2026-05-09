import sqlite3
from uuid import uuid4
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/orders", tags=["Pedidos"])

class RecipientIn(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    phone: Optional[str] = None

class OrderIn(BaseModel):
    external_id: Optional[str] = None
    recipient: RecipientIn
    weight_kg: float = 0
    volume_m3: float = 0
    tw_start: Optional[str] = "08:00"
    tw_end: Optional[str] = "18:00"
    notes: Optional[str] = None

class BatchIn(BaseModel):
    source: str = "manual"
    orders: list[OrderIn]

class OrderOut(BaseModel):
    id: str
    external_id: Optional[str] = None
    recipient_name: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    weight_kg: float = 0
    volume_m3: float = 0
    tw_start: Optional[str] = None
    tw_end: Optional[str] = None
    status: str = "pending"
    created_at: Optional[str] = None
    delivery_date: Optional[str] = None
    order_type: Optional[str] = None
    total_value: Optional[float] = None
    regiao: Optional[str] = None
    priority: Optional[int] = 1
    codparc: Optional[int] = None
    tempo_entrega: Optional[str] = None
    model_config = {"from_attributes": True}


@router.get("/resumo-itens")
def resumo_itens(
    _=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resumo de quantidades de todos os pedidos do dia (qualquer status)"""
    rows = db.execute(text("""
        SELECT oi.item_nome, oi.item_tipo,
               SUM(oi.qtd) AS total_qtd,
               ROUND(SUM(oi.qtd * oi.peso_unit)) AS total_kg
        FROM order_items oi
        INNER JOIN orders o ON o.external_id = oi.nunota
        WHERE oi.item_tipo IN ('370','371','372','373')
          AND o.delivery_date = (
              SELECT MAX(delivery_date) FROM orders
              WHERE status IN ('pending','routed')
          )
        GROUP BY oi.item_tipo, oi.item_nome
        ORDER BY oi.item_tipo
    """)).fetchall()
    return [dict(r._mapping) for r in rows]

@router.get("", response_model=list[OrderOut])
def list_orders(
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """SELECT o.id, o.external_id,
               COALESCE(o.recipient_name, r.name, 'Cliente') AS recipient_name,
               COALESCE(o.address, r.address, 'Manaus - AM') AS address,
               COALESCE(o.lat, r.lat) AS lat,
               COALESCE(o.lng, r.lng) AS lng,
               o.weight_kg, o.volume_m3,
               COALESCE(o.time_window_start, o.tw_start, '07:30') AS tw_start,
               COALESCE(o.time_window_end, o.tw_end, '18:00') AS tw_end,
               o.status, o.created_at,
               o.delivery_date, o.order_type, o.total_value, o.regiao, o.priority,
               o.codparc,
               COALESCE(c.tempo_entrega, '') AS tempo_entrega
        FROM orders o
        LEFT JOIN recipients r ON r.id = o.recipient_id
        LEFT JOIN clientes c ON c.codparc = o.codparc"""
    params = {"limit": limit}
    if status:
        q += " WHERE o.status = :status"
        params["status"] = status
    q += " ORDER BY o.created_at DESC LIMIT :limit"
    rows = db.execute(text(q), params).fetchall()
    return [dict(r._mapping) for r in rows]

@router.get("/{oid}")
def get_order(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    # Buscar por id UUID ou external_id (numero da nota)
    row = db.execute(text("""
        SELECT o.id, o.external_id, o.codparc,
               COALESCE(o.recipient_name, 'Cliente') AS recipient_name,
               COALESCE(o.address, 'Manaus - AM') AS address,
               o.lat, o.lng, o.weight_kg, o.total_value,
               o.status, o.delivery_date, o.regiao, o.created_at
        FROM orders o
        WHERE o.id = :id OR o.external_id = :id
    """), {"id": oid}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado.")

    result = dict(row._mapping)

    # Buscar itens por codparc (nunota pode ser null)
    itens = db.execute(text("""
        SELECT top_app, item_tipo, item_nome, qtd, peso_unit,
               qtd * peso_unit as peso_total
        FROM order_items
        WHERE codparc = :codparc
        AND dt_neg = (SELECT MAX(dt_neg) FROM order_items WHERE codparc = :codparc)
        ORDER BY top_app, item_tipo
    """), {"codparc": result["codparc"]}).fetchall()



    # Agrupar por TOP
    tops = {}
    for item in itens:
        t = item[0] or "1000"
        if t not in tops:
            tops[t] = {"top": t, "itens": [], "peso_total": 0}
        tops[t]["itens"].append({
            "cod":        item[1],
            "nome":       item[2],
            "qtd":        item[3],
            "peso_unit":  item[4],
            "peso_total": item[5]
        })
        tops[t]["peso_total"] += item[5] or 0

    TOP_LABEL = {
        "1000": "Venda",
        "1009": "Troca",
        "1007": "Bonificacao",
        "1010": "Pre-pedido",
        "1008": "Consignacao"
    }

    result["mix_top"] = [
        {**v, "label": TOP_LABEL.get(v["top"], v["top"])}
        for v in sorted(tops.values(), key=lambda x: x["top"])
    ]
    result["peso_venda"]  = tops.get("1000", {}).get("peso_total", 0)
    result["peso_troca"]  = tops.get("1009", {}).get("peso_total", 0)
    result["peso_bonif"]  = tops.get("1007", {}).get("peso_total", 0)

    return result


@router.post("", status_code=201)
def create_order(order: dict = Body(...), db: Session = Depends(get_db)):
    import traceback
    try:
        from uuid import uuid4
        ts = now_str()

        # 1. Cria ou reutiliza recipient
        ext_id = order.get("external_id", "")
        name   = order.get("recipient_name") or order.get("nome") or "Cliente"
        addr   = order.get("address") or "Manaus - AM"
        lat    = order.get("lat")
        lng    = order.get("lng")

        rid = str(uuid4())
        db.execute(text(
            "INSERT OR IGNORE INTO recipients (id,name,address,lat,lng,created_at) "
            "VALUES (:id,:name,:addr,:lat,:lng,:ts)"
        ), {"id":rid,"name":name,"addr":addr,"lat":lat,"lng":lng,"ts":ts})

        # 2. Cria a order
        oid = str(uuid4())
        # Verificar se pedido ja existe e atualizar
        existente = db.execute(text(
            "SELECT id FROM orders WHERE external_id=:ext"
        ), {"ext": ext_id}).fetchone()

        if existente:
            db.execute(text(
                "UPDATE orders SET total_value=:tv, order_type=:ot, "
                "weight_kg=:kg, recipient_name=:rname, address=:addr, "
                "regiao=:regiao, codparc=:codparc, updated_at=:ts "
                "WHERE external_id=:ext"
            ), {
                "tv":      order.get("total_value"),
                "ot":      order.get("order_type") or order.get("notes"),
                "kg":      order.get("weight_kg", 0),
                "rname":   order.get("recipient_name") or name,
                "addr":    order.get("address") or addr,
                "regiao":  order.get("regiao"),
                "codparc": order.get("codparc"),
                "ts":      ts,
                "ext":     ext_id,
            })
            db.commit()
            return {"id": existente[0], "external_id": ext_id, "status": "updated"}

        db.execute(text(
            "INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at,total_value,order_type,"
            "recipient_name,address,regiao,codparc) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts,:tv,:ot,:rname,:addr,:regiao,:codparc)"
        ), {
            "id":      oid,
            "ext":     ext_id,
            "src":     "sankhya",
            "rid":     rid,
            "lat":     lat,
            "lng":     lng,
            "kg":      order.get("weight_kg", 0),
            "m3":      order.get("volume_m3", 0),
            "tws":     order.get("time_window_start", "07:30"),
            "twe":     order.get("time_window_end", "18:00"),
            "notes":   order.get("order_type") or order.get("notes"),
            "status":  order.get("status", "pending"),
            "priority":order.get("priority", 1),
            "ddate":   order.get("delivery_date"),
            "ts":      ts,
            "tv":      order.get("total_value"),
            "ot":      order.get("order_type") or order.get("notes"),
            "rname":   order.get("recipient_name") or name,
            "addr":    order.get("address") or addr,
            "regiao":  order.get("regiao"),
            "codparc": order.get("codparc"),
        })
        db.commit()
        return {"id": oid, "external_id": ext_id, "status": "created"}
    except Exception as e:
        print("ERRO POST /orders:", traceback.format_exc())
        raise

@router.delete("", status_code=200)
def delete_pending_orders(db: Session = Depends(get_db)):
    result = db.execute(text("DELETE FROM orders WHERE status='pending'"))
    db.commit()
    return {"deleted": result.rowcount}

@router.post("/batch", status_code=201)
def create_batch(body: BatchIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    created = []
    skipped = 0
    ts = now_str()
    for o in body.orders:
        if o.external_id:
            ex = db.execute(text("SELECT id FROM orders WHERE external_id=:ext"), {"ext": o.external_id}).fetchone()
            if ex: skipped += 1; continue
        rid = str(uuid4())
        db.execute(text("INSERT OR IGNORE INTO recipients (id,name,address,lat,lng,phone,created_at) VALUES (:id,:name,:addr,:lat,:lng,:phone,:ts)"),
            {"id":rid,"name":o.recipient.name,"addr":o.recipient.address,"lat":o.recipient.lat,"lng":o.recipient.lng,"phone":o.recipient.phone,"ts":ts})
        oid = str(uuid4())
        db.execute(text("INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,weight_kg,volume_m3,tw_start,tw_end,notes,created_at,updated_at) VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:ts,:ts)"),
            {"id":oid,"ext":o.external_id,"src":body.source,"rid":rid,"lat":o.recipient.lat,"lng":o.recipient.lng,"kg":o.weight_kg,"m3":o.volume_m3,"tws":o.tw_start,"twe":o.tw_end,"notes":o.notes,"ts":ts})
        created.append(oid)
    db.commit()
    return {"created": len(created), "skipped": skipped, "ids": created}

@router.patch("/{oid}")
def update_order(oid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"status","nfe_key","nfe_status","notes"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if updates:
        updates["updated_at"] = now_str()
        updates["id"] = oid
        sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
        db.execute(text(f"UPDATE orders SET {sets} WHERE id=:id"), updates)
        db.commit()
    return {"ok": True}

@router.delete("/{oid}", status_code=204)
def delete_order(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.execute(text("SELECT status FROM orders WHERE id=:id"), {"id": oid}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Pedido nao encontrado.")
    if row.status == "routed": raise HTTPException(status_code=409, detail="Pedido ja roteirizado.")
    db.execute(text("DELETE FROM orders WHERE id=:id"), {"id": oid})
    db.commit()



class ItemPlanilha(BaseModel):
    cod: str
    nome: str
    qtd: int
    peso_unit: float

class PedidoPlanilha(BaseModel):
    external_id: str
    num_doc: Optional[str] = None
    codparc: Optional[int] = None
    recipient_name: str
    weight_kg: float
    itens: List[ItemPlanilha] = []
    data: Optional[str] = None
    top_app: Optional[str] = None
    total_value: Optional[float] = None
    order_type: Optional[str] = None
    regiao: Optional[str] = None

class BulkPlanilhaRequest(BaseModel):
    pedidos: List[PedidoPlanilha]

@router.post("/bulk_planilha")
def bulk_planilha(body: BulkPlanilhaRequest, db: Session = Depends(get_db)):
    import uuid as _uuid
    importados = 0
    atualizados = 0

    for p in body.pedidos:
        try:
            cli = db.execute(text(
                "SELECT lat, lng, bairro, cidade, regiao FROM clientes WHERE codparc = :c"
            ), {"c": p.codparc}).mappings().fetchone()

            lat = float(cli["lat"]) if cli and cli["lat"] else None
            lng = float(cli["lng"]) if cli and cli["lng"] else None
            bairro = (cli["bairro"] or "") if cli else ""
            cidade = (cli["cidade"] or "Manaus") if cli else "Manaus"
            regiao = (cli["regiao"] or "") if cli else ""
            address = f"{bairro}, {cidade}".strip(", ") if bairro else cidade

            existente = db.execute(text(
                "SELECT id, status FROM orders WHERE external_id = :eid"
            ), {"eid": str(p.external_id)}).fetchone()

            if existente:
                if existente[1] == 'pending':
                    db.execute(text("""
                        UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,
                        regiao=:regiao, updated_at=CURRENT_TIMESTAMP,
                        total_value=COALESCE(:total_value, total_value),
                        order_type=COALESCE(:order_type, order_type)
                        WHERE external_id=:eid
                    """), {
                        "kg": float(p.weight_kg),
                        "nome": str(p.recipient_name),
                        "codparc": p.codparc,
                        "lat": lat, "lng": lng,
                        "addr": str(address),
                        "regiao": str(regiao),
                        "total_value": float(p.total_value) if p.total_value else None,
                        "order_type": str(p.order_type or p.top_app) if (p.order_type or p.top_app) else None,
                        "eid": str(p.external_id)
                    })
                    atualizados += 1
            else:
                order_id = str(_uuid.uuid4())
                db.execute(text("""
                    INSERT INTO orders (id, external_id, codparc, recipient_name,
                        weight_kg, lat, lng, address, regiao, status,
                        total_value, order_type, created_at)
                    VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,
                        :addr, :regiao, 'pending',
                        :total_value, :order_type, CURRENT_TIMESTAMP)
                """), {
                    "id": order_id,
                    "eid": str(p.external_id),
                    "codparc": p.codparc,
                    "nome": str(p.recipient_name),
                    "kg": float(p.weight_kg),
                    "lat": lat, "lng": lng,
                    "addr": str(address),
                    "regiao": str(regiao),
                    "total_value": float(p.total_value) if hasattr(p, "total_value") and p.total_value else None,
                    "order_type": str(getattr(p, "order_type", None) or getattr(p, "top_app", None) or "1000")
                })
                importados += 1

                for item in p.itens:
                    db.execute(text("""
                        INSERT INTO order_items (id, codparc, top_app, item_tipo,
                            item_nome, peso_unit, qtd, dt_neg, created_at)
                        VALUES (:id, :codparc, :top_app, :tipo, :nome,
                            :peso, :qtd, :dt, CURRENT_TIMESTAMP)
                    """), {
                        "id": str(_uuid.uuid4()),
                        "codparc": p.codparc,
                        "top_app": str(p.top_app or p.external_id),
                        "tipo": str(item.cod),
                        "nome": str(item.nome),
                        "peso": float(item.peso_unit),
                        "qtd": int(item.qtd),
                        "dt": str(p.data or "")[:10]
                    })
        except Exception as e:
            print(f"Erro no pedido {p.external_id}: {e}")
            continue

    db.commit()

    # Calcular volume automaticamente
    VOLUMES = {'370': 0.01338, '371': 0.02077, '372': 0.04901, '373': 0.07517}
    try:
        peds = db.execute(text("SELECT id, codparc FROM orders WHERE status='pending'")).fetchall()
        for oid, codparc in peds:
            if not codparc: continue
            its = db.execute(text("SELECT item_tipo, qtd FROM order_items WHERE codparc=:cp AND dt_neg=(SELECT MAX(dt_neg) FROM order_items WHERE codparc=:cp)"), {"cp": codparc}).fetchall()
            vol = sum(VOLUMES.get(str(t), 0) * int(q or 0) for t, q in its)
            if vol > 0:
                db.execute(text("UPDATE orders SET volume_m3=:v WHERE id=:i"), {"v": round(vol, 3), "i": oid})
        db.commit()
    except Exception as e:
        print(f"Aviso volume: {e}")

    return {"importados": importados, "atualizados": atualizados}
