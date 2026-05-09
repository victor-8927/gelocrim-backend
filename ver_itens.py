import sqlite3 
c = sqlite3.connect('fleet.db') 
cur = c.cursor() 
cur.execute("SELECT o.id, o.external_id, o.codparc, o.recipient_name, o.weight_kg, o.total_value FROM orders WHERE status='pending' LIMIT 3") 
[print('ORDER:', r) for r in cur.fetchall()] 
cur.execute("SELECT codparc, top_app, item_tipo, item_nome, qtd, peso_unit FROM order_items LIMIT 10") 
[print('ITEM:', r) for r in cur.fetchall()] 
