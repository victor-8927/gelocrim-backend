path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

ocorrencias = [m.start() for m in re.finditer('id="page-relatorios"', content)]
for o in ocorrencias:
    ln = content[:o].count('\n')+1
    ctx = content[max(0,o-50):o+60]
    print(f'linha {ln}: {repr(ctx)}')
