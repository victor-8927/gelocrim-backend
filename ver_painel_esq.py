path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver passo 1, passo 2, passo 3
for p in ['Passo 1','Passo 2','Passo 3','passo-3','rot-step-3','renderListaSel']:
    idx = content.find(p)
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'"{p}" linha {ln}: {repr(content[idx:idx+120])}')

# Ver o mapa - scrollwheel
for k in ['scrollwheel','gestureHandling','wheel']:
    idx = content.find(k)
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'\n"{k}" linha {ln}: {repr(content[idx:idx+80])}')
