path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica como editId é lido no salvarVeiculoCompleto
idx = content.find('salvarVeiculoCompleto')
while idx != -1:
    ctx = content[idx:idx+100]
    if 'async function' in ctx or 'function' in ctx:
        print(f'Função em pos {idx}:')
        print(repr(content[idx:idx+300]))
        break
    idx = content.find('salvarVeiculoCompleto', idx+1)

# Verifica como editId é definido
idx2 = content.find('dataset.editId = id')
if idx2 != -1:
    print(f'\neditId definido: {repr(content[idx2-20:idx2+40])}')

# Verifica como editId é lido
idx3 = content.find('.dataset.editId||null')
if idx3 != -1:
    print(f'\neditId lido: {repr(content[idx3-20:idx3+40])}')
