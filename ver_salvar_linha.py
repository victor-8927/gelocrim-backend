path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 4155-4175 ===')
for i in range(4154, min(4175, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')
