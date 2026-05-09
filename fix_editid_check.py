path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica onde _editVeiculoId é declarado e setado
for termo in ['_editVeiculoId', 'editVeiculoId']:
    ocorrencias = []
    idx = 0
    while True:
        idx = content.find(termo, idx)
        if idx == -1: break
        linha = content[:idx].count('\n') + 1
        ctx = content[max(0,idx-20):idx+50]
        ocorrencias.append(f'  linha {linha}: {repr(ctx)}')
        idx += 1
    if ocorrencias:
        print(f'\n{termo}:')
        for o in ocorrencias:
            print(o)
