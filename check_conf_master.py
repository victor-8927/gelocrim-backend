path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver função renderizarListaConf
idx = content.find('function renderizarListaConf')
ln = content[:idx].count('\n')
print('renderizarListaConf:')
for i in range(ln, ln+40):
    print(f'{i+1}: {lines[i]}')
