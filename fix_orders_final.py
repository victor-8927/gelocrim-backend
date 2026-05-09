orders_path = r'C:\fleet-cloud\app\routers\orders.py'

with open(orders_path, 'r') as f:
    content = f.read()

# Remove duplicate text import
content = content.replace(
    'from sqlalchemy.sql import text\nfrom sqlalchemy import text\n',
    'from sqlalchemy import text\n'
)

# Substitui o POST incorreto pelo correto
old_post = '''@router.post("", status_code=201)
def create_order(order: dict = Body(...), db: sqlite3.Connection = Depends(get_db)):
    try:
        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]
        vals = {c: order.get(c) for c in cols}
        cur = db.execute(
            f"INSERT INTO orders ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
            vals
        )
        db.commit()
        return {"id": cur.lastrowid, "external_id": order.get("external_id"), "status": "created"}
    except Exception as e:
        import traceback
        print("ERRO POST /orders:", traceback.format_exc())
        raise'''

new_post = '''@router.post("", status_code=201)
def create_order(order: dict = Body(...), db: Session = Depends(get_db)):
    import traceback
    try:
        from uuid import uuid4
        ts = now_str()

        # 1. Cria ou reutiliza recipient
        ext_id = order.get("external_id", "")
        name   = order.get("recipient_name") or order.get("nome") or "Cliente"
        addr   = order.get("address") or "Manaus - AM"
        lat    = order.get("lat")
        lng    = order.get("lng")

        rid = str(uuid4())
        db.execute(text(
            "INSERT OR IGNORE INTO recipients (id,name,address,lat,lng,created_at) "
            "VALUES (:id,:name,:addr,:lat,:lng,:ts)"
        ), {"id":rid,"name":name,"addr":addr,"lat":lat,"lng":lng,"ts":ts})

        # 2. Cria a order
        oid = str(uuid4())
        db.execute(text(
            "INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts)"
        ), {
            "id":     oid,
            "ext":    ext_id,
            "src":    "sankhya",
            "rid":    rid,
            "lat":    lat,
            "lng":    lng,
            "kg":     order.get("weight_kg", 0),
            "m3":     order.get("volume_m3", 0),
            "tws":    order.get("time_window_start", "07:30"),
            "twe":    order.get("time_window_end", "18:00"),
            "notes":  order.get("order_type") or order.get("notes"),
            "status": order.get("status", "pending"),
            "priority": order.get("priority", 1),
            "ddate":  order.get("delivery_date"),
            "ts":     ts,
        })
        db.commit()
        return {"id": oid, "external_id": ext_id, "status": "created"}
    except Exception as e:
        print("ERRO POST /orders:", traceback.format_exc())
        raise'''

if old_post in content:
    content = content.replace(old_post, new_post)
    print('POST corrigido com recipients!')
else:
    print('Padrão não encontrado — substituindo por posição...')
    import re
    content = re.sub(
        r'@router\.post\("", status_code=201\)\ndef create_order.*?(?=@router\.delete\("", status_code=200\))',
        new_post + '\n',
        content,
        flags=re.DOTALL
    )
    print('Corrigido via regex!')

# Também corrige o DELETE pending para usar SQLAlchemy
old_delete = '''@router.delete("", status_code=200)
def delete_pending_orders(db: sqlite3.Connection = Depends(get_db)):
    result = db.execute("DELETE FROM orders WHERE status='pending'")
    db.commit()
    return {"deleted": result.rowcount}'''

new_delete = '''@router.delete("", status_code=200)
def delete_pending_orders(db: Session = Depends(get_db)):
    result = db.execute(text("DELETE FROM orders WHERE status='pending'"))
    db.commit()
    return {"deleted": result.rowcount}'''

if old_delete in content:
    content = content.replace(old_delete, new_delete)
    print('DELETE pending corrigido!')

with open(orders_path, 'w') as f:
    f.write(content)

print('\nPronto! Reinicie o servidor.')
