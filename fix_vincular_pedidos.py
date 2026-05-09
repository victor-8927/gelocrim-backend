import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Verifica quantos pedidos têm codparc mas sem lat/lng
cur.execute("""
    SELECT COUNT(*) FROM orders 
    WHERE codparc IS NOT NULL 
    AND (lat IS NULL OR lng IS NULL OR lat = 0 OR lng = 0)
""")
sem_gps = cur.fetchone()[0]
print(f'Pedidos sem GPS mas com codparc: {sem_gps}')

# Atualiza lat/lng/regiao/rota dos pedidos usando os dados dos clientes
cur.execute("""
    UPDATE orders SET
        lat = (SELECT lat FROM clientes WHERE clientes.codparc = orders.codparc AND clientes.lat IS NOT NULL LIMIT 1),
        lng = (SELECT lng FROM clientes WHERE clientes.codparc = orders.codparc AND clientes.lng IS NOT NULL LIMIT 1),
        regiao = (SELECT regiao FROM clientes WHERE clientes.codparc = orders.codparc LIMIT 1),
        recipient_name = CASE 
            WHEN recipient_name IS NULL OR recipient_name = '' OR recipient_name LIKE 'CODPARC%'
            THEN (SELECT nome FROM clientes WHERE clientes.codparc = orders.codparc LIMIT 1)
            ELSE recipient_name
        END,
        address = CASE
            WHEN address IS NULL OR address = ''
            THEN (SELECT endereco FROM clientes WHERE clientes.codparc = orders.codparc LIMIT 1)
            ELSE address
        END
    WHERE codparc IS NOT NULL
""")
print(f'Pedidos atualizados: {cur.rowcount}')

# Verifica resultado
cur.execute("""
    SELECT COUNT(*) FROM orders 
    WHERE lat IS NOT NULL AND lat != 0
""")
com_gps = cur.fetchone()[0]
print(f'Pedidos com GPS agora: {com_gps}')

# Amostra
cur.execute("""
    SELECT o.external_id, o.recipient_name, o.codparc, o.lat, o.lng, o.regiao, c.rota
    FROM orders o
    LEFT JOIN clientes c ON c.codparc = o.codparc
    LIMIT 5
""")
rows = cur.fetchall()
print('\nAmostra:')
for r in rows:
    print(f'  {r[0]} | {r[1][:25]} | codparc={r[2]} | lat={r[3]:.4f if r[3] else None} | regiao={r[5]} | rota={r[6]}')

conn.commit()
conn.close()
print('\nPronto! Ctrl+Shift+R e abra Roteirização.')
