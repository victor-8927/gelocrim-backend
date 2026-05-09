path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver HTML da toolbar de roteirização
idx = content.find('page-roteirizacao')
ln = content[:idx].count('\n')
print('Toolbar roteirização (linhas 600-900):')
for i in range(ln, ln+5):
    print(f'{i+1}: {lines[i]}')

# Busca campos de tipo de roteirização
for keyword in ['opt-tipo', 'aproximado', 'otimizado', 'btn-rot-map', 'opt-date']:
    idx2 = content.find(keyword)
    if idx2 != -1:
        ln2 = content[:idx2].count('\n')
        print(f'\n{keyword} linha {ln2+1}: {lines[ln2][:100]}')
