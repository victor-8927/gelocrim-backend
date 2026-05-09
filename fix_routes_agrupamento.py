path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a secao de montagem das deliveries no optimize
old_deliveries = '''    deliveries = [
        Delivery(
            id=str(o["id"]), lat=float(o["lat"]), lng=float(o["lng"]),
            weight_kg=float(o["weight_kg"]), volume_m3=float(o["volume_m3"]),
            tw_start=_min(o["tw_start"]), tw_end=_min(o["tw_end"])
        )
        for o in raw_o
    ]'''

new_deliveries = '''    # Agrupa pedidos por cliente (mesmo recipient_id = mesma parada)
    from collections import defaultdict
    grupos = defaultdict(list)
    for o in raw_o:
        grupos[str(o["recipient_id"])].append(o)

    # Mapa de recipient_id -> pedidos agrupados
    grupos_list = []
    for rec_id, pedidos in grupos.items():
        peso_total = sum(float(p["weight_kg"] or 0) for p in pedidos)
        vol_total  = sum(float(p["volume_m3"] or 0) for p in pedidos)
        # Tempo: 10 min base + 5 min por pedido adicional
        service_min = 10 + (len(pedidos) - 1) * 5
        # Usa o primeiro pedido como referencia de coordenadas e janela
        ref = pedidos[0]
        # ID do grupo = recipient_id (para identificar na parada)
        grupos_list.append({
            "group_id": rec_id,
            "order_ids": [str(p["id"]) for p in pedidos],
            "lat": float(ref["lat"] or -3.1019),
            "lng": float(ref["lng"] or -60.0250),
            "weight_kg": peso_total,
            "volume_m3": vol_total,
            "tw_start": ref["tw_start"],
            "tw_end": ref["tw_end"],
            "service_min": service_min,
            "pedidos": pedidos,
        })

    deliveries = [
        Delivery(
            id=g["group_id"],
            lat=g["lat"], lng=g["lng"],
            weight_kg=g["weight_kg"], volume_m3=g["volume_m3"],
            tw_start=_min(g["tw_start"]), tw_end=_min(g["tw_end"]),
            service_minutes=g["service_min"]
        )
        for g in grupos_list
    ]

    # Mapa group_id -> grupo para usar na criacao das paradas
    grupos_map = {g["group_id"]: g for g in grupos_list}'''

content = content.replace(old_deliveries, new_deliveries)

# Corrige o mapa om para usar grupos
old_om = '''    om = {str(o["id"]): o for o in raw_o}'''
new_om = '''    om = {str(o["id"]): o for o in raw_o}
    # grupos_map ja foi criado acima'''

content = content.replace(old_om, new_om)

# Corrige a criacao das stops para usar grupos
old_stops = '''        stops_out = []
        for stop in r.stops:
            sid = str(uuid4())
            o = om[stop.delivery_id]
            db.execute(text("""
                INSERT INTO stops (id,route_id,order_id,sequence,lat,lng,eta,status,created_at,updated_at)
                VALUES (:id,:rid,:oid,:seq,:lat,:lng,:eta,\'pending\',:ts,:ts)
            """), {"id": sid, "rid": rid, "oid": str(o["id"]), "seq": stop.sequence,
                   "lat": o["lat"], "lng": o["lng"], "eta": _hhmm(stop.arrival_min), "ts": ts})
            db.execute(
                text("UPDATE orders SET status=\'routed\', updated_at=:ts WHERE id=:id"),
                {"ts": ts, "id": str(o["id"])}
            )
            stops_out.append({
                "stop_id": sid, "order_id": str(o["id"]),
                "sequence": stop.sequence, "eta": _hhmm(stop.arrival_min),
                "address": o["address"], "recipient_name": o["recipient_name"],
                "weight_kg": o["weight_kg"]
            })'''

new_stops = '''        stops_out = []
        for stop in r.stops:
            # stop.delivery_id é o group_id (recipient_id)
            grupo = grupos_map.get(stop.delivery_id)
            if not grupo:
                continue

            # Cria uma stop para cada pedido do grupo
            for i, order_id in enumerate(grupo["order_ids"]):
                o = om.get(order_id)
                if not o:
                    continue
                sid = str(uuid4())
                db.execute(text("""
                    INSERT INTO stops (id,route_id,order_id,sequence,lat,lng,eta,status,created_at,updated_at)
                    VALUES (:id,:rid,:oid,:seq,:lat,:lng,:eta,\'pending\',:ts,:ts)
                """), {"id": sid, "rid": rid, "oid": str(o["id"]),
                       "seq": stop.sequence,
                       "lat": o["lat"], "lng": o["lng"],
                       "eta": _hhmm(stop.arrival_min), "ts": ts})
                db.execute(
                    text("UPDATE orders SET status=\'routed\', updated_at=:ts WHERE id=:id"),
                    {"ts": ts, "id": str(o["id"])}
                )

            # Monta o TOP label
            top_map = {"1000": "Venda", "1009": "Troca", "1007": "Bonif"}
            pedidos_info = []
            for p in grupo["pedidos"]:
                top_raw = str(p.get("top","") or "")
                top_label = top_map.get(top_raw, f"TOP {top_raw}")
                pedidos_info.append(f"{top_label}: {float(p.get('weight_kg',0) or 0):.0f}kg")

            ref_o = om.get(grupo["order_ids"][0])
            stops_out.append({
                "stop_id": str(uuid4()),
                "order_id": grupo["order_ids"][0],
                "order_ids": grupo["order_ids"],
                "sequence": stop.sequence,
                "eta": _hhmm(stop.arrival_min),
                "address": ref_o["address"] if ref_o else "",
                "recipient_name": ref_o["recipient_name"] if ref_o else "",
                "weight_kg": grupo["weight_kg"],
                "num_pedidos": len(grupo["order_ids"]),
                "pedidos_info": " | ".join(pedidos_info),
            })'''

content = content.replace(old_stops, new_stops)

# Corrige o total_stops para contar clientes (grupos), nao pedidos
old_total = '''            "total_stops": len(r.stops),'''
new_total = '''            "total_stops": len(stops_out),'''
content = content.replace(old_total, new_total)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('routes.py corrigido - 1 parada por cliente!')
