path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra o CSS existente de tr:hover e mostra
import re
hovers = list(re.finditer(r'tr\s*:hover[^}]*}', content))
print(f'Total tr:hover encontrados: {len(hovers)}')
for h in hovers:
    print(f'  Pos {h.start()}: {h.group()[:80]}')

# Remove todos os tr:hover existentes
content = re.sub(r'\n?[^\n]*tr\s*:hover[^}]*\}', '', content)
print('Todos tr:hover removidos!')

# Adiciona CSS correto e definitivo
css = '''
/* ── HOVER TABELA DEFINITIVO ── */
tbody tr { transition: background .15s; }
tbody tr:hover { background: rgba(30,58,92,0.8) !important; }
tbody tr:hover td { color: #e8f0fe !important; }
tbody tr:hover td b { color: #64B4FF !important; }
'''

content = content.replace('</style>', css + '\n</style>', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
