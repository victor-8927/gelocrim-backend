path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extrai o segundo script
start = content.find('<script>\nvar _clientesCache')
end   = content.find('</script>', start)
script2 = content[start+8:end]

# Salva para testar com node
with open(r'C:\fleet-cloud\test_script2.js', 'w', encoding='utf-8') as f:
    # Adiciona stubs para funções externas
    f.write('''
// Stubs
var XLSX={};
function api(){}
function toast(){}
function initMap(){}
function addMarker(){}
function google={maps:{Marker:function(){return {addListener:function(){},setIcon:function(){}}},SymbolPath:{CIRCLE:0}}};
var google = {maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};},SymbolPath:{CIRCLE:0},event:{trigger:function(){}}}};
''')
    f.write(script2)

import subprocess
result = subprocess.run(
    ['node', r'C:\fleet-cloud\test_script2.js'],
    capture_output=True, text=True, cwd=r'C:\fleet-cloud'
)
if result.returncode == 0:
    print('Script JS VALIDO!')
else:
    print('ERRO JS:')
    print(result.stderr[:2000])
