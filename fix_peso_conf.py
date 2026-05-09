path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver como confOrdem é populado na linha 3176
idx = content.find('confOrdem = [...selecionados]')
ln = content[:idx].count('\n')
print('confOrdem populado:')
for i in range(max(0,ln-5), ln+5):
    print(f'{i+1}: {lines[i]}')

# Ver linha 3092 - como selecionados é construído
idx2 = content.find('const selecionados = ')
ln2 = content[:idx2].count('\n')
print('\nselecionados:')
for i in range(max(0,ln2-2), ln2+5):
    print(f'{i+1}: {lines[i]}')

# Ver estrutura do objeto no clienteMap - weight_kg
idx3 = content.find('weight_kg: 0,')
ln3 = content[:idx3].count('\n')
print('\nclienteMap weight_kg:')
for i in range(max(0,ln3-3), ln3+8):
    print(f'{i+1}: {lines[i]}')
