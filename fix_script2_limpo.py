path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra o segundo <script> (clientes + funções)
import re
scripts = list(re.finditer(r'<script[^>]*>', content))
closes = list(re.finditer(r'</script>', content))

print(f'Scripts: {len(scripts)} opens, {len(closes)} closes')
for s in scripts:
    ln = content[:s.start()].count('\n')+1
    print(f'  <script> linha {ln}')
for s in closes:
    ln = content[:s.start()].count('\n')+1
    print(f'  </script> linha {ln}')

# O segundo script começa após os modais HTML
# Encontra <script> que contém _clientesCache
idx_script2 = content.find('<script>\nvar _clientesCache')
if idx_script2 == -1:
    idx_script2 = content.find('<script>\nvar _clientesCache')
    
print(f'\nSegundo script em: {idx_script2}')
print(f'Linha: {content[:idx_script2].count(chr(10))+1}')
