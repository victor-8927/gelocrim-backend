path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Encontra todos os modal-veiculo
for m in re.finditer(r'modal-veiculo-completo', content):
    ln = content[:m.start()].count('\n')+1
    ctx = content[max(0,m.start()-30):m.start()+50]
    print(f'Linha {ln}: {repr(ctx)}')
