import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("PRAGMA table_info(orders)")
cols = [c[1] for c in cur.fetchall()]
print('Colunas orders:', cols)

# Mostra um pedido completo
cur.execute("SELECT * FROM orders LIMIT 1")
row = cur.fetchone()
if row:
    cur.execute("PRAGMA table_info(orders)")
    names = [c[1] for c in cur.fetchall()]
    for n, v in zip(names, row):
        print(f'  {n}: {repr(v)}')
conn.close()
