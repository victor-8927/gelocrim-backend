path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var x=1;\n'
lines = (stub+'\n'+js).split('\n')
for i in range(848, 862):
    print(f'{i+1}: {repr(lines[i])}')
