caminho = r"C:\fleet-cloud\app\routers\orders.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

# Remover o fallback - buscar apenas por nunota
antigo = """    # Fallback: se nao achar por nunota, busca por codparc + data
    if not itens:
        itens = db.execute(text(\"\"\"
            SELECT top_app, item_tipo, item_nome, qtd, peso_unit,
                   qtd * peso_unit as peso_total
            FROM order_items
            WHERE codparc = :cp AND dt_neg = :dt
            ORDER BY top_app, item_tipo
        \"\"\"), {\"cp\": result[\"codparc\"], \"dt\": (result.get(\"delivery_date\") or \"\")[:10]}).fetchall()"""

if antigo in data:
    data = data.replace(antigo, "")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - fallback removido!")
else:
    print("Trecho nao encontrado - verificando...")
    idx = data.find("Fallback")
    if idx >= 0:
        print(data[idx:idx+300])
    else:
        print("Fallback nao existe mais no arquivo")
