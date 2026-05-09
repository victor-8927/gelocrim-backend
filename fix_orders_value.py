PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Corrigir UPDATE para incluir total_value e order_type
OLD_UPDATE = """                        UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,
                        regiao=:regiao, updated_at=CURRENT_TIMESTAMP
                        WHERE external_id=:eid
                    \"\"\"), {
                        \"kg\": float(p.weight_kg),
                        \"nome\": str(p.recipient_name),
                        \"codparc\": p.codparc,
                        \"lat\": lat, \"lng\": lng,
                        \"addr\": str(address),
                        \"regiao\": str(regiao),
                        \"eid\": str(p.external_id)
                    })"""

NEW_UPDATE = """                        UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,
                        regiao=:regiao, total_value=:total_value,
                        order_type=:order_type, updated_at=CURRENT_TIMESTAMP
                        WHERE external_id=:eid
                    \"\"\"), {
                        \"kg\": float(p.weight_kg),
                        \"nome\": str(p.recipient_name),
                        \"codparc\": p.codparc,
                        \"lat\": lat, \"lng\": lng,
                        \"addr\": str(address),
                        \"regiao\": str(regiao),
                        \"total_value\": float(p.total_value) if p.total_value else None,
                        \"order_type\": str(p.order_type or p.top_app or '1000'),
                        \"eid\": str(p.external_id)
                    })"""

if OLD_UPDATE in content:
    content = content.replace(OLD_UPDATE, NEW_UPDATE)
    changes += 1
    print("OK: UPDATE corrigido com total_value e order_type")
else:
    print("AVISO: UPDATE nao encontrado exatamente, tentando alternativa...")
    # Substituicao mais simples
    content = content.replace(
        "UPDATE orders SET weight_kg=:kg, recipient_name=:nome,\n                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,\n                        regiao=:regiao, updated_at=CURRENT_TIMESTAMP",
        "UPDATE orders SET weight_kg=:kg, recipient_name=:nome,\n                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,\n                        regiao=:regiao, total_value=:total_value, order_type=:order_type, updated_at=CURRENT_TIMESTAMP"
    )
    content = content.replace(
        '"regiao": str(regiao),\n                        "eid": str(p.external_id)',
        '"regiao": str(regiao),\n                        "total_value": float(p.total_value) if hasattr(p,"total_value") and p.total_value else None,\n                        "order_type": str(getattr(p,"order_type",None) or getattr(p,"top_app",None) or "1000"),\n                        "eid": str(p.external_id)'
    )
    changes += 1
    print("OK: UPDATE corrigido via substituicao simples")

# 2. Corrigir INSERT para incluir total_value e order_type
OLD_INSERT = """                    INSERT INTO orders (id, external_id, codparc, recipient_name,
                        weight_kg, lat, lng, address, regiao, status, created_at)
                    VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,
                        :addr, :regiao, 'pending', CURRENT_TIMESTAMP)
                \"\"\"), {
                    \"id\": order_id,
                    \"eid\": str(p.external_id),
                    \"codparc\": p.codparc,
                    \"nome\": str(p.recipient_name),
                    \"kg\": float(p.weight_kg),
                    \"lat\": lat, \"lng\": lng,
                    \"addr\": str(address),
                    \"regiao\": str(regiao)
                })"""

NEW_INSERT = """                    INSERT INTO orders (id, external_id, codparc, recipient_name,
                        weight_kg, lat, lng, address, regiao, status,
                        total_value, order_type, created_at)
                    VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,
                        :addr, :regiao, 'pending',
                        :total_value, :order_type, CURRENT_TIMESTAMP)
                \"\"\"), {
                    \"id\": order_id,
                    \"eid\": str(p.external_id),
                    \"codparc\": p.codparc,
                    \"nome\": str(p.recipient_name),
                    \"kg\": float(p.weight_kg),
                    \"lat\": lat, \"lng\": lng,
                    \"addr\": str(address),
                    \"regiao\": str(regiao),
                    \"total_value\": float(p.total_value) if hasattr(p, \"total_value\") and p.total_value else None,
                    \"order_type\": str(getattr(p, \"order_type\", None) or getattr(p, \"top_app\", None) or \"1000\")
                })"""

if OLD_INSERT in content:
    content = content.replace(OLD_INSERT, NEW_INSERT)
    changes += 1
    print("OK: INSERT corrigido com total_value e order_type")
else:
    print("AVISO: INSERT nao encontrado exatamente, tentando alternativa...")
    content = content.replace(
        "INSERT INTO orders (id, external_id, codparc, recipient_name,\n                        weight_kg, lat, lng, address, regiao, status, created_at)\n                    VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,\n                        :addr, :regiao, 'pending', CURRENT_TIMESTAMP)",
        "INSERT INTO orders (id, external_id, codparc, recipient_name,\n                        weight_kg, lat, lng, address, regiao, status,\n                        total_value, order_type, created_at)\n                    VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,\n                        :addr, :regiao, 'pending',\n                        :total_value, :order_type, CURRENT_TIMESTAMP)"
    )
    content = content.replace(
        '"regiao": str(regiao)\n                })',
        '"regiao": str(regiao),\n                    "total_value": float(p.total_value) if hasattr(p,"total_value") and p.total_value else None,\n                    "order_type": str(getattr(p,"order_type",None) or getattr(p,"top_app",None) or "1000")\n                })'
    )
    changes += 1
    print("OK: INSERT corrigido via substituicao simples")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes} correcoes aplicadas!")
print("Reinicie o backend: Ctrl+C e rode novamente uvicorn")
