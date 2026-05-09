path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

opens  = [(m.start(), content[m.start():m.start()+50]) for m in re.finditer(r'<script[^>]*>', content)]
closes = [m.start() for m in re.finditer(r'</script>', content)]

print(f'Opens: {len(opens)}')
print(f'Closes: {len(closes)}')

# Simula o parser para encontrar qual script não fecha
stack = []
oi = 0
ci = 0
events = []
for pos, snippet in opens:
    events.append((pos, 'open', snippet))
for pos in closes:
    events.append((pos, 'close', ''))
events.sort()

depth = 0
for pos, typ, snip in events:
    if typ == 'open':
        depth += 1
        stack.append((pos, snip))
        print(f'  OPEN  depth={depth} pos={pos}: {snip[:40]}')
    else:
        if stack:
            opened = stack.pop()
            print(f'  CLOSE depth={depth} pos={pos} <- fechou open em {opened[0]}')
        depth -= 1

if stack:
    print(f'\n!!! Scripts NAO FECHADOS: {len(stack)}')
    for pos, snip in stack:
        print(f'  Pos {pos}: {snip[:60]}')
        # Mostra contexto do arquivo nessa posição
        line_num = content[:pos].count('\n') + 1
        print(f'  Linha {line_num}')
        # Mostra 300 chars após o open
        print(f'  Conteudo: {content[pos:pos+200]}')
