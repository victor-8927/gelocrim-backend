PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

OLD = """          weight_kg: 0,
          pedidos: [],
          order_type: o.order_type||'',
          status: 'pending',
          order_ids: []"""

NEW = """          weight_kg: 0,
          volume_m3: 0,
          pedidos: [],
          order_type: o.order_type||'',
          status: 'pending',
          order_ids: []"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK: volume_m3 adicionado ao clienteMap!")
else:
    print("AVISO: bloco nao encontrado")

# Tambem adicionar acumulacao do volume
OLD2 = "      clienteMap[key].weight_kg += parseFloa"
# Buscar o contexto completo
import re
m = re.search(r'clienteMap\[key\]\.weight_kg \+= parseFloat.*?;', content)
if m:
    OLD_WEIGHT = m.group()
    NEW_WEIGHT = OLD_WEIGHT + '\n      clienteMap[key].volume_m3 += parseFloat(o.volume_m3||0);'
    content = content.replace(OLD_WEIGHT, NEW_WEIGHT)
    print("OK: acumulacao de volume_m3 adicionada!")
else:
    print("AVISO: acumulacao nao encontrada")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Ctrl+Shift+R e Atualizar na roteirizacao!")
