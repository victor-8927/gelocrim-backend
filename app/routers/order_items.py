from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

router = APIRouter(prefix="/api/v1/order_items", tags=["OrderItems"])

class OrderItemIn(BaseModel):
    codparc: int
    top_app: Optional[str] = "1000"
    item_type: Optional[str] = Field(None, alias="item_tipo")
    item_name: Optional[str] = Field(None, alias="item_nome")
    weight_unit: Optional[float] = Field(0, alias="peso_unit")
    qty: Optional[int] = Field(0, alias="qtd")
    negotiation_date: Optional[str] = Field(None, alias="dt_neg")
    invoice_number: Optional[str] = Field(None, alias="nunota")

    model_config = {"populate_by_name": True}

class OrderItemBulk(BaseModel):
    items: List[OrderItemIn]

@router.get("")
def get_order_items(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT oi.id, oi.codparc, oi.top_app,
               oi.item_type AS item_tipo,
               oi.item_name AS item_nome,
               oi.weight_unit AS peso_unit,
               oi.qty AS qtd,
               (oi.qty * oi.weight_unit) as peso_total,
               oi.negotiation_date AS dt_neg, oi.created_at,
               c.name AS cliente_nome, c.route AS rota, c.district AS bairro
        FROM order_items oi
        LEFT JOIN clients c ON c.codparc = oi.codparc
        ORDER BY oi.item_type, c.name
    """)).mappings().all()
    return [dict(r) for r in rows]

@router.post("/bulk")
def bulk_order_items(body: OrderItemBulk, db: Session = Depends(get_db)):
    items = body.items
    if not items: raise HTTPException(400, "No items")
    tipo = items[0].item_type
    db.execute(text("DELETE FROM order_items WHERE item_type=:tipo"), {"tipo": tipo})
    inserted = 0
    for it in items:
        try:
            db.execute(text("""
                INSERT INTO order_items (codparc,top_app,item_type,item_name,
                    weight_unit,qty,negotiation_date,invoice_number,created_at)
                VALUES (:codparc,:top_app,:item_type,:item_name,
                    :weight_unit,:qty,:neg_date,:inv_num,NOW())
            """), {
                "codparc": it.codparc, "top_app": it.top_app,
                "item_type": it.item_type, "item_name": it.item_name,
                "weight_unit": it.weight_unit, "qty": it.qty,
                "neg_date": it.negotiation_date, "inv_num": it.invoice_number
            })
            inserted += 1
        except: pass
    db.commit()
    return {"inserted": inserted}

@router.delete("/{item_type}")
def delete_order_items(item_type: str, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM order_items WHERE item_type=:tipo"), {"tipo": item_type})
    db.commit()
    return {"deleted": True}
