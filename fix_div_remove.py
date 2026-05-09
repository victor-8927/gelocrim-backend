path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Remove a linha que acabei de inserir (linha 2413 agora é '    </div>')
# Verifica contexto
for i in range(2410, 2420):
    print(f'{i+1}: {repr(lines[i])}')

# Remove linha 2413 (índice 2412)
if lines[2413].strip() == '</div>':
    lines.pop(2413)
    print('\nLinha removida!')

content = '\n'.join(lines)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re
opens  = len(re.findall(r'<div[\s>]', content))
closes = len(re.findall(r'</div>', content))
print(f'<div>: {opens} opens, {closes} closes')

# Agora encontra o div duplicado corretamente
# O problema é que a página relatorios tem 2 divs de page-relatorios
count = content.count('id="page-relatorios"')
print(f'page-relatorios aparece {count} vezes!')
