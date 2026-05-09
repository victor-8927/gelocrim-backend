path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona declarações globais logo após o início do Script 1
old = '''const API = 'http://localhost:8000/api/v1';
let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];'''

new = '''const API = 'http://localhost:8000/api/v1';
let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];
// ── Variáveis globais compartilhadas ──
var rotSelecionados = {};
var confOrdem = [];
var confMap = null;
var rotaConfirmada = false;
var _tgfiteTipo = null;
var _tgfiteNome = null;
var _tgfitePeso = null;
var _tgfiteDados = [];
var _clientesCache = {};
var _todosClientes = [];
var _allOrders = [];
var _csvDados = [];'''

if old in content:
    content = content.replace(old, new, 1)
    print('Variáveis globais adicionadas no Script 1!')
else:
    print('Padrão não encontrado!')
    idx = content.find("const API = 'http://localhost:8000/api/v1'")
    print(f'API const na linha: {content[:idx].count(chr(10))+1}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
