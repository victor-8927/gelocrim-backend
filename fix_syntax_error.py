path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 4835-4855 ===')
for i in range(4834, min(4855, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
