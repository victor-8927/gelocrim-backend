path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'abrirModalPlanilha' in content:
    idx = content.find('abrirModalPlanilha')
    ln = content[:idx].count('\n')+1
    print(f'abrirModalPlanilha encontrado na linha {ln}')
else:
    print('BOTAO NAO ENCONTRADO!')

if 'modal-planilha-ti' in content:
    print('Modal planilha-ti: EXISTE')
else:
    print('Modal planilha-ti: NAO EXISTE')

if 'importarPlanilhaTI' in content:
    print('Função importarPlanilhaTI: EXISTE')
else:
    print('Função importarPlanilhaTI: NAO EXISTE')
