import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Ver o que tem na tabela recipients que corresponde aos orders
# Orders têm recipient_id como UUID — precisa ver a tabela que liga UUID ao nome
cur.execute("SELECT id, name, lat, lng FROM recipients WHERE id = 'b6700daf-000f-4cc6-a2e4-64c24b3c592a'")
r = cur.fetchone()
print(f'Recipient UUID: {r}')

# Busca todos recipients com UUID
cur.execute("SELECT COUNT(*) FROM recipients WHERE id NOT LIKE 'SNK-CLI-%'")
print(f'Recipients com UUID: {cur.fetchone()[0]}')

cur.execute("SELECT id, name, lat, lng FROM recipients WHERE id NOT LIKE 'SNK-CLI-%' LIMIT 5")
for r in cur.fetchall():
    print(f'  {r[0][:8]} | {str(r[1])[:30]} | lat={r[2]} | lng={r[3]}')

conn.close()
