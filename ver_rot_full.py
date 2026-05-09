path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
# Mostra linhas 765 a 895
for i in range(764, 895):
    print(f'{i+1}: {lines[i]}')
