path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print('Linhas 2385-2410:')
for i in range(2384, 2410):
    print(f'{i+1}: {repr(lines[i])}')
