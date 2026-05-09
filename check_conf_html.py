path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Encontra o painel de conferencia master
idx = content.find('conf-lista-clientes')
ln = content[:idx].count('\n')
print('Área conf-lista-clientes:')
for i in range(max(0,ln-5), ln+30):
    print(f'{i+1}: {lines[i]}')
