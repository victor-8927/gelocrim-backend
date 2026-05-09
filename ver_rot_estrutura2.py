path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca pelo container da roteirização visual
for termo in ['rot-map', 'MAPA -->', 'rot-sidebar', 'Roteirização Visual', 'roteirizacao']:
    idx = content.find(termo)
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'"{termo}" linha {ln}')

# Mostra estrutura ao redor do rot-map
idx = content.find('id="rot-map"')
ln = content[:idx].count('\n')+1
lines = content.split('\n')
print(f'\nContexto rot-map (linha {ln}):')
for i in range(max(0,ln-30), min(len(lines), ln+5)):
    print(f'{i+1}: {lines[i]}')
