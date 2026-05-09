path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Rastreia profundidade de divs linha a linha
depth = 0
min_depth = 0
min_line = 0
for i, line in enumerate(lines):
    opens  = line.count('<div') - line.count('<div/>')
    closes = line.count('</div>')
    depth += opens - closes
    if depth < min_depth:
        min_depth = depth
        min_line = i+1

print(f'Profundidade mínima: {min_depth} na linha {min_line}')
print(f'Contexto linha {min_line}:')
for i in range(max(0,min_line-3), min(len(lines),min_line+3)):
    print(f'{i+1}: {repr(lines[i])}')

# Encontra onde depth vai negativo pela primeira vez
depth = 0
for i, line in enumerate(lines):
    opens  = line.count('<div') - line.count('<div/>')
    closes = line.count('</div>')
    depth += opens - closes
    if depth < 0:
        print(f'\nDepth negativo na linha {i+1}: {repr(line)}')
        print(f'Linhas anteriores:')
        for j in range(max(0,i-3), i+2):
            print(f'  {j+1}: {lines[j]}')
        break
