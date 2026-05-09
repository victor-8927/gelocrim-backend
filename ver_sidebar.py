path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Mostra o sidebar
for i, line in enumerate(lines):
    if 'sidebar-item' in line or 'sidebar-section' in line:
        print(f'{i+1}: {lines[i].rstrip()}')
