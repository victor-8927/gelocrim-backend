path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Encontra o painel de conferencia master
idx = content.find('conf-painel')
if idx == -1:
    idx = content.find('Conferência Master')
    if idx == -1:
        idx = content.find('conferencia-master')
        if idx == -1:
            idx = content.find('conf-mapa')

ln = content[:idx].count('\n')
print(f'Conferência Master começa linha {ln+1}')
# Mostra 120 linhas a partir dali
for i in range(max(0,ln-30), ln+120):
    print(f'{i+1}: {lines[i]}')
