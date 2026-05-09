caminho = r"C:\fleet-cloud\app\routers\orders.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

antigo = """    priority: Optional[int] = 1
    model_config ="""

novo = """    priority: Optional[int] = 1
    codparc: Optional[int] = None
    tempo_entrega: Optional[str] = None
    model_config ="""

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - tempo_entrega adicionado no OrderOut!")
else:
    print("Trecho nao encontrado")
