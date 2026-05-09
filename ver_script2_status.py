path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Encontra o segundo script
scripts = list(re.finditer(r'<script[^>]*>', content))
closes  = list(re.finditer(r'</script>', content))

print(f'Scripts: {len(scripts)} opens / {len(closes)} closes')
for s in scripts:
    ln = content[:s.start()].count('\n')+1
    print(f'  <script> linha {ln}')
for s in closes:
    ln = content[:s.start()].count('\n')+1
    print(f'  </script> linha {ln}')

# Extrai o segundo script e verifica
idx2_start = None
for s in scripts:
    if content[s.start():s.end()] == '<script>':
        ln = content[:s.start()].count('\n')+1
        if ln > 3400:
            idx2_start = s.end()
            idx2_ln = ln
            break

if idx2_start:
    # Encontra o </script> correspondente
    idx2_end = content.find('</script>', idx2_start)
    script2 = content[idx2_start:idx2_end]
    print(f'\nSegundo script: linha {idx2_ln}, tamanho {len(script2)} chars')
    print(f'Primeiras 3 linhas:')
    for ln in script2.split('\n')[:5]:
        print(f'  {repr(ln[:80])}')
    print(f'Últimas 3 linhas:')
    for ln in script2.split('\n')[-5:]:
        print(f'  {repr(ln[:80])}')
