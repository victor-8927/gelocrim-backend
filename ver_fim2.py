path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total linhas: {len(lines)}')
print('=== LINHAS 3708-FIM ===')
for i in range(3707, len(lines)):
    print(f'{i+1}: {repr(lines[i][:100])}')
