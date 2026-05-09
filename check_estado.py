path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

opens  = len(re.findall(r'<div[\s>]', content))
closes = len(re.findall(r'</div>', content))
print(f'<div>: {opens} opens, {closes} closes')

count = content.count('id="page-relatorios"')
print(f'page-relatorios: {count} vez/vezes')

scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
print(f'Scripts: {len(scripts)}')

# Verifica funções críticas
funcs = ['loadRoutes','liberarRota','verProgressoRota','gravarCarga','doLogin','setModoSelecao']
for fn in funcs:
    found = fn in content
    print(f'  {fn}: {"OK" if found else "NAO ENCONTRADA"}')

lines = content.split('\n')
print(f'Total linhas: {len(lines)}')
