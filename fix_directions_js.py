path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

GMAPS_KEY = 'AIzaSyB47DpEZW4qbU74LxcG1ZD76cYLRlJw88M'

idx_start = content.find('async function atualizarRotaMapa()')
idx_end   = content.find('\nasync function gravarCarga')
print(f'Substituindo linhas {content[:idx_start].count(chr(10))+1} a {content[:idx_end].count(chr(10))+1}')

new_func = r"""async function atualizarRotaMapa() {
  if (!confMap) { toast('Mapa não inicializado!', 'error'); return; }

  // Limpa camadas anteriores
  if (confMap._confMarkers) confMap._confMarkers.forEach(function(m){m.setMap(null);});
  if (confMap._confLine) { confMap._confLine.setMap(null); confMap._confLine = null; }
  if (confMap._confDirections) { try { confMap._confDirections.setMap(null); } catch(e){} confMap._confDirections = null; }
  confMap._confMarkers = [];

  var DEPOSITO = {lat: -3.093544, lng: -60.075812};
  var validos = confOrdem.filter(function(o){ return parseFloat(o.lat) && parseFloat(o.lng); });

  if (!validos.length) { toast('Nenhum cliente com GPS válido!', 'error'); return; }

  var bounds = new google.maps.LatLngBounds();

  // Marcador depósito
  var mkDep = new google.maps.Marker({
    position: DEPOSITO, map: confMap, zIndex: 999,
    icon: { path: google.maps.SymbolPath.CIRCLE, scale:14,
      fillColor:'#e8521a', fillOpacity:1, strokeColor:'#fff', strokeWeight:2 },
    title: 'Depósito Gelocrim'
  });
  confMap._confMarkers.push(mkDep);
  bounds.extend(new google.maps.LatLng(DEPOSITO.lat, DEPOSITO.lng));

  // Marcadores numerados
  validos.forEach(function(o, i) {
    var mk = new google.maps.Marker({
      position: {lat: parseFloat(o.lat), lng: parseFloat(o.lng)},
      map: confMap, zIndex: 100+i,
      label: { text: String(i+1), color:'#002855', fontWeight:'800', fontSize:'11px' },
      icon: { path: google.maps.SymbolPath.CIRCLE, scale:15,
        fillColor:'#64B4FF', fillOpacity:1, strokeColor:'#002855', strokeWeight:2 },
      title: (o.recipient_name||'') + (o._eta ? ' — ETA: '+o._eta : '')
    });
    confMap._confMarkers.push(mk);
    bounds.extend(new google.maps.LatLng(parseFloat(o.lat), parseFloat(o.lng)));
  });
  confMap.fitBounds(bounds);

  toast('Calculando rota pelas estradas...', 'info');

  try {
    // Usa Directions API via fetch (sem SDK JS)
    var GMAPS_KEY = 'AIzaSyB47DpEZW4qbU74LxcG1ZD76cYLRlJw88M';
    var origem  = DEPOSITO.lat + ',' + DEPOSITO.lng;
    var destino = DEPOSITO.lat + ',' + DEPOSITO.lng;

    // Waypoints (máx 23 intermediários)
    var wpsArr = validos.slice(0, 23).map(function(o){
      return parseFloat(o.lat)+','+parseFloat(o.lng);
    });
    var wpsStr = wpsArr.join('|');

    var url = 'https://maps.googleapis.com/maps/api/directions/json' +
      '?origin=' + origem +
      '&destination=' + destino +
      '&waypoints=' + encodeURIComponent(wpsStr) +
      '&mode=driving&region=br&language=pt-BR' +
      '&key=' + GMAPS_KEY;

    var res  = await fetch(url);
    var data = await res.json();

    if (data.status !== 'OK') {
      throw new Error('Directions API: ' + data.status + ' — ' + (data.error_message||''));
    }

    var route = data.routes[0];
    var legs  = route.legs; // 1 leg por waypoint + retorno

    // Decodifica polyline e desenha
    function decodePolyline(encoded) {
      var poly = [], index = 0, lat = 0, lng = 0;
      while (index < encoded.length) {
        var shift = 0, result = 0, b;
        do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
        lat += (result & 1) ? ~(result >> 1) : (result >> 1);
        shift = 0; result = 0;
        do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
        lng += (result & 1) ? ~(result >> 1) : (result >> 1);
        poly.push({lat: lat/1e5, lng: lng/1e5});
      }
      return poly;
    }

    var pts = [];
    legs.forEach(function(leg){
      leg.steps.forEach(function(step){
        pts = pts.concat(decodePolyline(step.polyline.points));
      });
    });

    confMap._confLine = new google.maps.Polyline({
      path: pts, map: confMap, geodesic: false,
      strokeColor: '#64B4FF', strokeOpacity: 0.9, strokeWeight: 4
    });

    // Calcula ETAs com duração real de cada leg
    var horaEl = document.getElementById('conf-hora-inicio');
    var horaStr = horaEl ? horaEl.value : '07:30';
    var partes = horaStr.split(':').map(Number);
    var minTotais = partes[0]*60 + partes[1];

    var distTotal = 0;
    confOrdem.forEach(function(o, i) {
      if (i < legs.length) {
        var duracaoMin = Math.round(legs[i].duration.value / 60);
        var tempoParada = parseInt(o.tempo_entrega || 15);
        distTotal += legs[i].distance.value;
        minTotais += duracaoMin + tempoParada;
        var h = Math.floor(minTotais/60) % 24;
        var m = minTotais % 60;
        o._eta = String(h).padStart(2,'0')+':'+String(m).padStart(2,'0');
      }
    });

    // Atualiza indicadores
    var kmTotal = (distTotal/1000).toFixed(1);
    var fimEl = document.getElementById('conf-hora-fim');
    var ultimo = confOrdem.filter(function(o){return o._eta;});
    if (fimEl && ultimo.length) fimEl.textContent = ultimo[ultimo.length-1]._eta;
    var distEl = document.getElementById('conf-distancia');
    if (distEl) distEl.textContent = kmTotal + ' km';

    renderizarListaConf();

    // Habilita Confirmar Rota
    var bC = document.getElementById('btn-confirmar-rota');
    if (bC) {
      bC.disabled=false; bC.style.opacity='1'; bC.style.cursor='pointer';
      bC.style.background='rgba(16,185,129,.2)';
      bC.style.borderColor='#10b981'; bC.style.color='#10b981';
    }

    toast('Rota: '+kmTotal+'km · ETAs calculados pela BR-174!', 'success');

  } catch(err) {
    console.error('Directions erro:', err);
    toast('Erro: ' + err.message, 'error');
  }
}
"""

content = content[:idx_start] + new_func + content[idx_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re, subprocess
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){return{lat:0,lng:0};},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){return Promise.resolve({json:function(){return Promise.resolve({status:"OK",routes:[{legs:[],overview_polyline:{points:""}}]});}})}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('VÁLIDO! Ctrl+Shift+R')
else:
    print('ERRO:', stderr[:400])
    m = re.search(r':(\d+)\n', stderr)
    if m:
        ln = int(m.group(1))
        js_lines = (stub+'\n'+js).split('\n')
        for x in range(max(0,ln-3), min(len(js_lines),ln+2)):
            print(f'{x+1}: {repr(js_lines[x])}')
