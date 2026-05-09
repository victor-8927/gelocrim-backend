path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== HTML DO DASHBOARD (linhas 340-420) ===')
for i in range(339, min(420, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')

print('\n=== FUNCAO loadDashboard (linhas 1207-1280) ===')
for i in range(1206, min(1280, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
