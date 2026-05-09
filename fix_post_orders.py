PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

OLD = '''        db.execute(text(
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
        })'''

NEW = '''        # Verificar se pedido ja existe e atualizar
        existente = db.execute(text(
            "SELECT id FROM orders WHERE external_id=:ext"
        ), {"ext": ext_id}).fetchone()

        if existente:
            db.execute(text(
                "UPDATE orders SET total_value=:tv, order_type=:ot, "
                "weight_kg=:kg, recipient_name=:rname, address=:addr, "
                "regiao=:regiao, codparc=:codparc, updated_at=:ts "
                "WHERE external_id=:ext"
            ), {
                "tv":      order.get("total_value"),
                "ot":      order.get("order_type") or order.get("notes"),
                "kg":      order.get("weight_kg", 0),
                "rname":   order.get("recipient_name") or name,
                "addr":    order.get("address") or addr,
                "regiao":  order.get("regiao"),
                "codparc": order.get("codparc"),
                "ts":      ts,
                "ext":     ext_id,
            })
            db.commit()
            return {"id": existente[0], "external_id": ext_id, "status": "updated"}

        db.execute(text(
            "INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at,total_value,order_type,"
            "recipient_name,address,regiao,codparc) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts,:tv,:ot,:rname,:addr,:regiao,:codparc)"
        ), {
            "id":      oid,
            "ext":     ext_id,
            "src":     "sankhya",
            "rid":     rid,
            "lat":     lat,
            "lng":     lng,
            "kg":      order.get("weight_kg", 0),
            "m3":      order.get("volume_m3", 0),
            "tws":     order.get("time_window_start", "07:30"),
            "twe":     order.get("time_window_end", "18:00"),
            "notes":   order.get("order_type") or order.get("notes"),
            "status":  order.get("status", "pending"),
            "priority":order.get("priority", 1),
            "ddate":   order.get("delivery_date"),
            "ts":      ts,
            "tv":      order.get("total_value"),
            "ot":      order.get("order_type") or order.get("notes"),
            "rname":   order.get("recipient_name") or name,
            "addr":    order.get("address") or addr,
            "regiao":  order.get("regiao"),
            "codparc": order.get("codparc"),
        })'''

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK! Endpoint POST /orders corrigido!")
else:
    print("AVISO: bloco nao encontrado exatamente")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reinicie o backend e reimporte!")
