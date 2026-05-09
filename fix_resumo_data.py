caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Buscar o trecho atual da funcao atualizarResumoQuantidades
idx = data.find("atualizarResumoQuantidades")
print("Trecho atual:")
print(data[idx:idx+400])
