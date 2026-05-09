path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica modal
if 'modal-base-clientes' in content:
    import re
    ocorr = [m.start() for m in re.finditer('modal-base-clientes', content)]
    print(f'modal-base-clientes encontrado {len(ocorr)} vezes')
    for pos in ocorr:
        print(f'  Pos {pos}: {content[max(0,pos-30):pos+60]}')
else:
    print('modal-base-clientes NAO existe!')

# Verifica função
if 'function abrirImportacaoBaseClientes' in content:
    idx = content.find('function abrirImportacaoBaseClientes')
    print(f'\nFunção encontrada:')
    print(content[idx:idx+200])
else:
    print('\nFunção abrirImportacaoBaseClientes NAO existe!')
