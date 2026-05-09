path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 820-905 ===')
for i in range(819, min(905, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
