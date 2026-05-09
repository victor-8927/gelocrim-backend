"""
CORRECAO: Bug dos stops None/0kg no routes.py
Execute: python fix_stops_none.py
"""
import re

caminho = r"C:\fleet-cloud\app\routers\routes.py"

with open(caminho, encoding="utf-8") as f:
    conteudo = f.read()

# Trecho antigo (bugado)
antigo = '''    orders = []
    for oid in body.order_ids:
        o = db.execute(text("SELECT * FROM orders WHERE id = :id"),{"id":oid}).mappings().fetchone()
        if o: orders.append(dict(o))

    clientes = {}
    for o in orders:
        key = o.get("codparc") or o.get("recipient_name") or o["id"]
        if key not in clientes:
            clientes[key] = {"codparc":o.get("codparc"),"recipient_name":o.get("recipient_name",""),
                "address":o.get("address",""),"lat":o.get("lat"),"lng":o.get("lng"),
                "weight_kg":0,"order_ids":[]}
        clientes[key]["weight_kg"] += float(o.get("weight_kg") or 0)
        clientes[key]["order_ids"].append(o["id"])

    for i, (key, cli) in enumerate(clientes.items()):
        stop_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO route_stops
                (stop_id,route_id,order_id,sequence,recipient_name,address,
                 lat,lng,weight_kg,status,codparc)
            VALUES (:sid,:rid,:oid,:seq,:name,:addr,:lat,:lng,:kg,"pending",:cp)
        """), {"sid":stop_id,"rid":route_id,"oid":cli["order_ids"][0],"seq":i,
               "name":cli["recipient_name"],"addr":cli["address"],
               "lat":cli["lat"],"lng":cli["lng"],"kg":cli["weight_kg"],"cp":cli["codparc"]})
        for oid in cli["order_ids"]:
            db.execute(text("UPDATE orders SET status='routed' WHERE id=:id"),{"id":oid})

    db.commit()
    return {"route_id":route_id,"trip_number":trip_number,"status":"optimized","total_stops":len(clientes)}'''

# Trecho novo (corrigido)
novo = '''    orders = []
    for oid in body.order_ids:
        o = db.execute(text("SELECT * FROM orders WHERE id = :id"),{"id":oid}).mappings().fetchone()
        if o: orders.append(dict(o))

    # CORRIGIDO: agrupar por CODPARC somando peso de todos os pedidos do mesmo cliente
    clientes = {}
    for o in orders:
        codparc = o.get("codparc")
        nome    = o.get("recipient_name") or ""
        addr    = o.get("address") or ""
        lat     = o.get("lat")
        lng     = o.get("lng")

        # Chave primaria: CODPARC. Fallback: nome. Fallback final: id unico
        key = codparc if codparc else (nome.strip() if nome.strip() else o["id"])

        if key not in clientes:
            clientes[key] = {
                "codparc": codparc,
                "recipient_name": nome,
                "address": addr,
                "lat": lat,
                "lng": lng,
                "weight_kg": 0,
                "order_ids": []
            }
        else:
            # Preencher campos vazios com dados de outros pedidos do mesmo cliente
            if not clientes[key]["recipient_name"] and nome:
                clientes[key]["recipient_name"] = nome
            if not clientes[key]["address"] and addr:
                clientes[key]["address"] = addr
            if not clientes[key]["lat"] and lat:
                clientes[key]["lat"] = lat
            if not clientes[key]["lng"] and lng:
                clientes[key]["lng"] = lng

        clientes[key]["weight_kg"] += float(o.get("weight_kg") or 0)
        clientes[key]["order_ids"].append(o["id"])

    # Filtrar entradas sem nome e sem codparc (pedidos com dados incompletos)
    clientes_validos = {
        k: v for k, v in clientes.items()
        if v["recipient_name"] or v["codparc"]
    }

    for i, (key, cli) in enumerate(clientes_validos.items()):
        stop_id = str(uuid.uuid4())
        db.execute(text("""
            INSERT INTO route_stops
                (stop_id,route_id,order_id,sequence,recipient_name,address,
                 lat,lng,weight_kg,status,codparc)
            VALUES (:sid,:rid,:oid,:seq,:name,:addr,:lat,:lng,:kg,"pending",:cp)
        """), {"sid":stop_id,"rid":route_id,"oid":cli["order_ids"][0],"seq":i,
               "name":cli["recipient_name"],"addr":cli["address"],
               "lat":cli["lat"],"lng":cli["lng"],"kg":cli["weight_kg"],"cp":cli["codparc"]})
        for oid in cli["order_ids"]:
            db.execute(text("UPDATE orders SET status='routed' WHERE id=:id"),{"id":oid})

    db.commit()
    return {"route_id":route_id,"trip_number":trip_number,"status":"optimized","total_stops":len(clientes_validos)}'''

if antigo in conteudo:
    novo_conteudo = conteudo.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(novo_conteudo)
    print("✅ CORRIGIDO com sucesso!")
    print("   - Stops None/0kg eliminados")
    print("   - Agrupamento por CODPARC corrigido")
    print("   - Campos vazios preenchidos automaticamente")
    print()
    print("Reinicie o servidor para aplicar:")
    print("   Ctrl+C no terminal do backend")
    print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
else:
    print("⚠️  Trecho original não encontrado.")
    print("   O arquivo pode ter sido modificado anteriormente.")
    print()
    print("Substitua manualmente o bloco 'clientes = {}' no routes.py")
    print("pelo código corrigido acima.")
