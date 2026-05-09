path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca campos usados no renderOrders
idx = content.find('function renderOrders(orders)')
print(content[idx:idx+2000])
