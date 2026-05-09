path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver renderOrders atual
idx = content.find('function renderOrders(')
print('=== renderOrders ===')
print(content[idx:idx+1500])
