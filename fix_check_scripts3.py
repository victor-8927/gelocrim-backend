path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Ver fim do script 3 - onde fecha o </script>
content = ''.join(lines)

import re
closes = [m.start() for m in re.finditer(r'</script>', content)]
print('Fechamentos </script>:')
for c in closes:
    ln = content[:c].count('\n')+1
    print(f'  linha {ln}')

# Ver linhas ao redor do fechamento do script 3 (entre linha 2543 e 3943)
script3_close = [c for c in closes if 2543 < content[:c].count('\n')+1 < 3943]
if script3_close:
    for c in script3_close:
        ln = content[:c].count('\n')+1
        print(f'\n=== Fechamento Script 3 linha {ln} ===')
        for i in range(ln-5, ln+3):
            print(f'{i+1}: {repr(lines[i])}')
