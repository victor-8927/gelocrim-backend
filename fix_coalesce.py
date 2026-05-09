PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

OLD = """                    db.execute(text(\"\"\"
                        UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
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

NEW = """                    db.execute(text(\"\"\"
                        UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,
                        regiao=:regiao, updated_at=CURRENT_TIMESTAMP,
                        total_value=COALESCE(:total_value, total_value),
                        order_type=COALESCE(:order_type, order_type)
                        WHERE external_id=:eid
                    \"\"\"), {
                        \"kg\": float(p.weight_kg),
                        \"nome\": str(p.recipient_name),
                        \"codparc\": p.codparc,
                        \"lat\": lat, \"lng\": lng,
                        \"addr\": str(address),
                        \"regiao\": str(regiao),
                        \"total_value\": float(p.total_value) if p.total_value else None,
                        \"order_type\": str(p.order_type or p.top_app) if (p.order_type or p.top_app) else None,
                        \"eid\": str(p.external_id)
                    })"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK! UPDATE corrigido - nao apaga total_value existente!")
else:
    print("AVISO: bloco nao encontrado - tentando alternativa...")
    content = content.replace(
        "regiao=:regiao, total_value=:total_value,\n                        order_type=:order_type, updated_at=CURRENT_TIMESTAMP",
        "regiao=:regiao, updated_at=CURRENT_TIMESTAMP,\n                        total_value=COALESCE(:total_value, total_value),\n                        order_type=COALESCE(:order_type, order_type)"
    )
    print("OK! Corrigido via alternativa!")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reinicie o backend!")
