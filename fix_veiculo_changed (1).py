path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver rotVeiculoChanged e carregarFrota
idx = content.find('function rotVeiculoChanged()')
print('rotVeiculoChanged:')
print(content[idx:idx+200])

idx2 = content.find('async function carregarFrota()')
print('\ncarregarFrota:')
print(content[idx2:idx2+600])
