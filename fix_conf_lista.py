path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """function renderizarListaConf(){}
function inverterOrdemConf(){}
function reprocessarSequencia(){}
function atualizarRotaMapa(){toast('Rota atualizada!','success');}
function confirmarRota(){rotaConfirmada=true;toast('Rota confirmada!','success');}"""

new = """function renderizarListaConf() {
  var lista = document.getElementById('conf-lista-clientes');
  if (!lista) return;
  if (!confOrdem || !confOrdem.length) {
    lista.innerHTML = '<div style="padding:16px;text-align:center;color:#90afd4;font-size:11px">Nenhum cliente selecionado</div>';
    return;
  }

  lista.innerHTML = confOrdem.map(function(o, i) {
    var peso = (o.weight_kg || 0).toFixed(0);
    var itens = '';
    if (o.pedidos && o.pedidos.length) {
      itens = '<div style="font-size:9px;color:#64B4FF;margin-top:2px">' + o.pedidos.slice(0,3).join(' · ') + '</div>';
    }
    return '<div class="conf-item" draggable="true" data-idx="'+i+'" '+
      'ondragstart="confDragStart(event,'+i+')" '+
      'ondragover="confDragOver(event)" '+
      'ondrop="confDrop(event,'+i+')" '+
      'style="display:flex;align-items:center;gap:8px;padding:8px;margin-bottom:4px;'+
      'background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;cursor:grab;transition:background .15s" '+
      'onmouseover="this.style.background=\'#1e3a5c\'" onmouseout="this.style.background=\'#0a1628\'">'+
      '<div style="width:22px;height:22px;border-radius:50%;background:#64B4FF;color:#002855;'+
      'font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0">'+(i+1)+'</div>'+
      '<div style="flex:1;min-width:0">'+
        '<div style="font-size:11px;font-weight:700;color:#e8f0fe;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+
          (o.recipient_name || o.nome || '—')+'</div>'+
        '<div style="font-size:10px;color:#90afd4">⚖️ '+peso+' kg · '+(o.regiao||o.bairro||'—')+'</div>'+
        itens+
      '</div>'+
      '<button onclick="removerDaConf('+i+')" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:14px;padding:2px 4px;flex-shrink:0" title="Remover">✕</button>'+
    '</div>';
  }).join('');

  // Atualiza peso total
  var totalKg = confOrdem.reduce(function(s,o){return s+(parseFloat(o.weight_kg)||0);}, 0);
  var el = document.getElementById('conf-peso-total');
  if (el) el.textContent = totalKg.toFixed(0) + ' kg';
}

var _confDragIdx = null;
function confDragStart(e, idx) { _confDragIdx = idx; e.dataTransfer.effectAllowed='move'; }
function confDragOver(e) { e.preventDefault(); e.dataTransfer.dropEffect='move'; }
function confDrop(e, idx) {
  e.preventDefault();
  if (_confDragIdx === null || _confDragIdx === idx) return;
  var item = confOrdem.splice(_confDragIdx, 1)[0];
  confOrdem.splice(idx, 0, item);
  _confDragIdx = null;
  renderizarListaConf();
  atualizarEtaConf();
}

function removerDaConf(idx) {
  confOrdem.splice(idx, 1);
  renderizarListaConf();
  atualizarEtaConf();
}

function inverterOrdemConf() {
  confOrdem.reverse();
  renderizarListaConf();
  toast('Ordem invertida!', 'info');
}

function reprocessarSequencia() {
  // Ordena por região/bairro para otimizar rota
  confOrdem.sort(function(a,b){
    var ra = a.regiao||a.bairro||'';
    var rb = b.regiao||b.bairro||'';
    return ra.localeCompare(rb);
  });
  renderizarListaConf();
  toast('Sequência reprocessada por região!', 'success');
}

function atualizarEtaConf() {
  var horaEl = document.getElementById('conf-hora-inicio');
  var hora = horaEl ? horaEl.value : '07:30';
  var parts = hora.split(':').map(Number);
  var minutos = parts[0]*60 + parts[1];
  var tempoParada = 15; // minutos por parada
  var kmParada = 3;     // km entre paradas
  var velMedia = 30;    // km/h

  confOrdem.forEach(function(o, i) {
    minutos += tempoParada + Math.round(kmParada/velMedia*60);
    var h = Math.floor(minutos/60) % 24;
    var m = minutos % 60;
    o._eta = String(h).padStart(2,'0')+':'+String(m).padStart(2,'0');
  });

  var ultimo = confOrdem.length > 0 ? confOrdem[confOrdem.length-1]._eta : null;
  var fimEl = document.getElementById('conf-hora-fim');
  if (fimEl && ultimo) fimEl.textContent = ultimo;
}

function atualizarRotaMapa() {
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
}

function confirmarRota() {
  rotaConfirmada = true;
  var bG = document.getElementById('btn-gravar-carga');
  var bC = document.getElementById('btn-confirmar-rota');
  if (bG) {
    bG.disabled = false;
    bG.style.background = '#10b981';
    bG.style.color = '#fff';
    bG.style.cursor = 'pointer';
    bG.style.opacity = '1';
    bG.textContent = '💾 GRAVAR CARGA';
  }
  if (bC) {
    bC.textContent = '✅ Rota Confirmada!';
    bC.style.background = 'rgba(16,185,129,.2)';
    bC.style.borderColor = '#10b981';
    bC.style.color = '#10b981';
  }
  toast('Rota confirmada! Clique em GRAVAR CARGA.', 'success');
}"""

if old in content:
    content = content.replace(old, new)
    print('Funções da Conferência Master implementadas!')
else:
    print('Padrão não encontrado!')

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
    print('ERRO:', stderr[:300])
