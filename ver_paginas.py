path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Mostra todas as linhas com page id ou comentários de seção
for i, line in enumerate(lines):
    if 'class="page"' in line or '══' in line or 'page-rot' in line:
        print(f'{i+1}: {line.rstrip()}')
