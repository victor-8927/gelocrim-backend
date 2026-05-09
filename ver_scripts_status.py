path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
opens  = list(re.finditer(r'<script[^>]*>', content))
closes = list(re.finditer(r'</script>', content))
print(f'Opens: {len(opens)} / Closes: {len(closes)}')
for s in opens:
    ln = content[:s.start()].count('\n')+1
    print(f'  <script> linha {ln}')
for s in closes:
    ln = content[:s.start()].count('\n')+1
    print(f'  </script> linha {ln}')

# Mostra últimas 5 linhas
lines = content.split('\n')
print(f'\nTotal linhas: {len(lines)}')
print('Últimas 5:')
for i in range(len(lines)-5, len(lines)):
    print(f'  {i+1}: {repr(lines[i][:80])}')
