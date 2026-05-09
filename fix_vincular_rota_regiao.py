import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Ver situação atual
cur.execute("SELECT COUNT(*) FROM orders WHERE regiao IS NOT NULL")
print(f'Orders com regiao: {cur.fetchone()[0]}')
cur.execute("SELECT COUNT(*) FROM orders WHERE codparc IS NOT NULL")
print(f'Orders com codparc: {cur.fetchone()[0]}')

# Ver se recipient_id tem o codparc embutido
cur.execute("SELECT recipient_id FROM orders LIMIT 3")
for r in cur.fetchall():
    print(f'  recipient_id: {r[0]}')

# Ver a tabela recipients com mais detalhes
cur.execute("SELECT id, name FROM recipients LIMIT 5")
for r in cur.fetchall():
    print(f'  recipient: {r[0]} | {r[1][:30]}')

# Tenta vincular orders -> recipients -> clientes pelo nome
cur.execute("""
    UPDATE orders SET
        regiao = (
            SELECT c.regiao FROM recipients r
            JOIN clientes c ON UPPER(TRIM(c.nome)) = UPPER(TRIM(r.name))
            WHERE r.id = orders.recipient_id
            LIMIT 1
        ),
        lat = (
            SELECT c.lat FROM recipients r
            JOIN clientes c ON UPPER(TRIM(c.nome)) = UPPER(TRIM(r.name))
            WHERE r.id = orders.recipient_id AND c.lat IS NOT NULL
            LIMIT 1
        ),
        lng = (
            SELECT c.lng FROM recipients r
            JOIN clientes c ON UPPER(TRIM(c.nome)) = UPPER(TRIM(r.name))
            WHERE r.id = orders.recipient_id AND c.lng IS NOT NULL
            LIMIT 1
        ),
        codparc = (
            SELECT c.codparc FROM recipients r
            JOIN clientes c ON UPPER(TRIM(c.nome)) = UPPER(TRIM(r.name))
            WHERE r.id = orders.recipient_id
            LIMIT 1
        ),
        recipient_name = (
            SELECT r.name FROM recipients r WHERE r.id = orders.recipient_id LIMIT 1
        ),
        address = (
            SELECT r.address FROM recipients r WHERE r.id = orders.recipient_id LIMIT 1
        )
    WHERE recipient_id IS NOT NULL
""")
print(f'\nOrders atualizados: {cur.rowcount}')

cur.execute("SELECT COUNT(*) FROM orders WHERE lat IS NOT NULL AND lat != 0")
print(f'Orders com GPS: {cur.fetchone()[0]}')
cur.execute("SELECT COUNT(*) FROM orders WHERE regiao IS NOT NULL")
print(f'Orders com regiao: {cur.fetchone()[0]}')

# Amostra
cur.execute("""
    SELECT o.external_id, o.recipient_name, o.codparc, o.lat, o.lng, o.regiao
    FROM orders o WHERE o.lat IS NOT NULL LIMIT 5
""")
for r in cur.fetchall():
    print(f'  {r[0]} | {str(r[1])[:25]} | codparc={r[2]} | lat={round(r[3],4) if r[3] else None} | regiao={r[5]}')

conn.commit()
conn.close()
print('\nPronto! Ctrl+Shift+R e abra Roteirização.')
