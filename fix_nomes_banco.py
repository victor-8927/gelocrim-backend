"""
Corrige nomes de clientes no banco que ficaram como CODPARC numerico
Busca o nome correto na tabela clientes
"""
import sqlite3

conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = conn.cursor()

# Buscar pedidos com nome numerico
cur.execute("""
    SELECT o.id, o.external_id, o.codparc, o.recipient_name
    FROM orders o
    WHERE o.recipient_name IS NOT NULL
    AND CAST(o.recipient_name AS TEXT) = CAST(CAST(o.recipient_name AS INTEGER) AS TEXT)
""")
problemas = cur.fetchall()
print(f'Pedidos com nome numerico: {len(problemas)}')

corrigidos = 0
for oid, ext_id, codparc, nome_ruim in problemas:
    if not codparc:
        continue
    cli = cur.execute('SELECT nome FROM clientes WHERE codparc=?', (codparc,)).fetchone()
    if cli and cli[0]:
        cur.execute('UPDATE orders SET recipient_name=? WHERE id=?', (cli[0], oid))
        print(f'  {ext_id}: {nome_ruim} -> {cli[0]}')
        corrigidos += 1

conn.commit()
conn.close()
print(f'\nCorrigidos: {corrigidos}')
