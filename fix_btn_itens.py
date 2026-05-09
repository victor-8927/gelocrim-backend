path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Busca todos os botões que abrem modal-importacao-csv
matches = list(re.finditer(r"modal-importacao-csv", content))
for m in matches:
    ln = content[:m.start()].count('\n')+1
    ctx = content[max(0,m.start()-150):m.start()+80]
    print(f'linha {ln}: {repr(ctx)}\n')
