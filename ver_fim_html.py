path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f'Total de linhas: {total}')
print(f'\n=== ÚLTIMAS 20 LINHAS ===')
for i in range(max(0, total-20), total):
    print(f'{i+1}: {lines[i].rstrip()}')

print(f'\n=== LINHAS 3280-3295 ===')
for i in range(3279, min(3295, total)):
    print(f'{i+1}: {lines[i].rstrip()}')
