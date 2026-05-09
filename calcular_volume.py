import sys
sys.path.insert(0, r'C:\fleet-cloud')
from app.database import engine_sync
from sqlalchemy import text

# Volume real por tipo de item (comp x larg x alt)
VOLUMES = {
    '370': 0.38 * 0.32 * 0.11,   # Gelo 5kg  = 0.01338 m3
    '371': 0.55 * 0.32 * 0.118,  # Gelo 10kg = 0.02074 m3
    '372': 0.66 * 0.45 * 0.165,  # Gelo 20kg = 0.04901 m3
    '373': 0.87 * 0.48 * 0.18,   # Gelo 40kg = 0.07517 m3
}

print("Volumes por item:")
for cod, vol in VOLUMES.items():
    print(f"  Tipo {cod}: {vol:.5f} m³ por unidade")

with engine_sync.connect() as conn:
    # Buscar todos os pedidos pending com seus itens
    pedidos = conn.execute(text(
        "SELECT DISTINCT o.id, o.codparc FROM orders o WHERE o.status='pending'"
    )).fetchall()

    updated = 0
    for ped in pedidos:
        order_id, codparc = ped[0], ped[1]
        if not codparc:
            continue

        # Buscar itens do pedido
        itens = conn.execute(text("""
            SELECT item_tipo, qtd FROM order_items
            WHERE codparc = :cp
            AND dt_neg = (SELECT MAX(dt_neg) FROM order_items WHERE codparc = :cp)
        """), {"cp": codparc}).fetchall()

        volume_total = 0
        for item in itens:
            tipo, qtd = str(item[0]), int(item[1] or 0)
            vol_unit = VOLUMES.get(tipo, 0)
            volume_total += vol_unit * qtd

        if volume_total > 0:
            conn.execute(text(
                "UPDATE orders SET volume_m3=:vol WHERE id=:id"
            ), {"vol": round(volume_total, 3), "id": order_id})
            updated += 1

    conn.commit()
    print(f"\nOK! {updated} pedidos com volume calculado!")

    # Verificar resultado
    r = conn.execute(text(
        "SELECT SUM(volume_m3), AVG(volume_m3), MAX(volume_m3) FROM orders WHERE status='pending'"
    )).fetchone()
    print(f"Volume total: {r[0]:.2f} m³")
    print(f"Volume médio: {r[1]:.3f} m³")
    print(f"Volume máximo: {r[2]:.3f} m³")
