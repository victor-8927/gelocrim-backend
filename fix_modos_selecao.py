path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "function setModoSelecao(modo){}\nfunction rotVeiculoChanged(){}"

new = """function setModoSelecao(modo){
  window._rotModo = modo;
  var btnClick = document.getElementById('btn-modo-click');
  var btnArea  = document.getElementById('btn-modo-area');
  var dica     = document.getElementById('dica-modo');

  if(btnClick) btnClick.style.border = modo==='click' ? '2px solid #e8521a' : '2px solid #1e3a5c';
  if(btnClick) btnClick.style.background = modo==='click' ? 'rgba(232,82,26,.25)' : 'transparent';
  if(btnArea)  btnArea.style.border  = modo==='area'  ? '2px solid #10b981' : '2px solid #1e3a5c';
  if(btnArea)  btnArea.style.background  = modo==='area'  ? 'rgba(16,185,129,.25)' : 'transparent';

  // Para DrawingManager anterior
  if(window._drawingManager){
    window._drawingManager.setDrawingMode(null);
    window._drawingManager.setMap(null);
    window._drawingManager = null;
  }

  if(modo === 'area'){
    if(dica) dica.textContent = '✏️ Desenhe um polígono no mapa para selecionar clientes';
    var m = initMap('rot-map');
    if(!m){ toast('Carregue o mapa primeiro!','warn'); return; }

    if(typeof google.maps.drawing === 'undefined'){
      toast('DrawingManager não disponível nesta versão da API','warn');
      // Fallback: modo retângulo manual
      _iniciarSelecaoRetangulo(m);
      return;
    }

    var dm = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.POLYGON,
      drawingControl: false,
      polygonOptions: {
        fillColor:'#10b981', fillOpacity:0.2,
        strokeColor:'#10b981', strokeWeight:2, clickable:false
      }
    });
    dm.setMap(m);
    window._drawingManager = dm;

    google.maps.event.addListener(dm, 'polygoncomplete', function(polygon){
      dm.setDrawingMode(null);
      var path = polygon.getPath();
      var selecionados = 0;
      var cache = window._rotOrdersCache || [];
      cache.forEach(function(o){
        if(!o.lat || !o.lng) return;
        var pt = new google.maps.LatLng(parseFloat(o.lat), parseFloat(o.lng));
        if(google.maps.geometry.poly.containsLocation(pt, polygon)){
          if(!window.rotSelecionados[o.id]){
            window.rotSelecionados[o.id] = {order:o, marker:null};
            selecionados++;
          }
        }
      });
      polygon.setMap(null);
      renderRotMapMarkers(cache);
      atualizarSelecaoRot();
      toast(selecionados+' clientes selecionados na área!','success');
      setModoSelecao('click');
    });
  } else {
    if(dica) dica.textContent = '📌 Clique nos pins para selecionar individualmente';
  }
}

function _iniciarSelecaoRetangulo(m){
  // Fallback: clique-e-arraste cria um retângulo
  toast('Clique e arraste no mapa para selecionar área','info');
  var startLatLng = null;
  var rect = null;
  var dica = document.getElementById('dica-modo');
  if(dica) dica.textContent = '🖱️ Clique e arraste para selecionar área';

  var lDown = google.maps.event.addListener(m, 'mousedown', function(e){
    m.setOptions({draggable:false});
    startLatLng = e.latLng;
  });
  var lMove = google.maps.event.addListener(m, 'mousemove', function(e){
    if(!startLatLng) return;
    if(rect) rect.setMap(null);
    rect = new google.maps.Rectangle({
      bounds: new google.maps.LatLngBounds(
        new google.maps.LatLng(Math.min(startLatLng.lat(),e.latLng.lat()), Math.min(startLatLng.lng(),e.latLng.lng())),
        new google.maps.LatLng(Math.max(startLatLng.lat(),e.latLng.lat()), Math.max(startLatLng.lng(),e.latLng.lng()))
      ),
      fillColor:'#10b981', fillOpacity:0.2, strokeColor:'#10b981', strokeWeight:2, map:m
    });
  });
  var lUp = google.maps.event.addListener(m, 'mouseup', function(e){
    if(!startLatLng) return;
    m.setOptions({draggable:true});
    var bounds = rect ? rect.getBounds() : null;
    var sel=0;
    if(bounds){
      (window._rotOrdersCache||[]).forEach(function(o){
        if(!o.lat||!o.lng) return;
        if(bounds.contains(new google.maps.LatLng(parseFloat(o.lat),parseFloat(o.lng)))){
          if(!window.rotSelecionados[o.id]){ window.rotSelecionados[o.id]={order:o,marker:null}; sel++; }
        }
      });
      if(rect) rect.setMap(null);
    }
    startLatLng = null;
    google.maps.event.removeListener(lDown);
    google.maps.event.removeListener(lMove);
    google.maps.event.removeListener(lUp);
    renderRotMapMarkers(window._rotOrdersCache||[]);
    atualizarSelecaoRot();
    toast(sel+' clientes selecionados!','success');
    setModoSelecao('click');
  });
}

function rotVeiculoChanged(){}"""

if old in content:
    content = content.replace(old, new)
    print('setModoSelecao implementado!')
else:
    print('Padrão não encontrado!')

# Também melhora atualizarSelecaoRot para mostrar pallets/cubagem
old2 = """function atualizarSelecaoRot(){
  var itens=Object.values(window.rotSelecionados);
  var count=document.getElementById('rot-count');
  var pesoEl=document.getElementById('rot-total-peso');
  var volEl=document.getElementById('rot-total-vol');
  var btnRot=document.getElementById('btn-rot-map');
  var cardVeic=document.getElementById('card-sel-veiculo');
  if(count) count.textContent=itens.length;"""

new2 = """function atualizarSelecaoRot(){
  var itens=Object.values(window.rotSelecionados);
  var count=document.getElementById('rot-count');
  var pesoEl=document.getElementById('rot-total-peso');
  var volEl=document.getElementById('rot-total-vol');
  var btnRot=document.getElementById('btn-rot-map');
  var cardVeic=document.getElementById('card-sel-veiculo');
  if(count) count.textContent=itens.length;
  // Calcula peso total
  var pesoTotal = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).weight_kg)||0); },0);
  if(pesoEl) pesoEl.textContent = pesoTotal.toFixed(0)+' kg';
  // Atualiza painel de sugestão de veículo
  var painelSug = document.getElementById('rot-sugestao-veiculo');
  if(painelSug){
    if(itens.length>0){
      painelSug.style.display='block';
      var sugPeso = document.getElementById('sug-peso-total');
      var sugClientes = document.getElementById('sug-clientes');
      if(sugPeso) sugPeso.textContent = pesoTotal.toFixed(0)+' kg';
      if(sugClientes) sugClientes.textContent = itens.length;
    } else {
      painelSug.style.display='none';
    }
  }"""

if old2 in content:
    content = content.replace(old2, new2)
    print('atualizarSelecaoRot melhorado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
