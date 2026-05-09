path = r'C:\fleet-cloud\app\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona endpoint order_items antes do if __name__
endpoint = '''
# ── ORDER ITEMS ─────────────────────────────────────────────────────
class OrderItemBulk(BaseModel):
    items: list

@app.get("/order_items")
def get_order_items(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("""
        SELECT oi.*, c.nome as cliente_nome
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        ORDER BY oi.item_tipo, c.nome
    """).fetchall()
    return [dict(r) for r in rows]

@app.post("/order_items/bulk")
def bulk_order_items(body: OrderItemBulk, db: sqlite3.Connection = Depends(get_db)):
    items = body.items
    if not items:
        raise HTTPException(400, "Nenhum item")
    # Deleta itens do mesmo tipo antes de reimportar
    tipo = items[0].get('item_tipo')
    if tipo:
        db.execute("DELETE FROM order_items WHERE item_tipo = ?", (tipo,))
    inserted = 0
    for it in items:
        try:
            db.execute("""
                INSERT INTO order_items (codparc, top_app, item_tipo, item_nome, peso_unit, qtd, dt_neg)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                it.get('codparc'), it.get('top_app'), it.get('item_tipo'),
                it.get('item_nome'), it.get('peso_unit', 0),
                it.get('qtd', 0), it.get('dt_neg')
            ))
            inserted += 1
        except Exception as e:
            pass
    db.commit()
    return {"inserted": inserted, "tipo": tipo}

@app.delete("/order_items/{item_tipo}")
def delete_order_items_by_tipo(item_tipo: str, db: sqlite3.Connection = Depends(get_db)):
    db.execute("DELETE FROM order_items WHERE item_tipo = ?", (item_tipo,))
    db.commit()
    return {"deleted": True}
'''

if '/order_items' not in content:
    # Insere antes do último bloco
    idx = content.rfind('\nif __name__')
    if idx == -1:
        idx = len(content)
    content = content[:idx] + endpoint + content[idx:]
    print('Endpoints order_items adicionados!')
else:
    print('Endpoints já existem!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
