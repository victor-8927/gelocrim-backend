from sqlalchemy import text
path = r'C:\fleet-cloud\app\routers\orders.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona POST individual e DELETE em massa antes do /batch
new_routes = '''
@router.post("", status_code=201)
def create_order(order: dict, db: sqlite3.Connection = Depends(get_db)):
    cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
            "total_value","order_type","delivery_date","regiao","status","priority",
            "lat","lng","time_window_start","time_window_end"]
    vals = [order.get(c) for c in cols]
    cur = db.execute(
        f"INSERT INTO orders ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
        vals
    )
    db.commit()
    row = db.execute(text("SELECT * FROM orders WHERE id=?"), (cur.lastrowid,)).fetchone()
    desc = db.execute(text("SELECT * FROM orders LIMIT 0"))
    return dict(zip([d[0] for d in desc], row))

@router.delete("", status_code=200)
def delete_pending_orders(db: sqlite3.Connection = Depends(get_db)):
    result = db.execute("DELETE FROM orders WHERE status='pending'")
    db.commit()
    return {"deleted": result.rowcount}

'''

# Insere antes do @router.post("/batch")
if '@router.post("")' not in content:
    content = content.replace(
        '@router.post("/batch"',
        new_routes + '@router.post("/batch"'
    )
    print('POST e DELETE adicionados!')
else:
    print('POST já existe!')

# Garante que sqlite3 está importado
if 'import sqlite3' not in content:
    content = 'import sqlite3\n' + content
    print('sqlite3 importado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Reinicie o servidor.')
