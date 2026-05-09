import sqlite3 
c = sqlite3.connect('fleet.db') 
cur = c.cursor() 
print('=== STOPS ROTA ATIVA ===') 
cur.execute("SELECT sequence, recipient_name, codparc, weight_kg, status FROM route_stops WHERE route_id='5e354169-2f06-4569-a32c-779b705e53d9' ORDER BY sequence") 
[print(r) for r in cur.fetchall()] 
print('=== PEDIDOS POR CODPARC ===') 
cur.execute("SELECT codparc, recipient_name, COUNT(*) as notas, SUM(weight_kg) as peso FROM orders WHERE status='pending' GROUP BY codparc ORDER BY notas DESC LIMIT 15") 
[print(r) for r in cur.fetchall()] 
