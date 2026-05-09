path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Encontra posições de abertura e fechamento
opens  = [m.start() for m in re.finditer(r'<script[^>]*>', content)]
closes = [m.start() for m in re.finditer(r'</script>', content)]

print(f'Opens:  {len(opens)}  em posições: {opens}')
print(f'Closes: {len(closes)} em posições: {closes}')

# Identifica scripts não fechados
fechados = set()
for o in opens:
    # Encontra o próximo close após este open
    next_close = next((c for c in closes if c > o), None)
    if next_close:
        fechados.add(o)
    else:
        print(f'\nScript SEM FECHAMENTO na pos {o}:')
        print(content[o:o+200])
