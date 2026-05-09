# Testa o router diretamente
import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

# Testa a query
try:
    rows = conn.execute("""
        SELECT oi.*, c.nome as cliente_nome
        FROM order_items oi
        LEFT JOIN clientes c ON c.codparc = oi.codparc
        ORDER BY oi.item_tipo, c.nome
    """).fetchall()
    print(f'Query OK: {len(rows)} rows')
except Exception as e:
    print(f'ERRO query: {e}')

# Verifica estrutura da tabela
cur = conn.execute("PRAGMA table_info(order_items)")
cols = cur.fetchall()
print('\nColunas order_items:')
for c in cols:
    print(f'  {dict(c)}')

conn.close()
