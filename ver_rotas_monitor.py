path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra as seções
for i, line in enumerate(lines):
    if 'page-rotas' in line or 'page-monitoramento' in line or 'Torre de Controle' in line:
        print(f'{i+1}: {line.rstrip()}')

# Mostra HTML da tela de rotas
print('\n=== TELA ROTAS (primeiras 40 linhas) ===')
for i, line in enumerate(lines):
    if 'page-rotas' in line:
        for j in range(i, min(i+40, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
