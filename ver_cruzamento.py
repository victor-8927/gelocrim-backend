import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)

print('=== AMOSTRA ORDERS (campos externos) ===')
rows = conn.execute("""
    SELECT external_id, recipient_name, lat, lng, regiao, notes
    FROM orders LIMIT 5
""").fetchall()
for r in rows:
    print(r)

print('\n=== CLIENTES CADASTRADOS ===')
total = conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
print(f'Total: {total}')

rows = conn.execute("""
    SELECT codparc, nome, lat, lng, regiao, endereco
    FROM clientes WHERE lat IS NOT NULL LIMIT 5
""").fetchall()
for r in rows:
    print(r)

print('\n=== CODPARC NOS PEDIDOS? ===')
# Verifica se temos o PARCEIRO salvo nos pedidos
rows = conn.execute("""
    SELECT external_id, notes
    FROM orders LIMIT 10
""").fetchall()
for r in rows:
    print(r)

conn.close()
