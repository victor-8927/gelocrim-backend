path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Busca a div da página pedidos
idx = content.find('data-page="pedidos"')
# Pega o segundo (a página, não o sidebar)
idx2 = content.find('data-page="pedidos"', idx+1)
if idx2 == -1: idx2 = idx
ln = content[:idx2].count('\n')+1
print(f'Página pedidos linha {ln}')
for i in range(ln-1, min(len(lines), ln+30)):
    print(f'{i+1}: {lines[i]}')
