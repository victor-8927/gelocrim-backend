path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza rot-lista-sel e mostra contexto
idx = content.find('"rot-lista-sel"')
ln = content[:idx].count('\n')+1
print(f'rot-lista-sel linha {ln}')
# Mostra 10 linhas antes
lines = content.split('\n')
for i in range(max(0,ln-10), min(len(lines),ln+15)):
    print(f'{i+1}: {lines[i]}')
