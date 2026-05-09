path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
for m in re.finditer(r'function lerArquivoCSV', content):
    ln = content[:m.start()].count('\n')+1
    # Qual script?
    antes = content[:m.start()]
    opens = antes.count('<script')
    closes = antes.count('</script>')
    print(f'Linha {ln} — script {opens} (opens={opens}, closes={closes})')
    print(repr(content[m.start():m.start()+200]))
    print()
