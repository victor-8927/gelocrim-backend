path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corrige loadRotMapData para pins coloridos por rota
old = """async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando pedidos...';
  try{
    var orders=await api('GET','/orders?status=pending&limit=500');
    if(statusEl) statusEl.textContent=orders.length+' pedidos pendentes no mapa';
    setTimeout(function(){
      var m=initMap('rot-map');
      if(!m) return;
      orders.forEach(function(o){
        if(!o.lat||!o.lng) return;
        var marker=new google.maps.Marker({
          position:{lat:parseFloat(o.lat),lng:parseFloat(o.lng)},map:m,title:o.recipient_name,
          icon:{path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2}
        });
        marker.addListener('click',function(){
          if(rotSelecionados[o.id]){
            delete rotSelecionados[o.id];
            marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          }else{
            rotSelecionados[o.id]={order:o,marker:marker};
            marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:10,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          }
          atualizarSelecaoRot();
        });
      });
    },300);
  }catch(e){ if(statusEl) statusEl.textContent='Erro: '+e.message; }
}"""

new = """// Cores por rota
var COR_ROTAS = {
  '801':'#e8521a','802':'#64B4FF','803':'#10b981','804':'#f59e0b',
  '805':'#a78bfa','811':'#f87171','822':'#2dd4bf',
  'default':'#94a3b8'
};
var _rotMapMarkers = [];
var _rotOrdersCache = [];

function getCorRota(regiao) {
  if(!regiao) return COR_ROTAS.default;
  for(var k in COR_ROTAS){
    if(regiao.indexOf(k)>=0) return COR_ROTAS[k];
  }
  return COR_ROTAS.default;
}

async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando pedidos...';
  try{
    var orders=await api('GET','/orders?status=pending&limit=500');
    _rotOrdersCache = orders;
    if(statusEl) statusEl.textContent=orders.filter(function(o){return o.lat&&o.lng;}).length+' pedidos com GPS de '+orders.length+' total';
    
    // Popula filtros de rota
    var regioes = {};
    orders.forEach(function(o){ if(o.regiao) regioes[o.regiao]=1; });
    var selRota = document.getElementById('rot-filtro-rota');
    if(selRota){
      selRota.innerHTML = '<option value="">Todas as rotas</option>' +
        Object.keys(regioes).sort().map(function(r){
          return '<option value="'+r+'">'+r+'</option>';
        }).join('');
    }
    
    renderRotMapMarkers(orders);
  }catch(e){ if(statusEl) statusEl.textContent='Erro: '+e.message; }
}

function renderRotMapMarkers(orders) {
  var m = initMap('rot-map');
  if(!m) return;

  // Remove markers antigos
  _rotMapMarkers.forEach(function(mk){ mk.setMap(null); });
  _rotMapMarkers = [];

  var filtroRota   = document.getElementById('rot-filtro-rota')   ? document.getElementById('rot-filtro-rota').value   : '';
  var filtroTop    = document.getElementById('rot-filtro-top')     ? document.getElementById('rot-filtro-top').value     : '';
  var filtroBusca  = document.getElementById('rot-filtro-busca')   ? document.getElementById('rot-filtro-busca').value.toLowerCase() : '';

  var filtrados = orders.filter(function(o){
    if(!o.lat || !o.lng) return false;
    if(filtroRota && (o.regiao||'').indexOf(filtroRota)<0) return false;
    if(filtroTop  && (o.order_type||'').indexOf(filtroTop)<0) return false;
    if(filtroBusca && (o.recipient_name||'').toLowerCase().indexOf(filtroBusca)<0) return false;
    return true;
  });

  var statusEl = document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent = filtrados.length+' clientes no mapa';

  filtrados.forEach(function(o){
    var cor = rotSelecionados[o.id] ? '#10b981' : getCorRota(o.regiao);
    var scale = rotSelecionados[o.id] ? 12 : 9;
    var marker = new google.maps.Marker({
      position:{lat:parseFloat(o.lat),lng:parseFloat(o.lng)},
      map:m,
      title:o.recipient_name+' | '+(o.regiao||'—')+' | '+o.weight_kg+'kg',
      icon:{path:google.maps.SymbolPath.CIRCLE,scale:scale,fillColor:cor,fillOpacity:1,strokeColor:'#fff',strokeWeight:2}
    });

    // InfoWindow
    var iw = new google.maps.InfoWindow({
      content:'<div style="font-family:Arial;font-size:12px;min-width:160px">'+
        '<b>'+o.recipient_name+'</b><br>'+
        '<span style="color:#666">Rota: '+(o.regiao||'—')+'</span><br>'+
        '<span style="color:#666">Peso: '+o.weight_kg+' kg</span><br>'+
        '<span style="color:#666">TOP: '+(o.order_type||'—')+'</span>'+
        '</div>'
    });

    marker.addListener('click',function(){
      if(rotSelecionados[o.id]){
        delete rotSelecionados[o.id];
        marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:9,fillColor:getCorRota(o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
      }else{
        rotSelecionados[o.id]={order:o,marker:marker};
        marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
        iw.open(m,marker);
      }
      atualizarSelecaoRot();
    });
    _rotMapMarkers.push(marker);
  });
}

function filtrarRotMapa(){
  renderRotMapMarkers(_rotOrdersCache);
}

function selecionarTodaRota(){
  var filtroRota = document.getElementById('rot-filtro-rota') ? document.getElementById('rot-filtro-rota').value : '';
  if(!filtroRota){ toast('Selecione uma rota primeiro!','warn'); return; }
  _rotOrdersCache.filter(function(o){
    return o.lat && o.lng && (o.regiao||'').indexOf(filtroRota)>=0 && !rotSelecionados[o.id];
  }).forEach(function(o){
    // Encontra marker
    var mk = _rotMapMarkers.find(function(m){ return m.getTitle && m.getTitle().indexOf(o.recipient_name)>=0; });
    rotSelecionados[o.id]={order:o,marker:mk||null};
    if(mk) mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
  });
  atualizarSelecaoRot();
  toast('Rota '+filtroRota+' selecionada!','success');
}"""

if old in content:
    content = content.replace(old, new)
    print('loadRotMapData atualizado com pins coloridos!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
