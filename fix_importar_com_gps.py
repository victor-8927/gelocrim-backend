path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica o mapeamento atual de codparc no processarLinhas
idx = content.find("codparc:  ['PARCEIRO','CODPARC','COD PARC']")
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'Mapeamento codparc na linha {ln} - OK')
else:
    print('Mapeamento codparc nao encontrado!')

# Verifica se ao criar o pedido, busca GPS do cliente
idx2 = content.find('clienteBase?.lat||null')
if idx2 != -1:
    ln2 = content[:idx2].count('\n')+1
    print(f'GPS do cliente usado na linha {ln2} - OK')
    # Mostra contexto
    print(repr(content[max(0,idx2-100):idx2+100]))
else:
    print('GPS do cliente nao encontrado no processarLinhas!')

# Verifica o endpoint POST /orders para salvar lat/lng
idx3 = content.find("lat:               clienteBase")
if idx3 != -1:
    print('lat do clienteBase OK!')
else:
    idx3 = content.find("lat:               (clienteBase")
    print(f'lat clienteBase: {"encontrado" if idx3!=-1 else "NAO encontrado"}')
