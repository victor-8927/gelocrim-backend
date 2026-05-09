path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Mostra contexto completo dos botões Individual e Desenhar
idx = content.find('&#x1F4CC; Individual')
print('=== BOTÃO INDIVIDUAL ===')
print(content[max(0,idx-200):idx+200])

idx2 = content.find('&#x270F;&#xFE0F; Desenhar')
print('\n=== BOTÃO DESENHAR ===')
print(content[max(0,idx2-200):idx2+200])

# Busca as funções chamadas por esses botões
for fn in ['rotIndividual','iniciarDesenho','rotDesenhar','startDraw','ativarIndividual']:
    idx3 = content.find(fn)
    if idx3 != -1:
        ln = content[:idx3].count('\n')+1
        print(f'\n{fn} linha {ln}: {repr(content[idx3:idx3+100])}')
