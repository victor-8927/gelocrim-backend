path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver função setModoSelecao
idx = content.find('function setModoSelecao(')
print('=== setModoSelecao ===')
print(content[idx:idx+600])

# Ver função rotAtualizarTotais
idx2 = content.find('function rotAtualizarTotais(')
print('\n=== rotAtualizarTotais ===')
print(content[idx2:idx2+400])

# Ver função abrirConferenciaMaster
idx3 = content.find('function abrirConferenciaMaster(')
print('\n=== abrirConferenciaMaster ===')
print(content[idx3:idx3+300])

# Ver rotSelectedOrders
idx4 = content.find('rotSelectedOrders')
print('\n=== rotSelectedOrders ===')
print(content[max(0,idx4-50):idx4+200])
