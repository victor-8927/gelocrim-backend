path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra gerarRomaneio
for i, line in enumerate(lines):
    if 'function gerarRomaneio' in line:
        print(f'gerarRomaneio começa na linha {i+1}')
        # Mostra até o fechamento
        for j in range(i, min(i+80, len(lines))):
            print(f'{j+1}: {repr(lines[j][:100])}')
        break
