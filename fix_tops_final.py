import sys
sys.path.insert(0, r'C:\fleet-cloud')
from app.database import engine_sync
from sqlalchemy import text

with engine_sync.connect() as conn:
    conn.execute(text("UPDATE orders SET order_type='1009' WHERE external_id IN ('231210','231129','231120','231049','230992','230966','230767','230670')"))
    conn.execute(text("UPDATE orders SET order_type='1010' WHERE external_id IN ('231195','230663')"))
    conn.execute(text("UPDATE orders SET order_type='1007' WHERE external_id IN ('230887')"))
    conn.commit()

    r = conn.execute(text("SELECT order_type, COUNT(*) as qtd FROM orders WHERE status='pending' GROUP BY order_type"))
    labels = {'1000':'Venda','1009':'Troca','1007':'Bonif.','1010':'Pre-ped.'}
    for row in r:
        print(f"  {labels.get(row[0], str(row[0]))}: {row[1]} pedidos")
    print("OK!")
