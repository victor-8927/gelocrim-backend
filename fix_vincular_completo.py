import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Atualiza orders com dados dos recipients
cur.execute("""
    UPDATE orders SET
        lat = (SELECT lat FROM recipients WHERE recipients.id = orders.recipient_id),
        lng = (SELECT lng FROM recipients WHERE recipients.id = orders.recipient_id),
        recipient_name = (SELECT name FROM recipients WHERE recipients.id = orders.recipient_id),
        address = (SELECT address FROM recipients WHERE recipients.id = orders.recipient_id),
        codparc = CAST(REPLACE(orders.recipient_id, 'SNK-CLI-', '') AS INTEGER)
    WHERE recipient_id IS NOT NULL
""")
print(f'Orders atualizados com recipient: {cur.rowcount}')

# 2. Agora atualiza codparc, regiao e tempo via tabela clientes
cur.execute("""
    UPDATE orders SET
        regiao = (SELECT regiao FROM clientes WHERE clientes.codparc = orders.codparc),
        lat = COALESCE(
            (SELECT lat FROM clientes WHERE clientes.codparc = orders.codparc AND lat IS NOT NULL),
            lat
        ),
        lng = COALESCE(
            (SELECT lng FROM clientes WHERE clientes.codparc = orders.codparc AND lng IS NOT NULL),
            lng
        )
    WHERE codparc IS NOT NULL
""")
print(f'Orders atualizados com clientes: {cur.rowcount}')

# Verifica resultado
cur.execute("SELECT COUNT(*) FROM orders WHERE lat IS NOT NULL AND lat != 0")
print(f'Orders com GPS: {cur.fetchone()[0]}')

cur.execute("SELECT COUNT(*) FROM orders WHERE regiao IS NOT NULL")
print(f'Orders com região: {cur.fetchone()[0]}')

# Amostra
cur.execute("""
    SELECT o.external_id, o.recipient_name, o.codparc, o.lat, o.lng, o.regiao, o.weight_kg
    FROM orders o
    WHERE o.lat IS NOT NULL
    LIMIT 5
""")
print('\nAmostra pedidos com GPS:')
for r in cur.fetchall():
    print(f'  {r[0]} | {str(r[1])[:25]} | codparc={r[2]} | lat={r[3]:.4f} | regiao={r[5]} | {r[6]}kg')

conn.commit()
conn.close()
print('\nPronto! Ctrl+Shift+R e abra Roteirização.')
