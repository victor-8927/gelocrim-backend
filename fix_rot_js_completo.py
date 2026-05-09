path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui renderRotMapMarkers para usar ícone GPS e bounce
idx = content.find('function renderRotMapMarkers(orders){')
depth = 0
i = idx
while i < len(content):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
    i += 1

new_render = """function renderRotMapMarkers(orders){
  setTimeout(function(){
    var m = initMap('rot-map');
    if(!m) return;
    // Remove markers antigos
    (window._rotMapMarkers||[]).forEach(function(mk){mk.setMap(null);});
    window._rotMapMarkers=[];

    // Lê filtros
    var filtroRota   = (document.getElementById('rot-filtro-rota')   ||{value:''}).value;
    var filtroRegiao = (document.getElementById('rot-filtro-regiao') ||{value:''}).value;
    var filtroBairro = (document.getElementById('rot-filtro-bairro') ||{value:''}).value;
    var filtroBusca  = ((document.getElementById('rot-filtro-busca') ||{value:''}).value||'').toLowerCase();

    var filtrados = (orders||[]).filter(function(o){
      if(!o.lat||!o.lng) return false;
      if(filtroRota   && (o.rota||o.regiao||'').indexOf(filtroRota)<0)   return false;
      if(filtroRegiao && (o.regiao||'').indexOf(filtroRegiao)<0) return false;
      if(filtroBairro && (o.bairro||'').toLowerCase().indexOf(filtroBairro.toLowerCase())<0) return false;
      if(filtroBusca  && (o.recipient_name||'').toLowerCase().indexOf(filtroBusca)<0) return false;
      return true;
    });

    var st = document.getElementById('rot-map-status');
    if(st) st.textContent = filtrados.length+' clientes no mapa';

    var bounds = new google.maps.LatLngBounds();

    filtrados.forEach(function(o){
      var sel = !!window.rotSelecionados[o.id];
      var cor = sel ? '#10b981' : getCorRota(o.rota||o.regiao);

      var mk = new google.maps.Marker({
        position: {lat:parseFloat(o.lat), lng:parseFloat(o.lng)},
        map: m,
        title: o.recipient_name+'|'+(o.rota||o.regiao||''),
        animation: sel ? google.maps.Animation.BOUNCE : null,
        icon: {
          path: google.maps.SymbolPath.MAP_PIN,
          fillColor: cor,
          fillOpacity: 1,
          strokeColor: '#fff',
          strokeWeight: 1.5,
          scale: sel ? 6 : 5,
          anchor: new google.maps.Point(0, 22)
        }
      });

      // Para bounce após 2s
      if(sel){
        setTimeout(function(){ if(mk.getAnimation()) mk.setAnimation(null); }, 2000);
      }

      var tempoMin = parseInt(o.tempo_entrega)||0;
      var tempoStr = tempoMin>0 ? tempoMin+' min' : '—';
      var iw = new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:6px;min-width:200px">'+
        '<b style="font-size:13px;color:#333">'+(o.recipient_name||'—')+'</b><br>'+
        '<span style="color:#e8521a;font-weight:700">📍 Rota '+(o.rota||o.regiao||'—')+'</span><br>'+
        '<span style="color:#555">🏘️ '+(o.bairro||'—')+'</span><br>'+
        '<span style="color:#555">⏱️ Tempo médio: <b>'+tempoStr+'</b></span><br>'+
        (o.address?'<span style="color:#888;font-size:10px">'+o.address+'</span>':'')+
        '</div>'
      });

      mk.addListener('click', function(){
        if(window.rotSelecionados[o.id]){
          delete window.rotSelecionados[o.id];
          mk.setAnimation(null);
          mk.setIcon({path:google.maps.SymbolPath.MAP_PIN,fillColor:getCorRota(o.rota||o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:1.5,scale:5,anchor:new google.maps.Point(0,22)});
          iw.close();
        } else {
          window.rotSelecionados[o.id] = {order:o, marker:mk};
          mk.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout(function(){ mk.setAnimation(null); }, 2000);
          mk.setIcon({path:google.maps.SymbolPath.MAP_PIN,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:1.5,scale:6,anchor:new google.maps.Point(0,22)});
          iw.open(m, mk);
        }
        atualizarSelecaoRot();
      });

      window._rotMapMarkers.push(mk);
      bounds.extend({lat:parseFloat(o.lat), lng:parseFloat(o.lng)});
    });

    if(filtrados.length > 0) m.fitBounds(bounds);
  }, 300);
}

function buscarFiltrados(){
  var cache = window._rotOrdersCache||[];
  // Seleciona todos os clientes filtrados atualmente
  var filtroRota   = (document.getElementById('rot-filtro-rota')   ||{value:''}).value;
  var filtroRegiao = (document.getElementById('rot-filtro-regiao') ||{value:''}).value;
  var filtroBairro = (document.getElementById('rot-filtro-bairro') ||{value:''}).value;
  var filtroBusca  = ((document.getElementById('rot-filtro-busca') ||{value:''}).value||'').toLowerCase();

  if(!filtroRota && !filtroRegiao && !filtroBairro && !filtroBusca){
    toast('Selecione ao menos um filtro!','warn');
    return;
  }

  var candidatos = cache.filter(function(o){
    if(!o.lat||!o.lng) return false;
    if(filtroRota   && (o.rota||o.regiao||'').indexOf(filtroRota)<0)   return false;
    if(filtroRegiao && (o.regiao||'').indexOf(filtroRegiao)<0) return false;
    if(filtroBairro && (o.bairro||'').toLowerCase().indexOf(filtroBairro.toLowerCase())<0) return false;
    if(filtroBusca  && (o.recipient_name||'').toLowerCase().indexOf(filtroBusca)<0) return false;
    return true;
  });

  var novos = 0;
  candidatos.forEach(function(o){
    if(!window.rotSelecionados[o.id]){
      window.rotSelecionados[o.id]={order:o,marker:null};
      novos++;
    }
  });

  // Atualiza markers com bounce
  (window._rotMapMarkers||[]).forEach(function(mk){
    var t = mk.getTitle?mk.getTitle():'';
    var o = cache.find(function(x){return x.recipient_name&&t.indexOf(x.recipient_name)>=0;});
    if(o && window.rotSelecionados[o.id]){
      mk.setAnimation(google.maps.Animation.BOUNCE);
      mk.setIcon({path:google.maps.SymbolPath.MAP_PIN,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:1.5,scale:6,anchor:new google.maps.Point(0,22)});
      window.rotSelecionados[o.id].marker=mk;
      setTimeout(function(){mk.setAnimation(null);},2000);
    }
  });

  atualizarSelecaoRot();
  toast(novos+' clientes selecionados!','success');
}"""

content = content[:idx] + new_render + content[end:]

# Atualiza loadRotMapData para popular bairros e regioes
old_load = """    if(sel){
      var rotasFixas=['801','802','803','804','805','811','821','822'];
      var rotasDinamicas=Object.keys(regioes).sort().filter(function(r){
        return rotasFixas.indexOf(r)<0;
      });
      var todasRotas=rotasFixas.concat(rotasDinamicas);
      sel.innerHTML='<option value="">Todas as rotas</option>'+
        todasRotas.map(function(r){
          var count=items.filter(function(o){return (o.regiao||'').indexOf(r)>=0;}).length;
          return count>0?'<option value="'+r+'">Rota '+r+' ('+count+' clientes)</option>':'';
        }).join('');
    }"""

new_load = """    // Popular filtro de rotas
    var selRota=document.getElementById('rot-filtro-rota');
    if(selRota){
      var rotasFixas=['801','802','803','804','805','811','821','822'];
      selRota.innerHTML='<option value="">🗺️ Todas as rotas</option>'+
        rotasFixas.map(function(r){
          var count=items.filter(function(o){return (o.rota||o.regiao||'').indexOf(r)>=0;}).length;
          return count>0?'<option value="'+r+'">Rota '+r+' ('+count+')</option>':'';
        }).join('');
    }
    // Popular filtro de regiões
    var selRegiao=document.getElementById('rot-filtro-regiao');
    if(selRegiao){
      var regs={};
      items.forEach(function(o){if(o.regiao)regs[o.regiao]=1;});
      selRegiao.innerHTML='<option value="">📍 Todas regiões</option>'+
        Object.keys(regs).sort().map(function(r){
          return '<option value="'+r+'">'+r+'</option>';
        }).join('');
    }
    // Popular filtro de bairros
    var selBairro=document.getElementById('rot-filtro-bairro');
    if(selBairro){
      var bairros={};
      items.forEach(function(o){if(o.bairro)bairros[o.bairro]=1;});
      selBairro.innerHTML='<option value="">🏘️ Todos bairros</option>'+
        Object.keys(bairros).sort().map(function(b){
          return '<option value="'+b+'">'+b+'</option>';
        }).join('');
    }"""

if old_load in content:
    content = content.replace(old_load, new_load)
    print('loadRotMapData com bairros/regiões!')

# Adiciona bairro nos items convertidos de clientes
old_items = """    // Converte clientes para formato de order para compatibilidade
    var items=comGps.map(function(c){
      return {
        id:'cli-'+c.codparc,
        codparc:c.codparc,
        recipient_name:c.nome||'—',
        address:c.endereco||'',
        lat:parseFloat(c.lat),
        lng:parseFloat(c.lng),
        regiao:c.regiao||c.rota||'',
        rota:c.rota||'',
        weight_kg:0,
        order_type:'',
        tempo_entrega:c.tempo_entrega||'0',
        status:'pending'
      };
    });"""

new_items = """    // Converte clientes para formato compatível
    var items=comGps.map(function(c){
      return {
        id:'cli-'+c.codparc,
        codparc:c.codparc,
        recipient_name:c.nome||'—',
        address:c.endereco||'',
        lat:parseFloat(c.lat),
        lng:parseFloat(c.lng),
        regiao:c.regiao||c.zona_geo||'',
        rota:c.rota||'',
        bairro:c.bairro||'',
        cidade:c.cidade||'Manaus',
        weight_kg:0,
        order_type:'',
        tempo_entrega:c.tempo_entrega||'0',
        status:'pending'
      };
    });"""

if old_items in content:
    content = content.replace(old_items, new_items)
    print('Items com bairro/cidade!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
