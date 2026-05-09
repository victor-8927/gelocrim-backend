path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver todos os campos usados dos pedidos
import re
fields = re.findall(r'[ox]\.([\w_]+)', content)
order_fields = [f for f in set(fields) if f in ['total_value','value','price','order_value','amount','cost_per_day','daily_cost','km_l','fuel']]
print('Campos financeiros encontrados:', order_fields)

# Ver saveOrder para saber quais campos são salvos
idx = content.find('async function saveOrder(')
print('\n=== saveOrder ===')
print(content[idx:idx+800])

# Ver campos do driver no saveDriver
idx2 = content.find('async function saveDriver(')
print('\n=== saveDriver ===')
print(content[idx2:idx2+600])
