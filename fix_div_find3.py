path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Mostra depth a cada 100 linhas até 2416
depth = 0
for i, line in enumerate(lines[:2416]):
    import re
    # Conta apenas divs reais (não em atributos ou comentários)
    opens  = len(re.findall(r'<div[\s>]', line))
    closes = len(re.findall(r'</div>', line))
    depth += opens - closes
    if i % 200 == 0 or depth < 1:
        print(f'linha {i+1}: depth={depth}  ({opens} opens, {closes} closes) | {line[:60]}')

print(f'\nDepth final: {depth}')
