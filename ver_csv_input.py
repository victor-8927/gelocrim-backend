path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica o input do CSV
import re
for m in re.finditer(r'csv-file-input', content):
    ln = content[:m.start()].count('\n')+1
    ctx = content[max(0,m.start()-20):m.start()+80]
    print(f'Linha {ln}: {repr(ctx)}')
