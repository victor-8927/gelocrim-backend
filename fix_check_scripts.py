path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Conta scripts e localiza funções críticas
scripts = list(re.finditer(r'<script[^>]*>', content))
print(f'Total de blocos <script>: {len(scripts)}')
for i, m in enumerate(scripts):
    ln = content[:m.start()].count('\n')+1
    print(f'  Script {i+1}: linha {ln}')

# Localiza cada função crítica
funcs = ['loadRoutes','liberarRota','setModoSelecao','carregarFrota','atualizarSelecaoRot']
for fn in funcs:
    idx = content.find(f'function {fn}')
    if idx == -1:
        idx = content.find(f'async function {fn}')
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'  {fn}: linha {ln}')
    else:
        print(f'  {fn}: NAO ENCONTRADA!')
