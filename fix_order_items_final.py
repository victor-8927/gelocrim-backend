path = r'C:\fleet-cloud\app\routers\order_items.py'

content = '''import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db

router = APIRouter(prefix="/api/v1/order_items", tags=["OrderItems"])

class OrderItemBulk(BaseModel):
    items: list

@router.get("")
def get_order_items(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT oi.id, oi.codparc, oi.top_app, oi.item_tipo, oi.item_nome,
               oi.peso_unit, oi.qtd, (oi.qtd * oi.peso_unit) as peso_total,
               oi.dt_neg, oi.created_at,
               c.nome as cliente_nome
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        ORDER BY oi.item_tipo, c.nome
    """).fetchall()
    return [dict(r) for r in rows]

@router.get("/resumo")
def get_resumo_itens(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT oi.codparc, c.nome as cliente_nome, c.rota,
               SUM(CASE WHEN oi.item_tipo='gelo5'  THEN oi.qtd ELSE 0 END) as qtd_gelo5,
               SUM(CASE WHEN oi.item_tipo='gelo10' THEN oi.qtd ELSE 0 END) as qtd_gelo10,
               SUM(CASE WHEN oi.item_tipo='gelo20' THEN oi.qtd ELSE 0 END) as qtd_gelo20,
               SUM(CASE WHEN oi.item_tipo='gelo40' THEN oi.qtd ELSE 0 END) as qtd_gelo40,
               SUM(oi.qtd * oi.peso_unit) as peso_total
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        GROUP BY oi.codparc
        ORDER BY c.nome
    """).fetchall()
    return [dict(r) for r in rows]

@router.post("/bulk")
def bulk_order_items(body: OrderItemBulk, db: sqlite3.Connection = Depends(get_db)):
    items = body.items
    if not items:
        raise HTTPException(400, "Nenhum item")
    tipo = items[0].get("item_tipo")
    if tipo:
        db.execute("DELETE FROM order_items WHERE item_tipo = ?", (tipo,))
    inserted = 0
    for it in items:
        try:
            db.execute("""
                INSERT INTO order_items (codparc, top_app, item_tipo, item_nome, peso_unit, qtd, dt_neg)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                it.get("codparc"), it.get("top_app"), it.get("item_tipo"),
                it.get("item_nome"), it.get("peso_unit", 0),
                it.get("qtd", 0), it.get("dt_neg")
            ))
            inserted += 1
        except Exception:
            pass
    db.commit()
    return {"inserted": inserted, "tipo": tipo}

@router.delete("/{item_tipo}")
def delete_order_items(item_tipo: str, db: sqlite3.Connection = Depends(get_db)):
    db.execute("DELETE FROM order_items WHERE item_tipo = ?", (item_tipo,))
    db.commit()
    return {"deleted": True}
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Router order_items corrigido!')
print('Reinicie o servidor.')
