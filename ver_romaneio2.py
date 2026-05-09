path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra gerarRomaneio e mostra completa
for i, line in enumerate(lines):
    if 'function gerarRomaneio' in line:
        print(f'gerarRomaneio na linha {i+1}')
        for j in range(i, min(len(lines), i+60)):
            print(f'{j+1}: {repr(lines[j][:110])}')
        break
