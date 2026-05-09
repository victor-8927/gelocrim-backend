caminho = r"C:\fleet-cloud\app\routers\orders.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

# Remover a duplicata de codparc e tempo_entrega
antigo = """               o.codparc, COALESCE(c.tempo_entrega, '') AS tempo_entrega,
               o.codparc,
               COALESCE(c.tempo_entrega, '') AS tempo_entrega"""

novo = """               o.codparc,
               COALESCE(c.tempo_entrega, '') AS tempo_entrega"""

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - duplicata removida!")
else:
    print("Trecho nao encontrado")
