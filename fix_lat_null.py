import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)

# Verifica estrutura atual
print('=== TABELA ORDERS ===')
rows = conn.execute("SELECT sql FROM sqlite_master WHERE name='orders'").fetchone()
print(rows[0])

conn.close()
