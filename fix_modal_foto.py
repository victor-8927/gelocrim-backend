path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a linha da hora no modal para incluir foto
old = """        '<td style="padding:8px;text-align:center;font-size:12px;color:#90afd4">'+hora+'</td>'+
      '</tr>';"""

new = """        '<td style="padding:8px;text-align:center;font-size:12px;color:#90afd4">'+hora+'</td>'+
        '<td style="padding:8px;text-align:center">'+
          (s.foto_url
            ? '<img src="'+s.foto_url+'" style="width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid #1e3a5c;cursor:pointer" onclick="window.open(this.src)" title="Ver foto">'
            : (s.status==="completed"?'<span style="font-size:10px;color:#90afd4">sem foto</span>':''))+
        '</td>'+
      '</tr>';"""

if old in content:
    content = content.replace(old, new)
    print('Coluna foto adicionada!')
else:
    print('Padrão não encontrado!')

# Adiciona cabeçalho da coluna foto
old2 = """          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">Hora</th>'+"""
new2 = """          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">Hora</th>'+
          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">Canhoto</th>'+"""

if old2 in content:
    content = content.replace(old2, new2)
    print('Cabeçalho foto adicionado!')
else:
    print('Cabeçalho não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re, subprocess
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('VALIDO! Agora vamos ao app motorista.')
else:
    print('ERRO:', stderr[:300])
