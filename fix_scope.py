path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
scripts = list(re.finditer(r'<script[^>]*>', content))
closes  = list(re.finditer(r'</script>', content))

# Mapeia qual script contém cada função
for fn in ['_editVeiculoId', 'salvarVeiculoCompleto', 'editarVeiculo']:
    idx = content.find(fn)
    while idx != -1:
        # Verifica em qual script está
        script_num = 0
        for i, s in enumerate(scripts):
            if s.start() < idx:
                script_num = i+1
        ln = content[:idx].count('\n')+1
        print(f'{fn} → script {script_num}, linha {ln}')
        idx = content.find(fn, idx+1)
    print()
