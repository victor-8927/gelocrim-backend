path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Aumenta os pins - substitui renderRotMapMarkers completo
idx = content.find('function renderRotMapMarkers(orders){')
depth = 0; i = idx
while i < len(content):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0: end = i + 1; break
    i += 1

new_render = """function renderRotMapMarkers(orders){
  setTimeout(function(){
    var m = initMap('rot-map');
    if(!m) return;
    (window._rotMapMarkers||[]).forEach(function(mk){ mk.setMap(null); });
    window._rotMapMarkers = [];

    var fr  = document.getElementById('rot-filtro-rota');
    var freg= document.getElementById('rot-filtro-regiao');
    var fb  = document.getElementById('rot-filtro-bairro');
    var fs  = document.getElementById('rot-filtro-busca');
    var vr  = fr  ? fr.value  : '';
    var vreg= freg? freg.value: '';
    var vb  = fb  ? fb.value  : '';
    var vs  = fs  ? fs.value.toLowerCase() : '';

    var filtrados = (orders||[]).filter(function(o){
      if(!o.lat||!o.lng) return false;
      if(vr   && (o.rota||o.regiao||'').indexOf(vr)<0)   return false;
      if(vreg && (o.regiao||'').indexOf(vreg)<0)          return false;
      if(vb   && (o.bairro||'').toLowerCase().indexOf(vb.toLowerCase())<0) return false;
      if(vs   && (o.recipient_name||'').toLowerCase().indexOf(vs)<0) return false;
      return true;
    });

    var st = document.getElementById('rot-map-status');
    if(st) st.textContent = filtrados.length+' clientes no mapa';

    var bounds = new google.maps.LatLngBounds();
    var openIW = null; // InfoWindow atualmente aberto
    var fixedIW = null; // InfoWindow fixo (duplo clique)

    filtrados.forEach(function(o){
      var sel = !!window.rotSelecionados[o.id];
      var cor = sel ? '#10b981' : getCorRota(o.rota||o.regiao);
      var nPedidos = (o.pedidos||[]).length;
      var tempoMin = parseInt(o.tempo_entrega)||0;

      var mk = new google.maps.Marker({
        position: {lat:parseFloat(o.lat), lng:parseFloat(o.lng)},
        map: m,
        title: (o.recipient_name||'')+'|'+(o.rota||o.regiao||''),
        animation: sel ? google.maps.Animation.BOUNCE : null,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: cor,
          fillOpacity: 0.95,
          strokeColor: '#ffffff',
          strokeWeight: 2.5,
          scale: sel ? 16 : 12
        }
      });

      if(sel) setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);

      var iwContent =
        '<div style="font-family:Arial;font-size:12px;padding:8px;min-width:210px;max-width:260px">'+
        '<b style="font-size:14px;color:#1a3a5c">'+(o.recipient_name||'—')+'</b><br>'+
        '<span style="color:#e8521a;font-weight:700;font-size:12px">🗺️ Rota '+(o.rota||o.regiao||'—')+'</span><br>'+
        (o.bairro?'<span style="color:#555">🏘️ '+o.bairro+'</span><br>':'')+
        '<span style="color:#555">📦 '+nPedidos+' pedido(s) | '+(o.weight_kg||0).toFixed(0)+' kg total</span><br>'+
        '<span style="color:#555">⏱️ Tempo médio: '+(tempoMin>0?tempoMin+' min':'—')+'</span>'+
        '</div>';

      var iw = new google.maps.InfoWindow({content: iwContent});

      // 1 clique: seleciona + mostra InfoWindow temporário
      mk.addListener('click', function(){
        if(window.rotSelecionados[o.id]){
          delete window.rotSelecionados[o.id];
          mk.setAnimation(null);
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,fillColor:getCorRota(o.rota||o.regiao),fillOpacity:0.95,strokeColor:'#fff',strokeWeight:2.5,scale:12});
        } else {
          window.rotSelecionados[o.id] = {order:o, marker:mk};
          mk.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,fillColor:'#10b981',fillOpacity:0.95,strokeColor:'#fff',strokeWeight:2.5,scale:16});
        }
        // Fecha InfoWindow anterior temporário
        if(openIW && openIW !== fixedIW) openIW.close();
        iw.open(m, mk);
        openIW = iw;
        // Fecha automaticamente após 3s (a menos que seja fixo)
        setTimeout(function(){
          if(openIW === iw && fixedIW !== iw) { iw.close(); openIW = null; }
        }, 3000);
        atualizarSelecaoRot();
      });

      // 2 cliques: fixa o InfoWindow
      mk.addListener('dblclick', function(){
        if(fixedIW) fixedIW.close();
        iw.open(m, mk);
        fixedIW = iw;
        openIW = iw;
      });

      window._rotMapMarkers.push(mk);
      bounds.extend({lat:parseFloat(o.lat), lng:parseFloat(o.lng)});
    });

    if(filtrados.length > 0 && !bounds.isEmpty()) m.fitBounds(bounds);
  }, 200);
}"""

content = content[:idx] + new_render + content[end:]
print('renderRotMapMarkers atualizado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica botões Individual e Desenhar Área
idx2 = content.find('rotIndividual') or content.find('Desenhar')
if 'rotIndividual' in content:
    i = content.find('rotIndividual')
    ln = content[:i].count('\n')+1
    print(f'rotIndividual na linha {ln}')
if 'rot-btn-draw' in content or 'desenharArea' in content:
    print('Botão Desenhar encontrado')
else:
    print('Botão Desenhar NAO encontrado — será adicionado')
