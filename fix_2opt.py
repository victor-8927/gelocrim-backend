path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """function reprocessarSequencia() {
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

new = """// Distância euclidiana entre dois pontos
function distLatLng(a, b) {
  var dlat = (parseFloat(a.lat)||0) - (parseFloat(b.lat)||0);
  var dlng = (parseFloat(a.lng)||0) - (parseFloat(b.lng)||0);
  return Math.sqrt(dlat*dlat + dlng*dlng);
}

// Distância total da rota incluindo depósito
function distanciaTotal(rota, deposito) {
  var total = 0;
  var prev = deposito;
  rota.forEach(function(o) { total += distLatLng(prev, o); prev = o; });
  total += distLatLng(prev, deposito);
  return total;
}

// Algoritmo 2-opt: melhora a rota invertendo segmentos
function otimizar2opt(rota, deposito) {
  var melhorou = true;
  var melhor = rota.slice();
  while (melhorou) {
    melhorou = false;
    for (var i = 0; i < melhor.length - 1; i++) {
      for (var j = i + 1; j < melhor.length; j++) {
        // Inverte segmento entre i e j
        var nova = melhor.slice(0, i)
          .concat(melhor.slice(i, j+1).reverse())
          .concat(melhor.slice(j+1));
        if (distanciaTotal(nova, deposito) < distanciaTotal(melhor, deposito)) {
          melhor = nova;
          melhorou = true;
        }
      }
    }
  }
  return melhor;
}

// Nearest neighbor como ponto de partida
function nearestNeighbor(pontos, deposito) {
  var restantes = pontos.slice();
  var ordenado = [];
  var atual = deposito;
  while (restantes.length > 0) {
    var melhorIdx = 0;
    var melhorDist = Infinity;
    restantes.forEach(function(o, i) {
      if (!parseFloat(o.lat) || !parseFloat(o.lng)) return;
      var dist = distLatLng(atual, o);
      if (dist < melhorDist) { melhorDist = dist; melhorIdx = i; }
    });
    var prox = restantes.splice(melhorIdx, 1)[0];
    ordenado.push(prox);
    atual = prox;
  }
  return ordenado;
}

function reprocessarSequencia() {
  var modo = document.getElementById('conf-sequencia') ? document.getElementById('conf-sequencia').value : 'otimizado';
  var deposito = {lat: -3.093544, lng: -60.075812};

  // Separa clientes com e sem GPS
  var comGPS = confOrdem.filter(function(o){ return parseFloat(o.lat) && parseFloat(o.lng); });
  var semGPS = confOrdem.filter(function(o){ return !parseFloat(o.lat) || !parseFloat(o.lng); });

  if (modo === 'otimizado') {
    // Nearest Neighbor + 2-opt
    var nn = nearestNeighbor(comGPS, deposito);
    comGPS = otimizar2opt(nn, deposito);
    toast('Rota otimizada com 2-opt! Distância mínima calculada.', 'success');

  } else if (modo === 'proximidade') {
    // Só Nearest Neighbor (mais rápido)
    comGPS = nearestNeighbor(comGPS, deposito);
    toast('Sequência por proximidade aplicada!', 'success');

  } else if (modo === 'distancia') {
    // 2-opt puro partindo da ordem atual
    comGPS = otimizar2opt(comGPS, deposito);
    toast('Menor distância calculada!', 'success');

  } else if (modo === 'agrupamento') {
    // Agrupa por região/bairro
    comGPS.sort(function(a,b){
      var ra = (a.regiao||a.bairro||'zzz');
      var rb = (b.regiao||b.bairro||'zzz');
      if (ra !== rb) return ra.localeCompare(rb);
      // Dentro da mesma região, ordena por proximidade
      return distLatLng(deposito, a) - distLatLng(deposito, b);
    });
    toast('Agrupado por região!', 'success');
  }

  confOrdem = comGPS.concat(semGPS);
  renderizarListaConf();
  atualizarEtaConf();

  // Mostra distância estimada
  var km = (distanciaTotal(comGPS, deposito) * 111).toFixed(0);
  toast('Distância estimada: ~' + km + ' km', 'info');
}"""

if old in content:
    content = content.replace(old, new)
    print('Algoritmo 2-opt implementado!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re, subprocess
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){return{lat:0,lng:0};},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){return Promise.resolve({json:function(){return Promise.resolve({});}})}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('VÁLIDO! Ctrl+Shift+R')
else:
    print('ERRO:', stderr[:400])
