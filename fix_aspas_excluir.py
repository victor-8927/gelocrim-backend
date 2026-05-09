path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Substitui o bloco do botão excluir com aspas corretas
old = re.search(r"\(r\.status!=='executing'&&r\.status!=='done'\?'<button[^']*excluirRota[^;]+;", content)
if old:
    print(f'Encontrado: {repr(old.group(0)[:100])}')
    new_btn = "(r.status!=='executing'&&r.status!=='done'?'<button class=\"btn btn-sm btn-danger\" onclick=\"excluirRota(\\\"'+r.route_id+'\\\")\" title=\"Excluir viagem\">🗑️</button>':'')+"
    content = content[:old.start()] + new_btn + content[old.end():]
    print('Corrigido!')
else:
    print('Não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
import subprocess
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('Script 2 VALIDO!')
else:
    print('ERRO:', stderr[:300])
