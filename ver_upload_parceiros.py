path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 2138-2150 ===')
for i in range(2137, min(2150, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')

# Verifica se uploadParceiros existe
content = ''.join(lines)
if 'function uploadParceiros' in content:
    print('\nFunção uploadParceiros EXISTE!')
else:
    print('\nFunção uploadParceiros NAO EXISTE!')
