path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Pega a chave do Google Maps
m = re.search(r'key=([A-Za-z0-9_-]+)', content)
if m:
    print(f'Google Maps Key: {m.group(1)}')

# Verifica quais bibliotecas estão carregadas
m2 = re.search(r'libraries=([^&"]+)', content)
if m2:
    print(f'Libraries: {m2.group(1)}')

# Verifica se Directions está sendo usado
print(f'DirectionsService usado: {"DirectionsService" in content}')
print(f'DirectionsRenderer usado: {"DirectionsRenderer" in content}')

# Verifica o erro do mapa - busca o callback initMap
idx = content.find('function initMap')
if idx != -1:
    ln = content[:idx].count('\n')
    lines = content.split('\n')
    print(f'\ninitMap linha {ln+1}:')
    for i in range(ln, ln+10):
        print(f'{i+1}: {lines[i]}')
