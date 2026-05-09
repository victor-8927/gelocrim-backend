path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Mostra linhas 2395-2420 com depth
import re
depth = 0
# Calcula depth até linha 2394
for i in range(2394):
    opens  = len(re.findall(r'<div[\s>]', lines[i]))
    closes = len(re.findall(r'</div>', lines[i]))
    depth += opens - closes

print(f'Depth na linha 2394: {depth}')
print()
for i in range(2394, 2420):
    line = lines[i]
    opens  = len(re.findall(r'<div[\s>]', line))
    closes = len(re.findall(r'</div>', line))
    depth += opens - closes
    print(f'{i+1} [d={depth}] ({opens}o,{closes}c): {line[:80]}')
