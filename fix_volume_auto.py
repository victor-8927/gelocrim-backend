PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

OLD = "    db.commit()\n    return {\"importados\": importados, \"atualizados\": atualizados}"

NEW = """    db.commit()

    # Calcular volume automaticamente
    VOLUMES = {'370': 0.01338, '371': 0.02077, '372': 0.04901, '373': 0.07517}
    try:
        peds = db.execute(text("SELECT id, codparc FROM orders WHERE status='pending'")).fetchall()
        for oid, codparc in peds:
            if not codparc: continue
            its = db.execute(text("SELECT item_tipo, qtd FROM order_items WHERE codparc=:cp AND dt_neg=(SELECT MAX(dt_neg) FROM order_items WHERE codparc=:cp)"), {"cp": codparc}).fetchall()
            vol = sum(VOLUMES.get(str(t), 0) * int(q or 0) for t, q in its)
            if vol > 0:
                db.execute(text("UPDATE orders SET volume_m3=:v WHERE id=:i"), {"v": round(vol, 3), "i": oid})
        db.commit()
    except Exception as e:
        print(f"Aviso volume: {e}")

    return {"importados": importados, "atualizados": atualizados}"""

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print("OK! Volume automatico adicionado!")
else:
    print("AVISO: bloco nao encontrado")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reinicie o backend!")
