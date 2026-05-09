path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Busca onde confOrdem é populado
idx = content.find('confOrdem')
while idx != -1:
    ln = content[:idx].count('\n')+1
    line = lines[ln-1]
    if 'push' in line or '= [' in line or 'cli-' in line:
        print(f'linha {ln}: {line.strip()[:100]}')
    idx = content.find('confOrdem', idx+1)
