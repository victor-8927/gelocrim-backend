path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra a tela de roteirização
idx = content.find("id='roteirizacao'")
if idx == -1:
    idx = content.find('id="roteirizacao"')
ln = content[:idx].count('\n')+1
print(f'Tela roteirização linha {ln}')

# Mostra as primeiras 60 linhas da tela
lines = content.split('\n')
for i in range(ln-1, min(len(lines), ln+60)):
    print(f'{i+1}: {lines[i]}')
