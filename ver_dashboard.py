path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra o dashboard
for i, line in enumerate(lines):
    if 'dashboard' in line.lower() or 'page-dash' in line.lower():
        start = max(0, i-2)
        end = min(len(lines), i+3)
        for j in range(start, end):
            print(f'{j+1}: {lines[j].rstrip()}')
        print('---')
