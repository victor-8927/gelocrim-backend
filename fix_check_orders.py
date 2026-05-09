import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
print('=== ORDERS (primeiros 5) ===')
for r in conn.execute("SELECT id, codparc, recipient_name, status, weight_kg FROM orders LIMIT 5").fetchall():
    print(r)

print('\n=== ORDERS estrutura ===')
for r in conn.execute("PRAGMA table_info(orders)").fetchall():
    print(f"  {r[1]} - {r[2]}")
conn.close()
