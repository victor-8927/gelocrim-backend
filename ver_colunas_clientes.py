import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Mostra primeiros 3 registros com todos os campos
cur.execute("SELECT * FROM clientes LIMIT 3")
rows = cur.fetchall()
for row in rows:
    print('\n--- Parceiro ---')
    for key in row.keys():
        print(f'  {key}: {repr(row[key])}')

conn.close()
