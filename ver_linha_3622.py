path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 3615-3630 ===')
for i in range(3614, min(3630, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()[:120]}')
