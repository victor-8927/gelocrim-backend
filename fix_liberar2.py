path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Substitui o bloco btnLiberar inteiro por versão correta
old = re.search(r"var btnLiberar='';\s+if\(r\.status==='optimized'\)\{[^}]+\}", content)
if old:
    print(f'Encontrado: {repr(old.group(0)[:100])}')
    new_block = (
        "var btnLiberar='';\n"
        "      if(r.status==='optimized'){\n"
        "        btnLiberar='<button class=\"btn btn-sm\" style=\"background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981\" onclick=\"liberarRota(\\\"'+r.route_id+'\\\")\" title=\"Liberar\">🟢 Liberar</button>';\n"
        "      }"
    )
    content = content[:old.start()] + new_block + content[old.end():]
    print('Substituído!')
else:
    print('Bloco não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
import subprocess
lines = content.split('\n')
script4 = '\n'.join(lines[3942:5650]).replace('<script>','').replace('</script>','')
stub = 'var XLSX={read:function(){return{SheetNames:["s"],Sheets:{"s":{}}};},utils:{sheet_to_json:function(){return[];}}};var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},Map:function(){this.fitBounds=function(){};},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};function api(){}function toast(){}function initMap(){return null;}function addMarker(){}function closeModal(){}function openModal(){}function goTo(){}var token="";var maps={};var confOrdem=[];var confMap=null;var rotaConfirmada=false;var rotSelecionados={};var _tgfiteTipo=null;var _tgfiteNome=null;var _tgfitePeso=null;var _tgfiteDados=[];'
with open(r'C:\fleet-cloud\test_s4.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + script4)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s4.js'],capture_output=True,text=True)
if r.returncode==0:
    print('Script 4 VALIDO!')
else:
    print('ERRO:', r.stderr[:400])
