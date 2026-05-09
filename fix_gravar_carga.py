path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca a função gravarCarga atual
idx = content.find('async function gravarCarga()')
ln = content[:idx].count('\n')+1
lines = content.split('\n')
print(f'gravarCarga linha {ln}:')
for i in range(ln-1, min(ln+25, len(lines))):
    print(f'{i+1}: {lines[i]}')
