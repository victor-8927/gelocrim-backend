PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(PATH, encoding='utf-8', errors='ignore') as f:
    content = f.read()

OLD = """    var st = document.getElementById('rot-map-status');
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
          path: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',
          fillColor: cor,
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 1,
          scale: sel ? 2.2 : 1.7,
          anchor: new google.maps.Point(12, 22),
          rotation: 0
        }
      });
      if(sel) setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);"""

NEW = """    var st = document.getElementById('rot-map-status');
    if(st) st.textContent = filtrados.length+' clientes no mapa';
    var bounds = new google.maps.LatLngBounds();
    var openIW = null;
    var fixedIW = null;

    // Cores neon por segmento
    function getCorSegmento(o) {
      var seg = (o.segmento||o.segment||'').toUpperCase();
      if (seg.indexOf('POSTO') >= 0 || seg.indexOf('COMBUST') >= 0) return '#FF6B35';
      if (seg.indexOf('ILHA') >= 0 || seg.indexOf('GELAD') >= 0)    return '#00FFEA';
      if (seg.indexOf('FABRIC') >= 0 || seg.indexOf('INDUST') >= 0) return '#BF5FFF';
      if (seg.indexOf('REFEIT') >= 0 || seg.indexOf('RESTAUR') >= 0 || seg.indexOf('LANCH') >= 0) return '#FFD700';
      if (seg.indexOf('DISTRIB') >= 0 || seg.indexOf('ATACAD') >= 0) return '#00FF88';
      if (seg.indexOf('MERCED') >= 0 || seg.indexOf('SUPERM') >= 0) return '#FF3355';
      if (seg.indexOf('BAR') >= 0 || seg.indexOf('BOATE') >= 0)     return '#FF8C00';
      if (seg.indexOf('CONV') >= 0)                                   return '#FF6B35';
      if (seg.indexOf('HOTEL') >= 0 || seg.indexOf('POUSAD') >= 0)  return '#90afd4';
      return getCorRota(o.rota||o.regiao);
    }

    filtrados.forEach(function(o){
      var sel = !!window.rotSelecionados[o.id];
      var corBase = getCorSegmento(o);
      var cor = sel ? '#00FF88' : corBase;
      var nPedidos = (o.pedidos||[]).length;
      var tempoMin = parseInt(o.tempo_entrega)||0;
      var mk = new google.maps.Marker({
        position: {lat:parseFloat(o.lat), lng:parseFloat(o.lng)},
        map: m,
        title: (o.recipient_name||'')+'|'+(o.rota||o.regiao||''),
        animation: sel ? google.maps.Animation.BOUNCE : null,
        icon: {
          path: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',
          fillColor: cor,
          fillOpacity: 1,
          strokeColor: sel ? '#ffffff' : '#001020',
          strokeWeight: sel ? 2.5 : 1.5,
          scale: sel ? 2.5 : 1.8,
          anchor: new google.maps.Point(12, 22),
        }
      });
      if(sel) setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK! Pins neon por segmento adicionados!")
else:
    print("AVISO: bloco nao encontrado")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Ctrl+Shift+R no navegador!")
