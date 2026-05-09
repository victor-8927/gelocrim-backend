path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui renderizarListaConf completo
idx_start = content.find('function renderizarListaConf()')
idx_end = content.find('\n// Distância euclidiana')
print(f'Substituindo de linha {content[:idx_start].count(chr(10))+1} até {content[:idx_end].count(chr(10))+1}')

new_funcs = r"""function renderizarListaConf() {
  var lista = document.getElementById('conf-lista-clientes');
  if (!lista) return;
  if (!confOrdem || !confOrdem.length) {
    lista.innerHTML = '<div style="padding:16px;text-align:center;color:#90afd4;font-size:11px">Nenhum cliente selecionado</div>';
    return;
  }
  lista.innerHTML = confOrdem.map(function(o, i) {
    var peso = (parseFloat(o.weight_kg)||0).toFixed(0);
    var eta  = o._eta || '—';
    return '<div class="conf-item" draggable="true" data-idx="'+i+'" '+
      'ondragstart="confDragStart(event,'+i+')" '+
      'ondragover="confDragOver(event)" '+
      'ondrop="confDrop(event,'+i+')" '+
      'style="display:flex;align-items:center;gap:8px;padding:8px;margin-bottom:4px;'+
      'background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;cursor:grab">'+
      '<div style="width:22px;height:22px;border-radius:50%;background:#64B4FF;color:#002855;'+
      'font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0">'+(i+1)+'</div>'+
      '<div style="flex:1;min-width:0">'+
        '<div style="font-size:11px;font-weight:700;color:#e8f0fe;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+
          (o.recipient_name||o.nome||'—')+'</div>'+
        '<div style="font-size:10px;color:#90afd4">⚖️ '+peso+' kg · ⏱ '+eta+'</div>'+
      '</div>'+
      '<button onclick="removerDaConf('+i+')" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:14px;padding:2px 6px;flex-shrink:0">✕</button>'+
    '</div>';
  }).join('');
}

var _confDragIdx = null;

function confDragStart(e, idx) {
  _confDragIdx = idx;
  e.dataTransfer.effectAllowed = 'move';
}

function confDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
}

function confDrop(e, idx) {
  e.preventDefault();
  if (_confDragIdx === null || _confDragIdx === idx) return;
  // Remove o item da posição original e insere na nova posição
  var item = confOrdem.splice(_confDragIdx, 1)[0];
  confOrdem.splice(idx, 0, item);
  _confDragIdx = null;
  renderizarListaConf();
}

function removerDaConf(idx) {
  confOrdem.splice(idx, 1);
  renderizarListaConf();
}

function inverterOrdemConf() {
  confOrdem.reverse();
  renderizarListaConf();
  toast('Ordem invertida!', 'info');
}

function atualizarEtaConf() {
  var horaEl = document.getElementById('conf-hora-inicio');
  var hora = horaEl ? horaEl.value : '07:30';
  var parts = hora.split(':').map(Number);
  var minutos = parts[0]*60 + parts[1];
  var kmParada = 5;
  var velMedia = 40;

  confOrdem.forEach(function(o) {
    var tempoParada = parseInt(o.tempo_entrega || 15);
    var tempoViagem = Math.round(kmParada / velMedia * 60);
    minutos += tempoViagem + tempoParada;
    var h = Math.floor(minutos/60) % 24;
    var m = minutos % 60;
    o._eta = String(h).padStart(2,'0')+':'+String(m).padStart(2,'0');
  });

  var fimEl = document.getElementById('conf-hora-fim');
  if (fimEl && confOrdem.length) fimEl.textContent = confOrdem[confOrdem.length-1]._eta || '—';
}

"""

content = content[:idx_start] + new_funcs + content[idx_end:]

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
