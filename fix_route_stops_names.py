import sqlite3

conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = conn.cursor()

# Ver nome atual no banco de clientes para cod 3908
r = cur.execute("SELECT codparc, nome FROM clientes WHERE codparc=3908").fetchone()
print(f"Cliente 3908 no banco: {r}")

# Forcar atualizacao de todos os stops com nome do banco de clientes
cur.execute("""
    UPDATE route_stops
    SET recipient_name = (
        SELECT c.nome FROM clientes c
        WHERE c.codparc = route_stops.codparc
    )
    WHERE codparc IS NOT NULL
""")
print(f"Stops atualizados: {cur.rowcount}")

# Verificar resultado
cur.execute("""
    SELECT rs.sequence, rs.recipient_name, rs.codparc
    FROM routes r 
    JOIN route_stops rs ON rs.route_id = r.id
    WHERE r.trip_number = 'VGM-260504-001'
    ORDER BY rs.sequence
""")
print("\nStops atualizados:")
for r in cur.fetchall():
    print(f"  Seq {r[0]}: {r[1]} (cod:{r[2]})")

conn.commit()
conn.close()
