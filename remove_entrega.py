import re

PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remover o div que contem ENTREGA no modal de pedido
# Baseado no HTML inspecionado
patterns = [
    r'<div[^>]*background:rgba\(0,0,0,\.2\)[^>]*>(?:[^<]|<(?!div))*?ENTREGA(?:[^<]|<(?!/div>))*?</div>\s*</div>',
    r'<div[^>]*text-align:center[^>]*>\s*<div[^>]*>ENTREGA</div>\s*<div[^>]*id="mod-peso-entregue"[^>]*>.*?</div>\s*</div>',
]

original = content
for p in patterns:
    content = re.sub(p, '', content, flags=re.DOTALL)

if content != original:
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK! Campo ENTREGA removido!")
else:
    # Busca mais simples - encontrar e mostrar o contexto
    m = re.search(r'.{100}ENTREGA.{100}', content)
    if m:
        print("Contexto encontrado:")
        print(m.group())
    else:
        print("ENTREGA nao encontrado")
