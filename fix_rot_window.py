path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Garante que rotSelecionados é declarado como window no script principal
old = """let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];
var _editVeiculoId = null;
var _editMotoId = null;"""

new = """let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];
var _editVeiculoId = null;
var _editMotoId = null;
window.rotSelecionados = {};
window._rotMapMarkers = [];
window._rotOrdersCache = [];"""

if old in content:
    content = content.replace(old, new)
    print('window.rotSelecionados declarado!')
else:
    print('Padrão não encontrado!')

# Substitui todas as referências a rotSelecionados por window.rotSelecionados
# no renderRotMapMarkers
import re

# Conta quantas vezes rotSelecionados aparece sem window.
count = len(re.findall(r'(?<!window\.)rotSelecionados', content))
print(f'rotSelecionados sem window.: {count}')

# Substitui no renderRotMapMarkers e selecionarTodaRota
# Encontra as funções no script 3
for fn_name in ['renderRotMapMarkers', 'selecionarTodaRota', 'filtrarRotMapa', 'atualizarSelecaoRot', 'rotLimparTudo']:
    idx = content.find('function '+fn_name)
    while idx != -1:
        # Encontra fim da função
        depth = 0
        i = idx
        while i < len(content):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
            i += 1
        fn_body = content[idx:end]
        # Substitui rotSelecionados por window.rotSelecionados dentro da função
        new_body = re.sub(r'(?<!window\.)rotSelecionados', 'window.rotSelecionados', fn_body)
        if new_body != fn_body:
            content = content[:idx] + new_body + content[end:]
            print(f'  {fn_name}: rotSelecionados → window.rotSelecionados')
        idx = content.find('function '+fn_name, end)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
