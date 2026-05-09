path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Ver rotSelecionados declaração e uso
import re

# Declaração da variável
idx = content.find('rotSelecionados')
print('=== Declaração rotSelecionados ===')
print(content[max(0,idx-100):idx+200])

# Ver rotTogglePedido - onde os pedidos são adicionados
idx2 = content.find('function rotTogglePedido(')
print('\n=== rotTogglePedido ===')
print(content[idx2:idx2+600])

# Ver rotAtualizarSidebar
idx3 = content.find('function rotAtualizarSidebar(')
print('\n=== rotAtualizarSidebar ===')
print(content[idx3:idx3+500])
