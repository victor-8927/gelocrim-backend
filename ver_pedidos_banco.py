import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM orders")
print(f'Total pedidos: {cur.fetchone()[0]}')
cur.execute("SELECT COUNT(*) FROM orders WHERE codparc IS NOT NULL")
print(f'Com codparc: {cur.fetchone()[0]}')
cur.execute("SELECT COUNT(*) FROM orders WHERE lat IS NOT NULL AND lat != 0")
print(f'Com GPS: {cur.fetchone()[0]}')
cur.execute("SELECT external_id, recipient_name, codparc, lat, lng, regiao FROM orders LIMIT 5")
for r in cur.fetchall():
    print(f'  {r}')
conn.close()
