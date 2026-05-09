path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """      'onmouseover="this.style.background=\\'#1e3a5c\\'" onmouseout="this.style.background=\\'#0a1628\\'">'+"""

new = """      'onmouseover="this.style.background=&quot;#1e3a5c&quot;" onmouseout="this.style.background=&quot;#0a1628&quot;">'+"""

# Busca e substitui o trecho problemático
import re

old2 = r"""'onmouseover="this.style.background=\'#1e3a5c\'" onmouseout="this.style.background=\'#0a1628\'">'+"""
new2 = """'onmouseover="this.style.background=\'#1e3a5c\'" onmouseout="this.style.background=\'#0a1628\'">'+ """

# Substitui direto no texto
content = content.replace(
    "onmouseover=\"this.style.background='#1e3a5c'\" onmouseout=\"this.style.background='#0a1628'\">'+",
    "onmouseover=\"this.style.background='#1e3a5c'\" onmouseout=\"this.style.background='#0a1628'\">'+".replace("'#1e3a5c'", "\\'#1e3a5c\\'").replace("'#0a1628'", "\\'#0a1628\\'")
)

# Abordagem mais simples - encontra a linha e substitui
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'onmouseover' in line and '#1e3a5c' in line and 'conf-item' in content[max(0, content.find(line)-200):content.find(line)+200]:
        # Substitui aspas simples dentro de atributos HTML por versão escapada
        lines[i] = line.replace(
            """onmouseover="this.style.background='#1e3a5c'" onmouseout="this.style.background='#0a1628'">'+""",
            """onmouseover="this.style.background=\\'#1e3a5c\\'" onmouseout="this.style.background=\\'#0a1628\\'">'+"""
        )
        print(f'Linha {i+1} corrigida!')
        break

content = '\n'.join(lines)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
import subprocess
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){return{};},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('VÁLIDO! Ctrl+Shift+R')
else:
    print('ERRO:', stderr[:300])
    # Mostra linha do erro
    m = re.search(r':(\d+)\n', stderr)
    if m:
        ln = int(m.group(1))
        js_lines = (stub+'\n'+js).split('\n')
        for x in range(max(0,ln-2), min(len(js_lines),ln+2)):
            print(f'{x+1}: {repr(js_lines[x])}')
