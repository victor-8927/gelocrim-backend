path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """'onclick="liberarRota(\\'\\'+r.route_id+\\'\\')"\"""
# Busca o trecho exato
import re
m = re.search(r"onclick=\"liberarRota\([^)]+\)\"", content)
if m:
    ln = content[:m.start()].count('\n')+1
    print(f'Encontrado linha {ln}: {repr(m.group(0))}')

# Corrige a linha do btnLiberar
old_btn = """'<button class="btn btn-sm" style="background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981" '+
          'onclick="liberarRota(\\'\\'+r.route_id+'\\'\\'" title="Liberar para motorista">🟢 Liberar</button>';"""

# Busca por trecho identificador
idx = content.find("onclick=\"liberarRota(")
if idx != -1:
    ln = content[:idx].count('\n')+1
    print(f'liberarRota onclick linha {ln}')
    # Pega contexto
    ctx = content[max(0,idx-50):idx+100]
    print(f'Contexto: {repr(ctx)}')

# Substitui a linha problemática de forma mais segura
old_liberar = """'onclick="liberarRota(\'\''+r.route_id+'\''\')" title="Liberar para motorista">🟢 Liberar</button>';"""

# Vamos encontrar e substituir o bloco btnLiberar inteiro
old_block = """var btnLiberar='';
      if(r.status==='optimized'){
        btnLiberar='<button class="btn btn-sm" style="background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981" '+
          'onclick="liberarRota(\\'\\'+r.route_id+'\\'\\'" title="Liberar para motorista">🟢 Liberar</button>';
      }"""

new_block = """var btnLiberar='';
      if(r.status==='optimized'){
        btnLiberar='<button class="btn btn-sm" style="background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981" onclick="liberarRota(\\'' + r.route_id + '\\')" title="Liberar para motorista">🟢 Liberar</button>';
      }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print('Corrigido!')
else:
    # Busca e substitui por regex
    content = re.sub(
        r"btnLiberar='<button[^']*liberarRota[^;]+;",
        "btnLiberar='<button class=\"btn btn-sm\" style=\"background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981\" onclick=\"liberarRota(\\'' + r.route_id + '\\')\" title=\"Liberar para motorista\">🟢 Liberar</button>';",
        content
    )
    print('Corrigido via regex!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
import subprocess
lines = content.split('\n')
script4 = '\n'.join(lines[3942:5650])
script4 = script4.replace('<script>', '').replace('</script>', '')
with open(r'C:\fleet-cloud\test_script4.js', 'w', encoding='utf-8') as f:
    f.write('var XLSX={read:function(){return{SheetNames:["s"],Sheets:{"s":{}}};},utils:{sheet_to_json:function(){return[];}}};var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},Map:function(){this.fitBounds=function(){};},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};function api(){}function toast(){}function initMap(){return null;}function addMarker(){}function closeModal(){}function openModal(){}function goTo(){}function loadRoutes(){}var token="";var maps={};var confOrdem=[];var confMap=null;var rotaConfirmada=false;var rotSelecionados={};var _tgfiteTipo=null;var _tgfiteNome=null;var _tgfitePeso=null;var _tgfiteDados=[];\n')
    f.write(script4)

result = subprocess.run(['node','--check',r'C:\fleet-cloud\test_script4.js'],capture_output=True,text=True)
if result.returncode==0:
    print('Script 4 VÁLIDO!')
else:
    print('ERRO:', result.stderr[:500])
