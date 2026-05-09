path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver área do painel esquerdo da roteirização
idx = content.find('id="rot-sidebar"')
if idx == -1:
    idx = content.find('rot-lista-sel')
ln = content[:idx].count('\n')+1
print(f'rot-lista-sel linha {ln}:')
print(content[idx:idx+600])

# Ver initMap para scrollwheel
idx2 = content.find('function initMap(')
if idx2 != -1:
    print('\n\ninitMap:')
    print(content[idx2:idx2+400])

# Ver renderListaSel
idx3 = content.find('function renderListaSel')
print('\n\nrenderListaSel:')
print(content[idx3:idx3+400])
