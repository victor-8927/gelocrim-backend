path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Busca onde peso é calculado na conferência
for keyword in ['pesoTotal', 'conf-peso', 'weight_kg', 'peso_total']:
    idx = content.find(keyword)
    while idx != -1:
        ln = content[:idx].count('\n')
        line = lines[ln]
        if 'conf' in line.lower() or 'peso' in line.lower() or 'selecionados' in line.lower():
            print(f'linha {ln+1}: {line.strip()[:100]}')
        idx = content.find(keyword, idx+1)
