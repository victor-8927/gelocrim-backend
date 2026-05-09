import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')

print('=== ORDERS (primeiros 5) ===')
for r in conn.execute("SELECT id, codparc, recipient_name, weight_kg, status FROM orders LIMIT 5").fetchall():
    print(r)

print('\n=== Peso total ===')
r = conn.execute("SELECT COUNT(*), SUM(weight_kg) FROM orders WHERE status='pending'").fetchone()
print(f'Pedidos: {r[0]}, Peso total: {r[1]}')

print('\n=== ORDER_ITEMS (primeiros 5) ===')
for r in conn.execute("SELECT codparc, item_nome, qtd, peso_unit FROM order_items LIMIT 5").fetchall():
    print(r)
conn.close()
