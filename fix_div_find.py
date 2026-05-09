path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Rastreia depth e mostra onde fica em 0 pela última vez antes de 2416
depth = 0
last_zero = 0
for i, line in enumerate(lines[:2416]):
    opens  = line.count('<div') - line.count('<div/>')
    closes = line.count('</div>')
    depth += opens - closes
    if depth == 0:
        last_zero = i+1

print(f'Último depth=0 antes de 2416: linha {last_zero}')
print(f'Depth na linha 2415: {depth}')

# Mostra linhas ao redor do último zero
for i in range(max(0,last_zero-2), min(len(lines),last_zero+5)):
    print(f'{i+1}: {lines[i]}')
