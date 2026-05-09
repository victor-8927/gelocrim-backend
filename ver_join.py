import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)

print('=== ORDERS ===')
rows = conn.execute("SELECT id, external_id, recipient_id, weight_kg, status FROM orders LIMIT 5").fetchall()
for r in rows:
    print(r)
print(f'Total: {conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]}')

print('\n=== RECIPIENTS ===')
rows = conn.execute("SELECT id, name, address FROM recipients LIMIT 5").fetchall()
for r in rows:
    print(r)
print(f'Total: {conn.execute("SELECT COUNT(*) FROM recipients").fetchone()[0]}')

print('\n=== JOIN TEST ===')
rows = conn.execute("""
    SELECT o.external_id, r.name, o.weight_kg, o.status
    FROM orders o
    LEFT JOIN recipients r ON r.id = o.recipient_id
    LIMIT 5
""").fetchall()
for r in rows:
    print(r)

conn.close()
