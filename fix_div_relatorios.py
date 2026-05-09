path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print(f'Linha 2412: {repr(lines[2411])}')
print(f'Linha 2413: {repr(lines[2412])}')

# Adiciona </div> faltante após linha 2412 (fecha page-relatorios)
old = '      <div id="reports-content"><div class="empty-state"><div class="empty-icon">'
# Busca a linha exata
for i, line in enumerate(lines[2408:2415], start=2408):
    if 'reports-content' in line:
        print(f'Linha {i+1}: {repr(line)}')

# Insere </div> após a linha 2412
lines.insert(2413, '    </div>')  # fecha page-relatorios
content = '\n'.join(lines)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('</div> inserido na linha 2413!')

# Valida
import re
opens  = len(re.findall(r'<div[\s>]', content))
closes = len(re.findall(r'</div>', content))
print(f'<div> abertos: {opens}, </div> fechados: {closes}')
print('Pronto! Ctrl+Shift+R')
