import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')

print('=== ORDERS - peso ===')
rows = conn.execute("""
    SELECT codparc, recipient_name, weight_kg, status 
    FROM orders 
    WHERE status='pending' 
    ORDER BY weight_kg DESC
    LIMIT 10
""").fetchall()
for r in rows:
    print(f'  codparc:{r[0]} | {r[1][:30]} | {r[2]}kg | {r[3]}')

print('\n=== TOTAL ===')
r = conn.execute("SELECT COUNT(*), SUM(weight_kg), AVG(weight_kg) FROM orders WHERE status='pending'").fetchone()
print(f'  {r[0]} pedidos | total:{r[1]}kg | media:{r[2]:.1f}kg')

print('\n=== ORDER_ITEMS (amostra) ===')
rows2 = conn.execute("""
    SELECT codparc, item_nome, qtd, peso_unit, qtd*peso_unit as peso_total
    FROM order_items LIMIT 10
""").fetchall()
for r in rows2:
    print(f'  cod:{r[0]} | {r[1]} | {r[2]}x | {r[3]}kg/un | total:{r[4]}kg')
conn.close()
