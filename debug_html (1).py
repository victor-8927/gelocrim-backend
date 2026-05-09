path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca o problema na função loadProducao
idx = content.find('async function editarPallet(id)')
print(f'editarPallet encontrado em: {idx}')

# Mostra contexto ao redor
if idx != -1:
    print(content[max(0,idx-500):idx+200])
