path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra o início dos modais (modal-importacao-csv e modal-base-clientes)
# que estão dentro do script principal — precisam ficar FORA
modal_start = None
for i in range(2500, 3486):
    if 'modal-importacao-csv' in lines[i] and '<!-- MODAL' in lines[i]:
        modal_start = i
        print(f'Modal CSV começa na linha {i+1}: {lines[i][:60]}')
        break
    if 'MODAL IMPORTAÇÃO CSV' in lines[i] or 'MODAL IMPORTACAO CSV' in lines[i]:
        modal_start = i
        print(f'Modal CSV começa na linha {i+1}: {lines[i][:60]}')
        break

if modal_start is None:
    # Procura pelo comentário do modal
    for i in range(2500, 3486):
        if '<!-- MODAL' in lines[i]:
            modal_start = i
            print(f'Modal encontrado na linha {i+1}: {lines[i][:80]}')
            break

if modal_start:
    # Remove o </script> da linha 3484 (índice 3483)
    print(f'\nRemovendo </script> da linha 3484')
    del lines[3483]
    
    # Insere </script> antes do início dos modais
    print(f'Inserindo </script> antes da linha {modal_start+1}')
    lines.insert(modal_start, '</script>\n')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'Total: {len(lines)} linhas')
    print('Pronto! Ctrl+Shift+R.')
else:
    print('Modal não encontrado! Mostrando linhas 3440-3484:')
    for i in range(3439, 3484):
        if '<!--' in lines[i] or 'modal' in lines[i].lower():
            print(f'{i+1}: {lines[i][:80]}')
