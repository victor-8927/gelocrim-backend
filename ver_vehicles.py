import os, sqlite3

# Ver router
path = r'C:\fleet-cloud\app\routers\vehicles.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        print('=== vehicles.py ===')
        print(f.read()[:3000])

# Ver tabela
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("PRAGMA table_info(vehicles)")
cols = cur.fetchall()
print('\n=== Colunas vehicles ===')
for c in cols:
    print(f'  {c[1]} ({c[2]})')
cur.execute("SELECT * FROM vehicles LIMIT 2")
rows = cur.fetchall()
print(f'\nRegistros: {len(rows)}')
for r in rows:
    print(r)
conn.close()
