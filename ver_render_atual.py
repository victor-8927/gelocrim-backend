path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
for m in re.finditer(r'function renderRotMapMarkers', content):
    antes = content[:m.start()]
    opens = antes.count('<script')
    closes = antes.count('</script>')
    ln = antes.count('\n')+1
    print(f'renderRotMapMarkers: linha {ln}, script {opens}')
    # Mostra início da função
    print(repr(content[m.start():m.start()+200]))
    print()
