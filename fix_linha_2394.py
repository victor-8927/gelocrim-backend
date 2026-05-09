path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

lines = content.split('\n')

# Linha 2394 (índice 2393) tem o problema
# '    </div>v class="page" id="page-relatorios">'
# Deve virar apenas '    </div>' e remover as linhas 2395-fim da duplicata

# Verifica linha 2394
print(f'Linha 2394: {repr(lines[2393])}')

# Substitui linha 2394 por apenas '</div>'
lines[2393] = '    </div>'

# Agora remove as linhas 2395 até onde fecha a duplicata
# A duplicata vai da linha 2395 até antes de </div><!-- /main -->
# Vamos encontrar onde termina a duplicata
fim = None
for i in range(2394, len(lines)):
    if '<!-- /main -->' in lines[i] or 'id="page-' in lines[i] or '<!-- MODALS -->' in lines[i]:
        fim = i
        print(f'Fim duplicata: linha {i+1}: {repr(lines[i])}')
        break

if fim:
    print(f'Removendo linhas 2395 a {fim} ({fim-2394} linhas)')
    del lines[2394:fim]

content = '\n'.join(lines)

opens  = len(re.findall(r'<div[\s>]', content))
closes = len(re.findall(r'</div>', content))
print(f'<div>: {opens} opens, {closes} closes')
print(f'page-relatorios: {content.count("id=\"page-relatorios\"")} vez/vezes')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
