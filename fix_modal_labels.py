caminho = r"C:\fleet-cloud\gelocrim_v1.html"
with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# 1. Corrigir label VALOR VENDA no modal
antigo1 = """          '<div style="font-size:10px;color:#90afd4;margin-bottom:4px">VALOR VENDA</div>' +
          '<div style="font-size:18px;font-weight:700;color:#00d4aa">' + valor + '</div>' +"""

novo1 = """          '<div style="font-size:10px;color:#90afd4;margin-bottom:4px">' + ({'1000':'VALOR VENDA','1009':'VALOR TROCA','1007':'VALOR BONIF.','1010':'VALOR PRE-PED.','1008':'VALOR CONSIG.'}[o.order_type||'']||'VALOR') + '</div>' +
          '<div style="font-size:18px;font-weight:700;color:' + (o.order_type==='1000'?'#00d4aa':'#f59e0b') + '">' + valor + '</div>' +"""

if antigo1 in data:
    data = data.replace(antigo1, novo1)
    print("OK1 - label VALOR VENDA corrigido!")
else:
    print("ERRO1 - nao encontrado")

# 2. Corrigir label VENDA (campo do meio)
antigo2 = """'<div style="font-size:10px;color:#90afd4;margin-bottom:4px">VENDA</div>' +"""
novo2 = """'<div style="font-size:10px;color:#90afd4;margin-bottom:4px">' + (o.order_type==='1000'?'VENDA':'ENTREGA') + '</div>' +"""

if antigo2 in data:
    data = data.replace(antigo2, novo2)
    print("OK2 - label VENDA corrigido!")
else:
    print("ERRO2 - label VENDA nao encontrado")
    idx = data.find("VENDA</div>")
    if idx >= 0:
        print(repr(data[max(0,idx-100):idx+100]))

with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("Salvo!")
