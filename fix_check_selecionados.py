path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Ver contexto da linha 3176
print('Linhas 3150-3200:')
for i in range(3149, 3200):
    print(f'{i+1}: {lines[i]}')
