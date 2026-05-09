path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver função setModoSelecao
idx = content.find('function setModoSelecao')
ln = content[:idx].count('\n')
print('setModoSelecao:')
for i in range(ln, ln+20):
    print(f'{i+1}: {lines[i]}')

print('\n---')
# Ver função atualizarSelecaoRot
idx2 = content.find('function atualizarSelecaoRot')
ln2 = content[:idx2].count('\n')
print('atualizarSelecaoRot:')
for i in range(ln2, ln2+20):
    print(f'{i+1}: {lines[i]}')
