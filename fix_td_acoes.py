path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

old = """          btnLiberar+
          '<button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">👁 Ver</button>'+
          (r.status!=='executing'&&r.status!=='done'?'<button class="btn btn-sm btn-danger" onclick="excluirRota(\\"'+r.route_id+'\\")" title="Excluir viagem">🗑️</button>':'')+
    }).join('');"""

new = """          btnLiberar+
          '<button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">👁 Ver</button>'+
          (r.status!=='executing'&&r.status!=='done'?'<button class="btn btn-sm btn-danger" onclick="excluirRota(\\"'+r.route_id+'\\")" title="Excluir viagem">🗑️</button>':'')+
          '</td>'+
        '</tr>';
    }).join('');"""

if old in content:
    content = content.replace(old, new)
    print('Corrigido!')
else:
    print('Padrão não encontrado, buscando...')
    idx = content.find("}).join('');")
    ln = content[:idx].count('\n')+1
    print(f'}).join linha {ln}')
    # Ver contexto
    lines = content.split('\n')
    for i in range(ln-5, ln+2):
        print(f'{i+1}: {repr(lines[i])}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'
import subprocess
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('Script 2 VALIDO! Ctrl+Shift+R')
else:
    print('ERRO:', stderr[:300])
