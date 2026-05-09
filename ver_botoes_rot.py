path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca botões de seleção individual e desenhar área
terms = ['individual','Individual','desenhar','Desenhar','DrawingManager','polygon','rotIndividual','rot-btn']
for t in terms:
    idx = content.find(t)
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'"{t}" linha {ln}: {repr(content[max(0,idx-20):idx+60])}')

# Verifica atualizarSelecaoRot
idx = content.find('function atualizarSelecaoRot')
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'\natualizarSelecaoRot linha {ln}:')
    print(content[idx:idx+400])
