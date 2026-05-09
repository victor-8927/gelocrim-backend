path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra o fechamento do primeiro script
primeiro_close = content.find('</script>\n  <!-- MODAL IMPORTA')
if primeiro_close == -1:
    primeiro_close = content.find('\n</script>\n  <!-- MODAL')
ln = content[:primeiro_close].count('\n')+1
print(f'Inserindo antes da linha {ln}')

novo = """
// ── ROTEIRIZAÇÃO ─────────────────────────────────────────────────
var COR_ROTAS={'801':'#e8521a','802':'#64B4FF','803':'#10b981','804':'#f59e0b','805':'#a78bfa','811':'#f87171','822':'#2dd4bf'};
var _rotMapMarkers=[];
var _rotOrdersCache=[];

function getCorRota(r){
  if(!r) return '#94a3b8';
  for(var k in COR_ROTAS){ if(r.indexOf(k)>=0) return COR_ROTAS[k]; }
  return '#94a3b8';
}

function filtrarRotMapa(){ renderRotMapMarkers(_rotOrdersCache); }

function selecionarTodaRota(){
  var fr=document.getElementById('rot-filtro-rota');
  var filtro=fr?fr.value:'';
  if(!filtro){toast('Selecione uma rota!','warn');return;}
  var sel=0;
  _rotOrdersCache.forEach(function(o){
    if(!o.lat||!o.lng||rotSelecionados[o.id]) return;
    if((o.regiao||'').indexOf(filtro)<0) return;
    rotSelecionados[o.id]={order:o,marker:null};
    sel++;
  });
  _rotMapMarkers.forEach(function(mk){
    var t=mk.getTitle?mk.getTitle():'';
    var o=_rotOrdersCache.find(function(x){return x.lat&&t.indexOf(x.recipient_name)>=0;});
    if(o&&rotSelecionados[o.id]){
      mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
      rotSelecionados[o.id].marker=mk;
    }
  });
  atualizarSelecaoRot();
  toast(sel+' clientes da '+filtro+' selecionados!','success');
}

function renderRotMapMarkers(orders){
  setTimeout(function(){
    var m=initMap('rot-map');
    if(!m) return;
    _rotMapMarkers.forEach(function(mk){mk.setMap(null);});
    _rotMapMarkers=[];
    var fr=document.getElementById('rot-filtro-rota');
    var ft=document.getElementById('rot-filtro-top');
    var fb=document.getElementById('rot-filtro-busca');
    var filtroRota=fr?fr.value:'';
    var filtroTop=ft?ft.value:'';
    var filtroBusca=fb?fb.value.toLowerCase():'';
    var filtrados=orders.filter(function(o){
      if(!o.lat||!o.lng) return false;
      if(filtroRota&&(o.regiao||'').indexOf(filtroRota)<0) return false;
      if(filtroTop&&(o.order_type||'').indexOf(filtroTop)<0) return false;
      if(filtroBusca&&(o.recipient_name||'').toLowerCase().indexOf(filtroBusca)<0) return false;
      return true;
    });
    var st=document.getElementById('rot-map-status');
    if(st) st.textContent=filtrados.length+' clientes no mapa';
    filtrados.forEach(function(o){
      var sel=!!rotSelecionados[o.id];
      var cor=sel?'#10b981':getCorRota(o.regiao);
      var mk=new google.maps.Marker({
        position:{lat:parseFloat(o.lat),lng:parseFloat(o.lng)},map:m,
        title:o.recipient_name+'|'+(o.regiao||''),
        icon:{path:google.maps.SymbolPath.CIRCLE,scale:sel?12:9,fillColor:cor,fillOpacity:1,strokeColor:'#fff',strokeWeight:2}
      });
      var iw=new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:4px"><b>'+(o.recipient_name||'')+'</b><br>'+
        'Rota: <b>'+(o.regiao||'—')+'</b> | Peso: <b>'+o.weight_kg+' kg</b></div>'
      });
      mk.addListener('click',function(){
        if(rotSelecionados[o.id]){
          delete rotSelecionados[o.id];
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:9,fillColor:getCorRota(o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          iw.close();
        }else{
          rotSelecionados[o.id]={order:o,marker:mk};
          mk.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          iw.open(m,mk);
        }
        atualizarSelecaoRot();
      });
      _rotMapMarkers.push(mk);
    });
  },300);
}
"""

content = content[:primeiro_close] + novo + content[primeiro_close:]

# Atualiza loadRotMapData
old = """async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando pedidos...';
  try{
    var orders=await api('GET','/orders?status=pending&limit=500');
    _rotOrdersCache = orders;
    // Popula filtro de rotas
    var regioes={};
    orders.forEach(function(o){ if(o.regiao) regioes[o.regiao]=1; });
    var selRota=document.getElementById('rot-filtro-rota');
    if(selRota){
      selRota.innerHTML='<option value="">Todas as rotas</option>'+
        Object.keys(regioes).sort().map(function(r){return '<option value="'+r+'">'+r+'</option>';}).join('');
    }
    renderRotMapMarkers(orders);
  }catch(e){ if(statusEl) statusEl.textContent='Erro: '+e.message; }
}"""

new = """async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando...';
  try{
    var orders=await api('GET','/orders?status=pending&limit=500');
    _rotOrdersCache=orders;
    var regioes={};
    orders.forEach(function(o){if(o.regiao)regioes[o.regiao]=1;});
    var sel=document.getElementById('rot-filtro-rota');
    if(sel) sel.innerHTML='<option value="">Todas as rotas</option>'+Object.keys(regioes).sort().map(function(r){return '<option value="'+r+'">'+r+'</option>';}).join('');
    renderRotMapMarkers(orders);
  }catch(e){if(statusEl)statusEl.textContent='Erro: '+e.message;}
}"""

if old in content:
    content = content.replace(old, new)
    print('loadRotMapData atualizado!')
else:
    print('loadRotMapData padrao nao encontrado — mantendo existente')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Pronto! Ctrl+Shift+R.')
