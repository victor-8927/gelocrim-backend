import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Ver todos os veículos
cur.execute("SELECT id, vda, plate, model, status, created_at FROM vehicles ORDER BY plate, created_at")
rows = cur.fetchall()
print(f'Total veículos: {len(rows)}')
for r in rows:
    print(f'  {r["id"][:8]} | vda={r["vda"]} | plate={r["plate"]} | model={r["model"][:20]} | status={r["status"]}')

# Remove duplicatas — mantém o mais recente por placa
cur.execute("""
    DELETE FROM vehicles WHERE id NOT IN (
        SELECT id FROM vehicles v1
        WHERE created_at = (
            SELECT MAX(created_at) FROM vehicles v2 WHERE v2.plate = v1.plate
        )
    )
""")
print(f'\nDuplicatas removidas: {cur.rowcount}')

# Verifica resultado
cur.execute("SELECT id, vda, plate, model, status FROM vehicles ORDER BY plate")
rows = cur.fetchall()
print(f'Veículos restantes: {len(rows)}')
for r in rows:
    print(f'  {r["id"][:8]} | vda={r["vda"]} | plate={r["plate"]} | status={r["status"]}')

conn.commit()
conn.close()
print('\nPronto!')
