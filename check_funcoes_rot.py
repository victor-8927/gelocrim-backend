path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
for fn in ['filtrarRotMapa', 'selecionarTodaRota', 'renderRotMapMarkers']:
    for m in re.finditer(r'function '+fn, content):
        antes = content[:m.start()]
        opens = antes.count('<script')
        closes = antes.count('</script>')
        ln = antes.count('\n')+1
        print(f'{fn}: linha {ln}, script {opens} (opens={opens}, closes={closes})')
