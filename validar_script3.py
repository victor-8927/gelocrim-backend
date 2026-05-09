path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
scripts = list(re.finditer(r'<script[^>]*>', content))
closes  = list(re.finditer(r'</script>', content))

# Extrai script 3 (índice 2)
start = scripts[2].end()
end   = closes[2].start()
script3 = content[start:end]
print(f'Script 3: {len(script3)} chars')

with open(r'C:\fleet-cloud\test_s3.js', 'w', encoding='utf-8') as f:
    f.write('var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.getTitle=function(){return "";};},SymbolPath:{CIRCLE:0},InfoWindow:function(){this.open=function(){};this.close=function(){};},event:{trigger:function(){}}}};function api(){}function toast(){}function initMap(){return new google.maps.Map();}function addMarker(){}function atualizarSelecaoRot(){}var rotSelecionados={};\n')
    f.write(script3)

import subprocess
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s3.js'],capture_output=True,text=True)
if r.returncode==0:
    print('Script 3 VALIDO!')
else:
    print('ERRO:')
    print(r.stderr[:1000])
