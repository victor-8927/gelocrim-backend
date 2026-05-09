path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Substitui todos MAP_PIN por CIRCLE e remove anchor
content = content.replace('google.maps.SymbolPath.MAP_PIN', 'google.maps.SymbolPath.CIRCLE')
content = re.sub(r',\s*anchor:\s*new google\.maps\.Point\(0,\s*22\)', '', content)

# Ajusta scale para CIRCLE (MAP_PIN usava 4-6, CIRCLE usa 8-12)
content = content.replace('scale:sel?12:9,fillColor:cor', 'scale:sel?12:9,fillColor:cor')
content = content.replace('scale: sel ? 6 : 4,', 'scale: sel ? 12 : 8,')
content = content.replace('scale:sel?6:4,', 'scale:sel?12:8,')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Conta ocorrências
c = content.count('MAP_PIN')
print(f'MAP_PIN restantes: {c}')
print('Pronto! Ctrl+Shift+R.')
