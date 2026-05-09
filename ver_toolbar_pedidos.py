path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Busca toolbar na tela pedidos
idx = content.find("page==='pedidos'")
ln = content[:idx].count('\n')+1
print(f'goTo pedidos linha {ln}')

# Mostra linhas 395-430 (toolbar)
for i in range(394, 435):
    print(f'{i+1}: {lines[i]}')
