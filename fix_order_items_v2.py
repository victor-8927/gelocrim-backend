path = r'C:\fleet-cloud\app\routers\order_items.py'

content = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/order_items", tags=["OrderItems"])

class OrderItemIn(BaseModel):
    codparc: int
    top_app: Optional[str] = "1000"
    item_tipo: str
    item_nome: str
    peso_unit: float
    qtd: int
    dt_neg: Optional[str] = None

class OrderItemBulk(BaseModel):
    items: List[OrderItemIn]

@router.get("")
def get_order_items(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT oi.id, oi.codparc, oi.top_app, oi.item_tipo, oi.item_nome,
               oi.peso_unit, oi.qtd, (oi.qtd * oi.peso_unit) as peso_total,
               oi.dt_neg, oi.created_at,
               c.nome as cliente_nome, c.rota, c.bairro
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        ORDER BY oi.item_tipo, c.nome
    """)).mappings().all()
    return [dict(r) for r in rows]

@router.get("/resumo")
def get_resumo_itens(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT oi.codparc, c.nome as cliente_nome, c.rota, c.bairro,
               SUM(CASE WHEN oi.item_tipo=\'gelo5\'  THEN oi.qtd ELSE 0 END) as qtd_gelo5,
               SUM(CASE WHEN oi.item_tipo=\'gelo10\' THEN oi.qtd ELSE 0 END) as qtd_gelo10,
               SUM(CASE WHEN oi.item_tipo=\'gelo20\' THEN oi.qtd ELSE 0 END) as qtd_gelo20,
               SUM(CASE WHEN oi.item_tipo=\'gelo40\' THEN oi.qtd ELSE 0 END) as qtd_gelo40,
               SUM(oi.qtd * oi.peso_unit) as peso_total
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        GROUP BY oi.codparc
        ORDER BY c.nome
    """)).mappings().all()
    return [dict(r) for r in rows]

@router.post("/bulk")
def bulk_order_items(body: OrderItemBulk, db: Session = Depends(get_db)):
    items = body.items
    if not items:
        raise HTTPException(400, "Nenhum item")
    tipo = items[0].item_tipo
    db.execute(text("DELETE FROM order_items WHERE item_tipo = :tipo"), {"tipo": tipo})
    inserted = 0
    for it in items:
        try:
            db.execute(text("""
                INSERT INTO order_items (codparc, top_app, item_tipo, item_nome, peso_unit, qtd, dt_neg)
                VALUES (:codparc, :top_app, :item_tipo, :item_nome, :peso_unit, :qtd, :dt_neg)
            """), {
                "codparc": it.codparc, "top_app": it.top_app,
                "item_tipo": it.item_tipo, "item_nome": it.item_nome,
                "peso_unit": it.peso_unit, "qtd": it.qtd, "dt_neg": it.dt_neg
            })
            inserted += 1
        except Exception:
            pass
    db.commit()
    return {"inserted": inserted, "tipo": tipo}

@router.delete("/{item_tipo}")
def delete_order_items(item_tipo: str, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM order_items WHERE item_tipo = :tipo"), {"tipo": item_tipo})
    db.commit()
    return {"deleted": True}
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Router order_items reescrito com SQLAlchemy!')
print('Reinicie o servidor.')
