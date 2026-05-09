orders_path = r'C:\fleet-cloud\app\routers\orders.py'

with open(orders_path, 'r') as f:
    content = f.read()

# Adiciona codparc na lista de colunas do POST
old_cols = '''        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end"]'''

new_cols = '''        cols = ["external_id","recipient_name","address","weight_kg","volume_m3",
                "total_value","order_type","delivery_date","regiao","status","priority",
                "lat","lng","time_window_start","time_window_end","codparc"]'''

if old_cols in content:
    content = content.replace(old_cols, new_cols)
    print('Coluna codparc adicionada no POST!')
else:
    print('Padrão não encontrado')

# Também adiciona codparc no INSERT do orders
old_insert = '''"INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts)"'''

new_insert = '''"INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at,recipient_name,address,"
            "time_window_start,time_window_end,codparc) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts,"
            ":rname,:addr,:tws,:twe,:codparc)"'''

# Atualiza o dict de params também
old_params = '''        }, {
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

new_params = '''        }, {
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
            "rname":  order.get("recipient_name"),
            "addr":   order.get("address"),
            "codparc": order.get("codparc"),
        })'''

if old_params in content:
    content = content.replace(old_params, new_params)
    print('Params do INSERT atualizados!')

with open(orders_path, 'w') as f:
    f.write(content)

print('orders.py salvo!')
