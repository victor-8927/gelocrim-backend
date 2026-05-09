path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra as variáveis CSS
for i, line in enumerate(lines):
    if ':root' in line or '--bg' in line or '--text' in line or '--border' in line or '--card' in line:
        print(f'{i+1}: {lines[i].rstrip()}')
    if i > 200:
        break
