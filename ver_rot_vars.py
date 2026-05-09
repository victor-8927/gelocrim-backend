path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca variáveis relacionadas a seleção de pedidos
import re
vars = re.findall(r'(rot\w+)\s*=\s*\[\]', content)
print('Variáveis de array rot*:', set(vars))

# Busca rotSelected
for match in re.finditer(r'(rotSelected\w*)', content):
    ctx = content[max(0,match.start()-30):match.end()+50]
    print(f'\n{match.group()}: ...{ctx}...')
    if len(list(re.finditer(match.group(), content))) > 5:
        break

# Ver rotGetPesoTotal
idx = content.find('function rotGetPesoTotal')
print('\n=== rotGetPesoTotal ===')
print(content[idx:idx+200])
