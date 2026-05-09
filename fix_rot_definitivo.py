path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Verifica onde estão as funções
for fn in ['filtrarRotMapa','selecionarTodaRota','renderRotMapMarkers','getCorRota']:
    matches = list(re.finditer(r'function '+fn, content))
    if matches:
        for m in matches:
            antes = content[:m.start()]
            opens = antes.count('<script')
            closes = antes.count('</script>')
            ln = antes.count('\n')+1
            print(f'{fn}: linha {ln}, opens={opens} closes={closes} → script {opens}')
    else:
        print(f'{fn}: NAO ENCONTRADA')

# Verifica o primeiro script (script 3 — o principal)
scripts = list(re.finditer(r'<script[^>]*>', content))
closes_list = list(re.finditer(r'</script>', content))
print(f'\nScripts: {len(scripts)} opens / {len(closes_list)} closes')
for i,s in enumerate(scripts):
    ln = content[:s.start()].count('\n')+1
    print(f'  Script {i+1}: linha {ln}')
for i,s in enumerate(closes_list):
    ln = content[:s.start()].count('\n')+1
    print(f'  Close {i+1}: linha {ln}')
