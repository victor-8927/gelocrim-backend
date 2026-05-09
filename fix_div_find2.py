path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Rastreia de trás para frente a partir da linha 2415
# Procura onde depth vai positivo (div aberto sem fechar)
depth = 0
for i in range(2414, -1, -1):
    line = lines[i]
    opens  = line.count('<div') - line.count('<div/>')
    closes = line.count('</div>')
    depth += closes - opens  # invertido pois vai de trás
    if depth < 0:
        print(f'DIV extra aberto na linha {i+1}: {repr(lines[i])}')
        for j in range(max(0,i-2), min(len(lines),i+4)):
            print(f'  {j+1}: {lines[j]}')
        break
