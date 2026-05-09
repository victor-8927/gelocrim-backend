path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Mostra linhas ao redor do modal veículo (linha 1469)
print('=== LINHAS 1466-1480 ===')
for i in range(1465, min(1480, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')

# Busca v-edit-id no HTML (linhas 1-3400)
print('\n=== v-edit-id nas primeiras 3400 linhas ===')
for i in range(min(3400, len(lines))):
    if 'v-edit-id' in lines[i]:
        print(f'{i+1}: {repr(lines[i][:100])}')
