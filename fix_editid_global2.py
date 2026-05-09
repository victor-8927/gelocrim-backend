path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona _editVeiculoId no script principal (script 3 - o grande)
# Adiciona junto com as outras variáveis globais no início do script principal
old = """let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];"""

new = """let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];
var _editVeiculoId = null;
var _editMotoId = null;"""

if old in content:
    content = content.replace(old, new)
    print('Variáveis globais adicionadas no script principal!')
else:
    print('Padrão não encontrado!')

# Remove declaração duplicada do script 4
old2 = "var rotSelecionados = {};\nvar _editVeiculoId = null;"
new2 = "var rotSelecionados = {};"
if old2 in content:
    content = content.replace(old2, new2)
    print('Declaração duplicada removida do script 4!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
