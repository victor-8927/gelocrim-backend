path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove declarações duplicadas do Script 2
dups = [
    'var rotSelecionados = {};',
    'var confOrdem = [];',
    'var confMap = null;',
    'var rotaConfirmada = false;',
    'var _tgfiteTipo = null;',
    'var _tgfiteNome = null;',
    'var _tgfitePeso = null;',
    'var _tgfiteDados = [];',
    'var _clientesCache = {};',
    'var _todosClientes = [];',
    'var _allOrders = [];',
    'var _csvDados  = [];',
    'var _csvDados = [];',
]

# O Script 2 começa na linha 3943
# Precisamos remover apenas a segunda ocorrência de cada var
for var in dups:
    first = content.find(var)
    if first == -1:
        continue
    second = content.find(var, first + 1)
    if second != -1:
        content = content[:second] + content[second+len(var):]
        print(f'Removida duplicata: {var.strip()}')

# Também remove let confMap e let confOrdem se existirem
import re
for var in ['confMap', 'confOrdem', 'rotaConfirmada']:
    # Remove 'let varname = ...' no script 1 se existir (mantém só o var global)
    content = re.sub(r'\nlet ' + var + r' = [^;]+;', '', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
