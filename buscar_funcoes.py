path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Buscando onchange, veiculo, motorista...')
for i, line in enumerate(lines):
    l = line.lower()
    if any(x in l for x in ['onchange', 'rot-veiculo', 'sel-motorista', 'carregarfrota', 'veiculochanged']):
        print(f'{i+1}: {line.rstrip()}')
