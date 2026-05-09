path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra processarLinhas no segundo script
idx = content.find('function processarLinhas(rows)')
if idx == -1:
    print('processarLinhas nao encontrado!')
else:
    ln = content[:idx].count('\n')+1
    print(f'processarLinhas na linha {ln}')
    
    # Mostra o mapa atual
    idx_mapa = content.find("codparc:  ['PARCEIRO'", idx)
    if idx_mapa == -1:
        idx_mapa = content.find("codparc:", idx)
    if idx_mapa != -1:
        print(repr(content[idx_mapa:idx_mapa+100]))
    
    # Mostra onde cria o pedido (_csvDados.push)
    idx_push = content.find('_csvDados.push({', idx)
    if idx_push != -1:
        print('\n_csvDados.push:')
        print(content[idx_push:idx_push+600])
