path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se o botão existe
if 'Importar CSV' in content:
    print('Botão já existe!')
else:
    print('Botão não encontrado, adicionando...')

# Verifica o header da tela de pedidos
import re
idx = content.find('page-pedidos')
print(content[idx:idx+500])
