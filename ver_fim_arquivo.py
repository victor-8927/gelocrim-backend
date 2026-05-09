path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f'Total linhas: {total}')
print('\n=== ÚLTIMAS 30 LINHAS ===')
for i in range(max(0, total-30), total):
    print(f'{i+1}: {lines[i].rstrip()[:100]}')
