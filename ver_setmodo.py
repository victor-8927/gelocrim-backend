path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function setModoSelecao')
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'setModoSelecao linha {ln}:')
    print(content[idx:idx+500])
else:
    print('setModoSelecao NAO ENCONTRADA!')
