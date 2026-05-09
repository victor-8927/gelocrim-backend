path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca pelo id correto
for termo in ['page-clientes', 'page-parceiros', 'PARCEIROS', 'Parceiros']:
    idx = content.find(termo)
    if idx != -1:
        print(f'=== {termo} na pos {idx} ===')
        print(content[idx:idx+600])
        print()
