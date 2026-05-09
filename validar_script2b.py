path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('<script>\nvar _clientesCache')
end   = content.find('</script>', start)
script2 = content[start+8:end]

with open(r'C:\fleet-cloud\test_script2.js', 'w', encoding='utf-8') as f:
    f.write('''
var XLSX = {};
var google = {maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};},SymbolPath:{CIRCLE:0},event:{trigger:function(){}}}};
function api(){}
function toast(){}
function initMap(){return null;}
function addMarker(){}
function closeModal(){}
function openModal(){}
function loadDashboard(){}
function loadRoutes(){}
''')
    f.write(script2)

import subprocess
result = subprocess.run(
    ['node', '--check', r'C:\fleet-cloud\test_script2.js'],
    capture_output=True, text=True
)
if result.returncode == 0:
    print('Script JS VALIDO! Sem erros de sintaxe.')
else:
    print('ERRO DE SINTAXE:')
    print(result.stderr[:3000])
