path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extrai script 4 (linha 3943 até 5646)
lines = content.split('\n')
script4 = '\n'.join(lines[3942:5645])

# Remove a tag <script> inicial
script4 = script4.replace('<script>', '').replace('</script>', '')

# Salva para testar com node
with open(r'C:\fleet-cloud\test_script4.js', 'w', encoding='utf-8') as f:
    # Adiciona stubs necessários
    f.write('''
var XLSX={read:function(){return{SheetNames:['s'],Sheets:{s:{}}};},utils:{sheet_to_json:function(){return[];}}};
var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},
  SymbolPath:{CIRCLE:0},Map:function(){this.fitBounds=function(){};},
  LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},
  LatLng:function(){},DirectionsService:function(){this.route=function(){};},
  DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},
  TrafficLayer:function(){this.setMap=function(){};},
  TravelMode:{DRIVING:'DRIVING'},Polyline:function(){this.setMap=function(){};},
  InfoWindow:function(){this.open=function(){};},
  event:{trigger:function(){}}}};
function api(){}function toast(){}function initMap(){return null;}function addMarker(){}
function closeModal(){}function openModal(){}function goTo(){}function loadRoutes(){}
var token='';var maps={};var confOrdem=[];var confMap=null;var rotaConfirmada=false;
var rotSelecionados={};var _tgfiteTipo=null;var _tgfiteNome=null;var _tgfitePeso=null;
var _tgfiteDados=[];
''')
    f.write(script4)

import subprocess
result = subprocess.run(
    ['node', '--check', r'C:\fleet-cloud\test_script4.js'],
    capture_output=True, text=True
)
if result.returncode == 0:
    print('Script 4 VÁLIDO!')
else:
    print('ERRO no Script 4:')
    print(result.stderr[:800])
