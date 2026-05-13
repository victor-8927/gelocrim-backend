from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user
from app.translations import normalizar, normalizar_status, normalizar_codparc

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


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
    region: Optional[str] = None
    priority: Optional[int] = 1
    codparc: Optional[int] = None
    service_time: Optional[str] = None
    model_config = {"from_attributes": True}


@router.get("/resumo-itens")
def resumo_itens(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT item_name, item_type, total_qty, total_kg FROM vw_resumo_producao WHERE delivery_date = (SELECT MAX(delivery_date) FROM orders WHERE status IN ('pending','routed'))
    """)).fetchall()
    return [dict(r._mapping) for r in rows]


@router.get("", response_model=list[OrderOut])
def list_orders(
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """
        SELECT
            o.id,
            o.external_id,
            COALESCE(c.name, o.recipient_name, 'Parceiro') AS recipient_name,
            COALESCE(c.address, o.address, 'Manaus - AM')  AS address,
            COALESCE(c.lat, o.lat)                          AS lat,
            COALESCE(c.lng, o.lng)                          AS lng,
            o.weight_kg,
            o.volume_m3,
            COALESCE(o.tw_start, '07:30')                  AS tw_start,
            COALESCE(o.tw_end,   '18:00')                  AS tw_end,
            o.status,
            o.created_at::text,
            o.delivery_date::text                           AS delivery_date,
            o.order_type,
            o.total_value,
            o.region,
            o.priority,
            o.codparc,
            COALESCE(c.service_time, '') AS service_time
        FROM orders o
        LEFT JOIN clients c ON c.codparc = o.codparc
    """
    params: dict = {"limit": limit}
    if status:
        q += " WHERE o.status = :status"
        params["status"] = status
    q += " ORDER BY o.created_at DESC LIMIT :limit"
    rows = db.execute(text(q), params).fetchall()
    return [dict(r._mapping) for r in rows]


@router.get("/{oid}")
def get_order(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.execute(text("""
        SELECT o.id, o.external_id, o.codparc,
               COALESCE(c.name, o.recipient_name, 'Parceiro') AS recipient_name,
               COALESCE(c.address, o.address, 'Manaus - AM')  AS address,
               COALESCE(c.lat, o.lat) AS lat,
               COALESCE(c.lng, o.lng) AS lng,
               o.weight_kg, o.total_value,
               o.status, o.delivery_date::text, o.region, o.created_at::text
        FROM orders o
        LEFT JOIN clients c ON c.codparc = o.codparc
        WHERE o.id = :id OR o.external_id = :id
    """), {"id": oid}).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found.")
    result = dict(row._mapping)
    itens = db.execute(text("""
        SELECT top_app, item_type, item_name, qty, weight_unit,
               qty * weight_unit as total_weight
        FROM order_items
        WHERE codparc = :codparc
        AND negotiation_date = (SELECT MAX(negotiation_date) FROM order_items WHERE codparc = :codparc)
        ORDER BY top_app, item_type
    """), {"codparc": result["codparc"]}).fetchall()
    tops = {}
    for item in itens:
        t = item[0] or "1000"
        if t not in tops:
            tops[t] = {"top": t, "items": [], "total_weight": 0}
        tops[t]["items"].append({"type": item[1], "name": item[2],
            "qty": item[3], "weight_unit": item[4], "total_weight": item[5]})
        tops[t]["total_weight"] += item[5] or 0
    TOP_LABEL = {"1000":"Venda","1009":"Troca","1007":"Bonificacao","1010":"Pre-pedido","1008":"Consignacao"}
    result["mix_top"] = [{**v, "label": TOP_LABEL.get(v["top"], v["top"])} for v in sorted(tops.values(), key=lambda x: x["top"])]
    result["weight_sale"]  = tops.get("1000", {}).get("total_weight", 0)
    result["weight_trade"] = tops.get("1009", {}).get("total_weight", 0)
    result["weight_bonus"] = tops.get("1007", {}).get("total_weight", 0)
    return result


@router.post("", status_code=201)
def create_order(order: dict = Body(...), db: Session = Depends(get_db)):
    import traceback
    try:
        ts = now_str()
        order = normalizar(order)
        name    = order.get("recipient_name") or order.get("name") or "Parceiro"
        addr    = order.get("address") or "Manaus - AM"
        lat     = order.get("lat")
        lng     = order.get("lng")
        weight  = order.get("weight_kg") or 0
        region  = order.get("region") or ""
        codparc = normalizar_codparc(order.get("codparc"))
        status  = normalizar_status(order.get("status", "pending"))
        tw_start = order.get("tw_start") or "07:30"
        tw_end   = order.get("tw_end")   or "18:00"
        ext_id   = order.get("external_id") or ""
        rid = str(uuid4())
        db.execute(text("""
            INSERT INTO recipients (id, name, address, lat, lng, created_at)
            VALUES (:id, :name, :addr, :lat, :lng, :ts)
            ON CONFLICT DO NOTHING
        """), {"id": rid, "name": name, "addr": addr, "lat": lat, "lng": lng, "ts": ts})
        existente = db.execute(
            text("SELECT id FROM orders WHERE external_id = :ext"), {"ext": ext_id}
        ).fetchone()
        if existente:
            db.execute(text("""
                UPDATE orders SET total_value=:tv, order_type=:ot, weight_kg=:kg,
                    recipient_name=:rname, address=:addr, region=:region,
                    codparc=:codparc, updated_at=:ts
                WHERE external_id=:ext
            """), {"tv": order.get("total_value"), "ot": order.get("order_type"),
                   "kg": weight, "rname": name, "addr": addr, "region": region,
                   "codparc": codparc, "ts": ts, "ext": ext_id})
            db.commit()
            return {"id": existente[0], "external_id": ext_id, "status": "updated"}
        oid = str(uuid4())
        db.execute(text("""
            INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,
                weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,
                delivery_date,created_at,updated_at,total_value,order_type,
                recipient_name,address,region,codparc)
            VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,
                    :ddate,:ts,:ts,:tv,:ot,:rname,:addr,:region,:codparc)
        """), {"id":oid,"ext":ext_id,"src":"sankhya","rid":rid,"lat":lat,"lng":lng,
               "kg":weight,"m3":order.get("volume_m3",0),"tws":tw_start,"twe":tw_end,
               "notes":order.get("order_type"),"status":status,"priority":order.get("priority",1),
               "ddate":order.get("delivery_date"),"ts":ts,"tv":order.get("total_value"),
               "ot":order.get("order_type"),"rname":name,"addr":addr,"region":region,"codparc":codparc})
        db.commit()
        return {"id": oid, "external_id": ext_id, "status": "created"}
    except Exception:
        print("ERROR POST /orders:", traceback.format_exc())
        raise


@router.delete("", status_code=200)
def delete_pending_orders(_=Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.execute(text("DELETE FROM orders WHERE status IN ('pending','routed')"))
    db.commit()
    return {"deleted": result.rowcount}


@router.patch("/{oid}/status")
def update_order_status(oid: str, body: dict = Body(...),
                        _=Depends(get_current_user), db: Session = Depends(get_db)):
    status = body.get("status")
    if not status:
        raise HTTPException(400, "Status required")
    db.execute(text("UPDATE orders SET status=:s, updated_at=:ts WHERE id=:id"),
               {"s": status, "ts": now_str(), "id": oid})
    db.commit()
    return {"updated": True}



@router.post("/bulk_planilha", status_code=200)
def bulk_planilha(body: dict = Body(...), db: Session = Depends(get_db)):
    import traceback
    try:
        pedidos = body.get("pedidos", [])
        importados = 0
        atualizados = 0
        ts = now_str()
        for p in pedidos:
            ext_id  = str(p.get("external_id") or "")
            codparc = normalizar_codparc(p.get("codparc"))
            name    = p.get("recipient_name") or "Parceiro"
            weight  = float(p.get("weight_kg") or 0)
            ddate   = p.get("data")
            itens   = p.get("itens") or []
            existente = db.execute(
                text("SELECT id FROM orders WHERE external_id = :ext"), {"ext": ext_id}
            ).fetchone()
            if existente:
                db.execute(text("""
                    UPDATE orders SET weight_kg=:kg, codparc=:cp,
                        recipient_name=:name, updated_at=:ts
                    WHERE external_id=:ext
                """), {"kg": weight, "cp": codparc, "name": name, "ts": ts, "ext": ext_id})
                oid = existente[0]
                atualizados += 1
            else:
                oid = str(__import__('uuid').uuid4())
                db.execute(text("""
                    INSERT INTO orders (id, external_id, source, weight_kg, codparc,
                        recipient_name, status, priority, delivery_date, created_at, updated_at,
                        order_type, address, volume_m3, tw_start, tw_end)
                    VALUES (:id, :ext, 'planilha', :kg, :cp,
                        :name, 'pending', 1, :ddate, :ts, :ts,
                        '1000', 'Manaus - AM', 0, '07:30', '18:00')
                """), {"id": oid, "ext": ext_id, "kg": weight, "cp": codparc,
                       "name": name, "ddate": ddate, "ts": ts})
                importados += 1
            if itens:
                db.execute(text("DELETE FROM order_items WHERE invoice_number = :ext"), {"ext": ext_id})
                for it in itens:
                    db.execute(text("""
                        INSERT INTO order_items (id, codparc, top_app, item_type, item_name, weight_unit, qty, negotiation_date, invoice_number, created_at) VALUES (gen_random_uuid(), :cp, :top, :tipo, :nome, :peso, :qty, :ddate, :inv, :ts)
                    """), {
                        "cp": codparc, "top": it.get("top_app", "1000"),
                        "tipo": it.get("item_type") or it.get("cod"), "nome": it.get("item_name") or it.get("nome"), "peso": float(it.get("weight_unit") or it.get("peso_unit") or 0), "qty": int(it.get("qty") or it.get("qtd") or 0),
                        "ddate": ddate, "inv": ext_id, "ts": ts
                    })
        db.commit()
        return {"importados": importados, "atualizados": atualizados}
    except Exception:
        print("ERROR bulk_planilha:", traceback.format_exc())
        raise


