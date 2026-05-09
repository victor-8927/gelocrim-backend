path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Busca onde rotSelecionados recebe valores
idx = 0
while True:
    idx = content.find('rotSelecionados', idx+1)
    if idx == -1: break
    ln = content[:idx].count('\n')
    line = lines[ln]
    if 'push' in line or '=' in line and 'cli-' in line or 'order' in line.lower():
        print(f'linha {ln+1}: {line.strip()[:120]}')
