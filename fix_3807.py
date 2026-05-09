path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 3803-3812 ===')
for i in range(3802, min(3812, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')
