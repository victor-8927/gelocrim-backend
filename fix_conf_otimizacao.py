path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui as funções reprocessarSequencia e atualizarRotaMapa
old_reprocessar = """function reprocessarSequencia() {
  // Ordena por região/bairro para otimizar rota
  confOrdem.sort(function(a,b){
    var ra = a.regiao||a.bairro||'';
    var rb = b.regiao||b.bairro||'';
    return ra.localeCompare(rb);
  });
  renderizarListaConf();
  toast('Sequência reprocessada por região!', 'success');
}"""

new_reprocessar = """function reprocessarSequencia() {
  var modo = document.getElementById('conf-sequencia') ? document.getElementById('conf-sequencia').value : 'otimizado';
  var deposito = {lat: -3.093544, lng: -60.075812};

  if (modo === 'proximidade' || modo === 'otimizado' || modo === 'distancia') {
    // Algoritmo nearest neighbor a partir do depósito
    var restantes = confOrdem.slice();
    var ordenado = [];
    var atual = deposito;
    while (restantes.length > 0) {
      var melhorIdx = 0;
      var melhorDist = Infinity;
      restantes.forEach(function(o, i) {
        var lat = parseFloat(o.lat);
        var lng = parseFloat(o.lng);
        if (!lat || !lng) return;
        var dist = Math.sqrt(Math.pow(lat - atual.lat, 2) + Math.pow(lng - atual.lng, 2));
        if (dist < melhorDist) { melhorDist = dist; melhorIdx = i; }
      });
      var proximo = restantes.splice(melhorIdx, 1)[0];
      ordenado.push(proximo);
      atual = {lat: parseFloat(proximo.lat)||deposito.lat, lng: parseFloat(proximo.lng)||deposito.lng};
    }
    confOrdem = ordenado;
  } else if (modo === 'agrupamento') {
    // Agrupa por região/bairro
    confOrdem.sort(function(a,b){
      var ra = (a.regiao||a.bairro||'');
      var rb = (b.regiao||b.bairro||'');
      return ra.localeCompare(rb);
    });
  }

  renderizarListaConf();
  atualizarEtaConf();
  toast('Sequência otimizada!', 'success');
}"""

if old_reprocessar in content:
    content = content.replace(old_reprocessar, new_reprocessar)
    print('reprocessarSequencia atualizado!')
else:
    print('reprocessarSequencia não encontrado!')

# Substitui atualizarRotaMapa para usar Google Directions
old_atualizar = """function atualizarRotaMapa() {
  atualizarEtaConf();
  // Desenha rota no mapa de conferência
  if (!confMap) return;
  if (confMap._confMarkers) confMap._confMarkers.forEach(function(m){m.setMap(null);});
  if (confMap._confLine) confMap._confLine.setMap(null);
  confMap._confMarkers = [];

  var coords = [];
  var deposito = {lat: -3.093544, lng: -60.075812};
  coords.push(new google.maps.LatLng(deposito.lat, deposito.lng));

  confOrdem.forEach(function(o, i) {
    var lat = parseFloat(o.lat);
    var lng = parseFloat(o.lng);
    if (!lat || !lng) return;
    coords.push(new google.maps.LatLng(lat, lng));
    var mk = new google.maps.Marker({
      position: {lat:lat, lng:lng},
      map: confMap,
      label: { text: String(i+1), color:'#002855', fontWeight:'800', fontSize:'11px' },
      icon: { path: google.maps.SymbolPath.CIRCLE, scale:14, fillColor:'#64B4FF', fillOpacity:1, strokeColor:'#002855', strokeWeight:2 }
    });
    confMap._confMarkers.push(mk);
  });

  coords.push(new google.maps.LatLng(deposito.lat, deposito.lng));

  if (coords.length > 1) {
    confMap._confLine = new google.maps.Polyline({
      path: coords, geodesic:true,
      strokeColor:'#64B4FF', strokeOpacity:0.8, strokeWeight:3, map:confMap
    });
    var bounds = new google.maps.LatLngBounds();
    coords.forEach(function(c){bounds.extend(c);});
    confMap.fitBounds(bounds);
  }

  toast('Rota atualizada no mapa!', 'success');
}"""

new_atualizar = """async function atualizarRotaMapa() {
  atualizarEtaConf();
  if (!confMap) return;

  // Limpa marcadores e rotas anteriores
  if (confMap._confMarkers) confMap._confMarkers.forEach(function(m){m.setMap(null);});
  if (confMap._confDirections) confMap._confDirections.setMap(null);
  if (confMap._confLine) confMap._confLine.setMap(null);
  confMap._confMarkers = [];

  var deposito = {lat: -3.093544, lng: -60.075812};
  var validos = confOrdem.filter(function(o){ return parseFloat(o.lat) && parseFloat(o.lng); });

  if (validos.length === 0) { toast('Nenhum cliente com GPS!', 'error'); return; }

  // Adiciona marcador do depósito
  new google.maps.Marker({
    position: deposito, map: confMap,
    icon: { path: google.maps.SymbolPath.CIRCLE, scale:12, fillColor:'#e8521a', fillOpacity:1, strokeColor:'#fff', strokeWeight:2 },
    title: 'Depósito Gelocrim'
  });

  // Adiciona marcadores numerados dos clientes
  validos.forEach(function(o, i) {
    var lat = parseFloat(o.lat);
    var lng = parseFloat(o.lng);
    var mk = new google.maps.Marker({
      position: {lat:lat, lng:lng}, map: confMap,
      label: { text: String(i+1), color:'#002855', fontWeight:'800', fontSize:'11px' },
      icon: { path: google.maps.SymbolPath.CIRCLE, scale:14, fillColor:'#64B4FF', fillOpacity:1, strokeColor:'#002855', strokeWeight:2 },
      title: o.recipient_name || o.nome || ''
    });
    confMap._confMarkers.push(mk);
  });

  // Traça rota pelas ruas usando Directions API
  toast('Calculando rota pelas ruas...', 'info');
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer({
    map: confMap,
    suppressMarkers: true,
    polylineOptions: { strokeColor:'#64B4FF', strokeWeight:4, strokeOpacity:0.9 }
  });
  confMap._confDirections = directionsRenderer;

  // Google Directions suporta max 25 waypoints
  var origem = deposito;
  var destino = deposito;
  var waypoints = validos.slice(0, 23).map(function(o) {
    return { location: new google.maps.LatLng(parseFloat(o.lat), parseFloat(o.lng)), stopover: true };
  });

  directionsService.route({
    origin: new google.maps.LatLng(origem.lat, origem.lng),
    destination: new google.maps.LatLng(destino.lat, destino.lng),
    waypoints: waypoints,
    optimizeWaypoints: false,
    travelMode: google.maps.TravelMode.DRIVING,
    region: 'br'
  }, function(result, status) {
    if (status === 'OK') {
      directionsRenderer.setDirections(result);
      // Atualiza ETA com distâncias reais
      var legs = result.routes[0].legs;
      var minutos = (function(){
        var h = document.getElementById('conf-hora-inicio');
        var v = h ? h.value : '07:30';
        var p = v.split(':').map(Number);
        return p[0]*60 + p[1];
      })();
      confOrdem.forEach(function(o, i) {
        if (i < legs.length) {
          var duracaoMin = Math.round(legs[i].duration.value / 60);
          var tempoParada = parseInt(o.tempo_entrega || 15);
          minutos += duracaoMin + tempoParada;
          var h2 = Math.floor(minutos/60) % 24;
          var m2 = minutos % 60;
          o._eta = String(h2).padStart(2,'0')+':'+String(m2).padStart(2,'0');
        }
      });
      renderizarListaConf();
      // Atualiza previsão fim
      var ultimo = confOrdem.filter(function(o){return o._eta;});
      if (ultimo.length) {
        var fimEl = document.getElementById('conf-hora-fim');
        if (fimEl) fimEl.textContent = ultimo[ultimo.length-1]._eta;
      }
      toast('Rota traçada pelas ruas! ETAs calculados.', 'success');
      // Habilita confirmar rota
      var bC = document.getElementById('btn-confirmar-rota');
      if (bC) { bC.disabled=false; bC.style.opacity='1'; bC.style.cursor='pointer'; bC.style.background='rgba(16,185,129,.2)'; bC.style.borderColor='#10b981'; bC.style.color='#10b981'; }
    } else {
      toast('Directions API: '+status+' — verifique GPS dos clientes', 'warn');
      // Fallback: linha reta
      var coords = [new google.maps.LatLng(deposito.lat, deposito.lng)];
      validos.forEach(function(o){ coords.push(new google.maps.LatLng(parseFloat(o.lat), parseFloat(o.lng))); });
      coords.push(new google.maps.LatLng(deposito.lat, deposito.lng));
      confMap._confLine = new google.maps.Polyline({ path:coords, strokeColor:'#f59e0b', strokeWeight:3, strokeOpacity:0.7, map:confMap });
      var bounds = new google.maps.LatLngBounds();
      coords.forEach(function(c){bounds.extend(c);});
      confMap.fitBounds(bounds);
    }
  });
}"""

if old_atualizar in content:
    content = content.replace(old_atualizar, new_atualizar)
    print('atualizarRotaMapa atualizado com Directions API!')
else:
    print('atualizarRotaMapa não encontrado!')

# Adiciona listener no select de sequência
old_confirmar = """function confirmarRota() {"""
new_confirmar = """// Listener para mudança de sequência
document.addEventListener('DOMContentLoaded', function() {
  var selSeq = document.getElementById('conf-sequencia');
  if (selSeq) selSeq.addEventListener('change', function(){ reprocessarSequencia(); });
  var selMod = document.getElementById('conf-modelo');
  if (selMod) selMod.addEventListener('change', function(){
    toast('Modelo: ' + this.options[this.selectedIndex].text, 'info');
  });
});

function confirmarRota() {"""

if old_confirmar in content and 'addEventListener' not in content[content.find(old_confirmar)-200:content.find(old_confirmar)]:
    content = content.replace(old_confirmar, new_confirmar, 1)
    print('Listeners adicionados!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re, subprocess
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
    print('ERRO:', stderr[:400])
    m = re.search(r':(\d+)\n', stderr)
    if m:
        ln = int(m.group(1))
        js_lines = (stub+'\n'+js).split('\n')
        for x in range(max(0,ln-3), min(len(js_lines),ln+2)):
            print(f'{x+1}: {repr(js_lines[x])}')
