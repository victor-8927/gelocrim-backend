path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
# Mostra linhas 3760-3810 para ver contexto do modal
for i in range(3759, 3810):
    print(f'{i+1}: {lines[i]}')
