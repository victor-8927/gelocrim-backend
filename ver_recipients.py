import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("PRAGMA table_info(recipients)")
cols = [c[1] for c in cur.fetchall()]
print('Colunas recipients:', cols)
cur.execute("SELECT * FROM recipients LIMIT 5")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()
