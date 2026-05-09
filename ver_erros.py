path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total: {len(lines)} linhas')

print('\n=== LINHAS 3450-3462 ===')
for i in range(3449, min(3462, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')

print('\n=== LINHAS 3598-3610 ===')
for i in range(3597, min(3610, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')
