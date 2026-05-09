caminho = r"C:\fleet-cloud\gelocrim_v1.html"

with open(caminho, encoding="utf-8", errors="ignore") as f:
    data = f.read()

# Corrigir as aspas quebradas nos botoes
antigo1 = """'<button class="btn btn-secondary" onclick="document.getElementById('modal-pedido-detalhe').style.display='none'">Fechar</button>' +
        '<button class="btn btn-primary" onclick="document.getElementById('modal-pedido-detalhe').style.display='none';goTo('roteirizacao',null)">+ Roteirizar</button>' +"""

novo1 = """'<button class="btn btn-secondary" onclick="document.getElementById(\\'modal-pedido-detalhe\\').style.display=\\'none\\'">Fechar</button>' +
        '<button class="btn btn-primary" onclick="document.getElementById(\\'modal-pedido-detalhe\\').style.display=\\'none\\';goTo(\\'roteirizacao\\',null)">+ Roteirizar</button>' +"""

if antigo1 in data:
    data = data.replace(antigo1, novo1)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - aspas corrigidas!")
else:
    print("Trecho nao encontrado. Tentando alternativa...")
    # Mostrar o trecho para analise
    idx = data.find("btn btn-secondary.*modal-pedido-detalhe")
    idx2 = data.find("Fechar</button>' +")
    if idx2 > 0:
        print(repr(data[idx2-200:idx2+300]))
