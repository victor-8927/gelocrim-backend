caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

idx = data.find("async function editarVeiculo")
print(data[idx:idx+1500])
