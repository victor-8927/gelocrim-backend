import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Verifica se recipient_id existe nos orders
cur.execute("SELECT id, recipient_id, lat, lng FROM orders LIMIT 3")
for r in cur.fetchall():
    print(f'Order: {r[0][:8]} | recipient_id={r[1]} | lat={r[2]} | lng={r[3]}')

# Verifica se o recipient existe
cur.execute("SELECT id, name, lat, lng FROM recipients LIMIT 3")
for r in cur.fetchall():
    print(f'Recipient: {r[0]} | {r[1][:25]} | lat={r[2]} | lng={r[3]}')

# Testa o join direto
cur.execute("""
    SELECT o.id, o.recipient_id, r.id, r.lat, r.lng
    FROM orders o
    JOIN recipients r ON r.id = o.recipient_id
    LIMIT 3
""")
rows = cur.fetchall()
print(f'\nJoin result: {len(rows)} rows')
for r in rows:
    print(f'  order={r[0][:8]} | r_id={r[1]} | match={r[2]} | lat={r[3]}')

conn.close()
