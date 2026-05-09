caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

antigo = "<th>Janela / Prioridade</th>"
novo   = "<th>T. ATEND.</th>"

if antigo in data:
    data = data.replace(antigo, novo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - header renomeado!")
else:
    print("Nao encontrado")
