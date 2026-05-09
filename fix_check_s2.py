path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re, subprocess

scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)

stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'

with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)

r = subprocess.run(
    ['node','--check',r'C:\fleet-cloud\test_s2.js'],
    capture_output=True
)
stdout = r.stdout.decode('utf-8', errors='replace')
stderr = r.stderr.decode('utf-8', errors='replace')

if r.returncode == 0:
    print('Script 2 VALIDO!')
else:
    print('ERRO Script 2:')
    print(stderr[:500])
    # Acha linha do erro
    m = re.search(r':(\d+)\n', stderr)
    if m:
        ln_err = int(m.group(1))
        js_lines = (stub+'\n'+js).split('\n')
        for x in range(max(0,ln_err-3), min(len(js_lines),ln_err+2)):
            print(f'{x+1}: {repr(js_lines[x])}')
