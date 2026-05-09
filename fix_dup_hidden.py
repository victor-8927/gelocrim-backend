path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove o segundo v-edit-id (linha 1624, índice 1623)
print(f'Linha 1624: {repr(lines[1623])}')
print(f'Linha 1625: {repr(lines[1624])}')

if 'v-edit-id' in lines[1623]:
    del lines[1623]
    print('Duplicado removido!')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verifica
count = sum(1 for l in lines if 'v-edit-id' in l and not l.strip().startswith('//'))
print(f'v-edit-id restantes: {count}')
print('Pronto! Ctrl+Shift+R.')
