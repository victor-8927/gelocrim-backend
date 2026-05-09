import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = conn.cursor()

# Atualizar coords dos pedidos baseado na tabela clientes
cur.execute("""
    UPDATE orders SET
        lat = (SELECT c.lat FROM clientes c WHERE c.codparc = orders.codparc),
        lng = (SELECT c.lng FROM clientes c WHERE c.codparc = orders.codparc)
    WHERE status = 'pending'
    AND codparc IS NOT NULL
    AND (lat IS NULL OR lat = 0)
""")
print(f"Pedidos atualizados com GPS: {cur.rowcount}")

# Verificar quantos ainda sem GPS
cur.execute("SELECT COUNT(*) FROM orders WHERE status='pending' AND (lat IS NULL OR lat=0)")
print(f"Ainda sem GPS: {cur.fetchone()[0]}")

conn.commit()
conn.close()
