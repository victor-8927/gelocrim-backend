import sqlite3

# ── 1. Mostra o POST /orders atual ────────────────────────────────
path_orders = r'C:\fleet-cloud\app\routers\orders.py'
with open(path_orders, 'r') as f:
    content = f.read()

import re
m = re.search(r'@router\.post\(""\).*?(?=@router|\Z)', content, re.DOTALL)
if m:
    print('=== POST /orders atual ===')
    print(m.group()[:600])

# ── 2. Verifica estrutura da tabela orders ─────────────────────────
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
print('\n=== COLUNAS DA TABELA ORDERS ===')
cols = conn.execute("PRAGMA table_info(orders)").fetchall()
for c in cols:
    print(f'  {c[1]} ({c[2]})')

print('\n=== CONTAGEM POR STATUS ===')
rows = conn.execute("SELECT status, COUNT(*) FROM orders GROUP BY status").fetchall()
for r in rows:
    print(f'  {r[0]}: {r[1]} pedidos')

print('\n=== PESO TOTAL ===')
peso = conn.execute("SELECT SUM(weight_kg) FROM orders").fetchone()[0]
print(f'  Total: {peso} kg')

conn.close()
