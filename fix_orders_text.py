orders_path = r'C:\fleet-cloud\app\routers\orders.py'

with open(orders_path, 'r') as f:
    content = f.read()

# Garante que text está importado
if 'from sqlalchemy' in content and 'text' not in content:
    content = content.replace('from sqlalchemy', 'from sqlalchemy.sql import text\nfrom sqlalchemy')
elif 'from sqlalchemy.sql import text' not in content and 'from sqlalchemy import' in content:
    content = content.replace('from sqlalchemy import', 'from sqlalchemy.sql import text\nfrom sqlalchemy import')

print('Imports verificados!')

# Substitui o POST para usar text()
import re

new_post = '''@router.post("", status_code=201)
def create_order(order: dict = Body(...), db = Depends(get_db)):
    import traceback
    try:
        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]
        vals = {c: order.get(c) for c in cols}
        sql = text(
            "INSERT INTO orders (" + ",".join(cols) + ") VALUES (" +
            ",".join([":" + c for c in cols]) + ")"
        )
        result = db.execute(sql, vals)
        db.commit()
        return {"id": result.lastrowid, "external_id": order.get("external_id"), "status": "created"}
    except Exception as e:
        print("ERRO POST /orders:", traceback.format_exc())
        raise

'''

content = re.sub(
    r'@router\.post\("", status_code=201\).*?(?=@router\.post\("/batch"\))',
    new_post,
    content,
    flags=re.DOTALL
)

with open(orders_path, 'w') as f:
    f.write(content)

print('POST /orders corrigido com text()!')
print('Reinicie o servidor!')
