path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re, subprocess

scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[0].group(1)  # Script 1 (linha 2543)

stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};},SymbolPath:{CIRCLE:0},InfoWindow:function(){this.open=function(){};},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}function parseInt(x){return x;}function parseFloat(x){return x;}'

with open(r'C:\fleet-cloud\test_s1.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)

r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s1.js'],capture_output=True,text=True)
if r.returncode==0:
    print('Script 1 VALIDO!')
else:
    err = r.stderr
    print('ERRO:', err[:400])
    m = re.search(r':(\d+)\n', err)
    if m:
        ln = int(m.group(1))
        js_lines = (stub+'\n'+js).split('\n')
        for i in range(max(0,ln-3), min(len(js_lines),ln+2)):
            print(f'{i+1}: {repr(js_lines[i])}')
