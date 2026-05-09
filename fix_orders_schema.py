import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)

# ── 1. Limpa TODOS os pedidos antigos ─────────────────────────────
conn.execute("DELETE FROM orders")
conn.commit()
print('Todos os pedidos antigos removidos!')

# ── 2. Adiciona colunas faltando ───────────────────────────────────
novas_colunas = [
    ("recipient_name", "TEXT"),
    ("address",        "TEXT"),
    ("order_type",     "TEXT"),
    ("total_value",    "REAL"),
    ("regiao",         "TEXT"),
    ("time_window_start", "TEXT"),
    ("time_window_end",   "TEXT"),
]

cols_existentes = [c[1] for c in conn.execute("PRAGMA table_info(orders)").fetchall()]
print(f'\nColunas existentes: {cols_existentes}')

for col, tipo in novas_colunas:
    if col not in cols_existentes:
        conn.execute(f"ALTER TABLE orders ADD COLUMN {col} {tipo}")
        print(f'Coluna adicionada: {col}')
    else:
        print(f'Coluna já existe: {col}')

conn.commit()
conn.close()
print('\nBanco atualizado!')

# ── 3. Corrige o POST /orders para usar as colunas corretas ────────
orders_path = r'C:\fleet-cloud\app\routers\orders.py'
with open(orders_path, 'r') as f:
    content = f.read()

old_post_body = '''    try:
        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]
        vals = [order.get(c) for c in cols]
        cur = db.execute(
            f"INSERT INTO orders ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
            vals
        )
        db.commit()
        return {"id": cur.lastrowid, "external_id": order.get("external_id"), "status": "created"}
    except Exception as e:
        import traceback
        print("ERRO POST /orders:", traceback.format_exc())
        raise'''

new_post_body = '''    try:
        import traceback
        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]
        vals = [order.get(c) for c in cols]
        cur = db.execute(
            f"INSERT INTO orders ({\\',\\'.join(cols)}) VALUES ({\\',\\'.join([\'?\']*len(cols))})",
            vals
        )
        db.commit()
        return {"id": cur.lastrowid, "external_id": order.get("external_id"), "status": "created"}
    except Exception as e:
        print("ERRO POST /orders:", traceback.format_exc())
        raise'''

# Abordagem mais simples - reescreve o arquivo orders.py com POST correto
import re

# Encontra e substitui o bloco POST
new_post = '''@router.post("", status_code=201)
def create_order(order: dict = Body(...), db: sqlite3.Connection = Depends(get_db)):
    import traceback
    try:
        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]
        vals = [order.get(c) for c in cols]
        cur = db.execute(
            "INSERT INTO orders (" + ",".join(cols) + ") VALUES (" + ",".join(["?"]*len(cols)) + ")",
            vals
        )
        db.commit()
        return {"id": cur.lastrowid, "external_id": order.get("external_id"), "status": "created"}
    except Exception as e:
        print("ERRO POST /orders:", traceback.format_exc())
        raise

'''

# Remove o POST antigo e insere o novo
content = re.sub(
    r'@router\.post\("", status_code=201\).*?(?=@router\.post\("/batch"\))',
    new_post,
    content,
    flags=re.DOTALL
)

with open(orders_path, 'w') as f:
    f.write(content)

print('\nPOST /orders corrigido!')
print('\nReinicie o servidor e reimporte o XLS!')
