import sqlite3
c = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = c.cursor()

print('=== TABELAS NO BANCO ===')
for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall():
    print(' ', r[0])

print()
print('=== PROCURANDO TABELAS COM PESO/PRODUTO ===')
for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    tbl = r[0]
    cols = [c[1] for c in cur.execute(f'PRAGMA table_info({tbl})').fetchall()]
    if any(x in str(cols).lower() for x in ['peso', 'produto', 'item']):
        print(f'\nTabela: {tbl}')
        print(f'Colunas: {cols}')
        try:
            rows = cur.execute(f'SELECT * FROM {tbl} LIMIT 3').fetchall()
            for r in rows:
                print(' ', r)
        except: pass
c.close()
