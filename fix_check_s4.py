path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re, subprocess

# Extrai o Script 4 corretamente entre <script> e </script>
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
print(f'Scripts encontrados: {len(scripts)}')
for i, s in enumerate(scripts):
    ln = content[:s.start()].count('\n')+1
    print(f'  Script {i+1}: linha {ln}, tamanho {len(s.group(1))} chars')

# Testa o script 4 (índice 3)
if len(scripts) >= 4:
    js = scripts[3].group(1)
    stub = 'var XLSX={read:function(){return{SheetNames:["s"],Sheets:{"s":{}}};},utils:{sheet_to_json:function(){return[];}}};var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},Map:function(){this.fitBounds=function(){};},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};function api(){}function toast(){}function initMap(){return null;}function addMarker(){}function closeModal(){}function openModal(){}function goTo(){}var token="";var maps={};var confOrdem=[];var confMap=null;var rotaConfirmada=false;var rotSelecionados={};var _tgfiteTipo=null;var _tgfiteNome=null;var _tgfitePeso=null;var _tgfiteDados=[];'
    with open(r'C:\fleet-cloud\test_s4.js', 'w', encoding='utf-8') as f:
        f.write(stub + '\n' + js)
    r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s4.js'],capture_output=True,text=True)
    if r.returncode==0:
        print('Script 4 VALIDO!')
    else:
        # Mostra linha do erro
        err = r.stderr
        print('ERRO:', err[:300])
        # Tenta encontrar linha problemática
        m = re.search(r':(\d+)\n', err)
        if m:
            ln = int(m.group(1))
            js_lines = (stub+'\n'+js).split('\n')
            print(f'Linha {ln}: {repr(js_lines[ln-1])}')
            print(f'Linha {ln-1}: {repr(js_lines[ln-2])}')
