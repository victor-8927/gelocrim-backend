path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver função abrirConferenciaMaster completa
idx = content.find('function abrirConferenciaMaster')
ln = content[:idx].count('\n')
print('abrirConferenciaMaster:')
for i in range(ln, ln+60):
    print(f'{i+1}: {lines[i]}')
