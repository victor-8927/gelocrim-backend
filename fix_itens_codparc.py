PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

OLD = """    # Buscar itens da nota especifica (por nunota)
    itens = db.execute(text(\"\"\"
        SELECT top_app, item_tipo, item_nome, qtd, peso_unit,
               qtd * peso_unit as peso_total
        FROM order_items
        WHERE nunota = :nunota
        ORDER BY top_app, item_tipo
    \"\"\"), {"nunota": result["external_id"]}).fetchall()"""

NEW = """    # Buscar itens por codparc (nunota pode ser null)
    itens = db.execute(text(\"\"\"
        SELECT top_app, item_tipo, item_nome, qtd, peso_unit,
               qtd * peso_unit as peso_total
        FROM order_items
        WHERE codparc = :codparc
        AND dt_neg = (SELECT MAX(dt_neg) FROM order_items WHERE codparc = :codparc)
        ORDER BY top_app, item_tipo
    \"\"\"), {"codparc": result["codparc"]}).fetchall()"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK! Busca de itens corrigida para usar codparc!")
else:
    print("AVISO: bloco nao encontrado")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reinicie o backend!")
