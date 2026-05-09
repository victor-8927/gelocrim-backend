import re

PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

# Encontrar e corrigir o INSERT INTO orders para incluir total_value e order_type
# e fazer UPDATE quando o pedido ja existe

OLD_INSERT = '''INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts)"'''

NEW_INSERT = '''INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,"
            "weight_kg,volume_m3,tw_start,tw_end,notes,status,priority,"
            "delivery_date,created_at,updated_at,total_value,order_type,"
            "recipient_name,address,regiao,codparc) "
            "VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:status,:priority,:ddate,:ts,:ts,:total_value,:order_type,:recipient_name,:address,:regiao,:codparc) "
            "ON CONFLICT(external_id) DO UPDATE SET "
            "total_value=excluded.total_value, "
            "order_type=excluded.order_type, "
            "weight_kg=excluded.weight_kg, "
            "recipient_name=excluded.recipient_name, "
            "address=excluded.address, "
            "regiao=excluded.regiao, "
            "updated_at=excluded.updated_at"'''

if OLD_INSERT in content:
    content = content.replace(OLD_INSERT, NEW_INSERT)
    print("OK: INSERT corrigido com total_value e ON CONFLICT UPDATE")
else:
    print("AVISO: INSERT nao encontrado exatamente")
    # Mostrar o que existe
    m = re.search(r'INSERT INTO orders.*?VALUES.*?\)', content, re.DOTALL)
    if m:
        print("Encontrado:", m.group()[:200])

# Adicionar os novos parametros no dict do execute
OLD_PARAMS = '''"id":     oid,
            "ext":    ext_id,
            "src":    "sankhya",
            "rid":    rid,
            "lat":    lat,
            "lng":    lng,
            "kg":     order.get("weight_kg", 0),
            "m3":     order.get("volume_m3", 0),'''

NEW_PARAMS = '''"id":     oid,
            "ext":    ext_id,
            "src":    "sankhya",
            "rid":    rid,
            "lat":    lat,
            "lng":    lng,
            "kg":     order.get("weight_kg", 0),
            "m3":     order.get("volume_m3", 0),
            "total_value":    order.get("total_value") or order.get("value"),
            "order_type":     order.get("order_type") or order.get("top"),
            "recipient_name": order.get("recipient_name") or name,
            "address":        order.get("address") or addr,
            "regiao":         order.get("regiao"),
            "codparc":        order.get("codparc"),'''

if OLD_PARAMS in content:
    content = content.replace(OLD_PARAMS, NEW_PARAMS)
    print("OK: Parametros do execute corrigidos")
else:
    print("AVISO: Parametros nao encontrados exatamente")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nReinicie o backend e reimporte o arquivo!")
