path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra a seção de veículos
start = None
for i, line in enumerate(lines):
    if 'page-veiculos' in line:
        start = i
        break

print(f'=== VEÍCULOS (linhas {start+1} a {start+80}) ===')
for i in range(start, min(start+80, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
