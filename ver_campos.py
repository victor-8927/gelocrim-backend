path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver campos do pedido no renderOrders
idx = content.find('function renderOrders(')
print('=== renderOrders (primeiros campos) ===')
print(content[idx:idx+800])

# Ver campos do motorista
idx2 = content.find('function loadDrivers(')
print('\n=== loadDrivers ===')
print(content[idx2:idx2+600])

# Ver campos do veículo no select
idx3 = content.find('async function carregarVeiculosSelect(')
print('\n=== carregarVeiculosSelect ===')
print(content[idx3:idx3+600])
