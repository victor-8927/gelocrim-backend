path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Encontra as duas ocorrências
ocorrencias = [m.start() for m in re.finditer('id="page-relatorios"', content)]
for o in ocorrencias:
    ln = content[:o].count('\n')+1
    print(f'page-relatorios na linha {ln}')

# A segunda ocorrência é a duplicata - encontra seu div pai e remove
# Segunda ocorrência
idx2 = ocorrencias[1]

# Volta para encontrar o início do <div class="page"
inicio = content.rfind('<div', 0, idx2)
ln_inicio = content[:inicio].count('\n')+1
print(f'Início do div duplicado: linha {ln_inicio}')
print(repr(content[inicio:inicio+60]))

# Encontra o fim deste div (fecha quando depth volta a 0)
depth = 0
i = inicio
while i < len(content):
    if content[i:i+4] == '<div':
        depth += 1
    elif content[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            fim = i + 6
            break
    i += 1

ln_fim = content[:fim].count('\n')+1
print(f'Fim do div duplicado: linha {ln_fim}')
print(f'Removendo {fim-inicio} chars...')

content = content[:inicio] + content[fim:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

opens  = len(re.findall(r'<div[\s>]', content))
closes = len(re.findall(r'</div>', content))
print(f'<div>: {opens} opens, {closes} closes')
count = content.count('id="page-relatorios"')
print(f'page-relatorios aparece {count} vez/vezes')
print('Pronto! Ctrl+Shift+R')
