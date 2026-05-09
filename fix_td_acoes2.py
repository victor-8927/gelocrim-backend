path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re, subprocess

# Ver contexto ao redor do problema
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var x=1;\n'
lines = (stub+'\n'+js).split('\n')

# Acha linha com excluirRota
for i, l in enumerate(lines):
    if 'excluirRota' in l and 'btn-danger' in l:
        print('Contexto:')
        for j in range(max(0,i-2), min(len(lines),i+5)):
            print(f'{j+1}: {repr(lines[j])}')
        break
