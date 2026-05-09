import os

# 1. Cria o router de order_items
router_content = '''import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import get_db

router = APIRouter()

class OrderItemBulk(BaseModel):
    items: list

@router.get("/order_items")
def get_order_items(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT oi.*, c.nome as cliente_nome
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        ORDER BY oi.item_tipo, c.nome
    """).fetchall()
    return [dict(r) for r in rows]

@router.post("/order_items/bulk")
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

@router.delete("/order_items/{item_tipo}")
def delete_order_items(item_tipo: str, db: sqlite3.Connection = Depends(get_db)):
    db.execute("DELETE FROM order_items WHERE item_tipo = ?", (item_tipo,))
    db.commit()
    return {"deleted": True}
'''

router_path = r'C:\fleet-cloud\app\routers\order_items.py'
with open(router_path, 'w', encoding='utf-8') as f:
    f.write(router_content)
print('Router order_items.py criado!')

# 2. Remove o bloco inserido errado do main.py
main_path = r'C:\fleet-cloud\app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove bloco order_items do main.py
import re
content = re.sub(
    r'\n# ── ORDER ITEMS ──.*?@app\.delete\("/order_items/\{item_tipo\}"\).*?\n\}',
    '',
    content,
    flags=re.DOTALL
)
print('Bloco removido do main.py!')

# 3. Adiciona import do novo router
old_import = 'from app.routers.clientes import router as clientes_router'
new_import = '''from app.routers.clientes import router as clientes_router
from app.routers.order_items import router as order_items_router'''
content = content.replace(old_import, new_import)

# 4. Registra o router
old_include = 'app.include_router(clientes_router)'
new_include = '''app.include_router(clientes_router)
app.include_router(order_items_router)'''
content = content.replace(old_include, new_include)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('main.py atualizado com novo router!')
print('Pronto! Reinicie o servidor.')
