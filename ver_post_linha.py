orders_path = r'C:\fleet-cloud\app\routers\orders.py'

with open(orders_path, 'r') as f:
    lines = f.readlines()

# Encontra a linha do @router.post("")
for i, line in enumerate(lines):
    if '@router.post("")' in line:
        print(f'POST encontrado na linha {i+1}')
        print(''.join(lines[i:i+25]))
        break
