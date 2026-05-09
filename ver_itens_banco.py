import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT * FROM itens_producao")
rows = cur.fetchall()
print(f'Total itens: {len(rows)}')
for r in rows:
    print(f'  id={r["id"][:8]} nome={r["nome"]} peso={r["peso"]} comp={r["comprimento"]} larg={r["largura"]} alt={r["altura"]}')
conn.close()
