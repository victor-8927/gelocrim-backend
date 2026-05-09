path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona aba Itens na tela de Pedidos — busca o header da tela pedidos
idx = content.find('📥 Importar Pedidos — CSV Sankhya')
ln = content[:idx].count('\n')+1
print(f'Modal importar pedidos linha {ln}')

# Adiciona botão "Importar Itens TGFITE" perto do botão de importar CSV
old_btn = '''onclick="document.getElementById('csv-file-input').click()"'''
# Verifica quantas vezes aparece
count = content.count(old_btn)
print(f'Botão importar CSV aparece {count} vezes')

# Adiciona modal de importação de itens TGFITE após o modal de importar pedidos
# Primeiro localiza o fechamento do modal existente
modal_end_marker = '<!-- FIM MODAL IMPORTAÇÃO'
if modal_end_marker not in content:
    # Busca pelo fechamento do modal de pedidos
    idx_modal = content.find('id="modal-csv-import"')
    if idx_modal == -1:
        idx_modal = content.find('csv-nome-arquivo')
    ln2 = content[:idx_modal].count('\n')+1
    print(f'Modal CSV linha {ln2}')

# Injeta modal TGFITE e funções JS
# Encontra onde fica a seção de Pedidos para adicionar botão
idx_ped = content.find("page==='pedidos'")
if idx_ped == -1:
    idx_ped = content.find("goTo('pedidos')")
ln3 = content[:idx_ped].count('\n')+1
print(f'goTo pedidos linha {ln3}')

# Busca a div principal da página pedidos
idx_pg = content.find('id="pg-pedidos"')
if idx_pg == -1:
    idx_pg = content.find("data-page='pedidos'")
if idx_pg != -1:
    ln4 = content[:idx_pg].count('\n')+1
    print(f'Página pedidos linha {ln4}')
    print(repr(content[idx_pg:idx_pg+200]))
