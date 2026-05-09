path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Verifica se existe tabela order_items no backend
idx = content.find('order_items')
print(f'order_items no HTML: {"SIM" if idx!=-1 else "NAO"}')

# 2. Verifica onde fica o modal de importação CSV para adicionar botão de itens
idx2 = content.find('csv-file-input')
ln = content[:idx2].count('\n')+1
print(f'csv-file-input linha {ln}')

# 3. Verifica se tem tela de Pedidos com botão importar
idx3 = content.find('Importar Pedidos')
if idx3 != -1:
    ln3 = content[:idx3].count('\n')+1
    print(f'Importar Pedidos linha {ln3}: {repr(content[max(0,idx3-50):idx3+80])}')
