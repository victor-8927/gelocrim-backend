path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui loadRotMapData para usar /clientes em vez de /orders
old = """async function loadRotMapData(){
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

new = """async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando clientes...';
  try{
    // Carrega clientes com GPS para o mapa
    var clientes=await api('GET','/clientes');
    var comGps=clientes.filter(function(c){return c.lat&&c.lng;});
    
    // Converte clientes para formato de order para compatibilidade
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
    });
    
    window._rotOrdersCache=items;
    
    // Popula filtro de rotas
    var regioes={};
    items.forEach(function(o){if(o.regiao)regioes[o.regiao]=1;});
    var sel=document.getElementById('rot-filtro-rota');
    if(sel) sel.innerHTML='<option value="">Todas as rotas</option>'+
      Object.keys(regioes).sort().map(function(r){
        return '<option value="'+r+'">'+r+'</option>';
      }).join('');
    
    if(statusEl) statusEl.textContent=items.length+' clientes com GPS carregados';
    renderRotMapMarkers(items);
  }catch(e){
    if(statusEl) statusEl.textContent='Erro: '+e.message;
    console.error('Erro loadRotMapData:',e);
  }
}"""

if old in content:
    content = content.replace(old, new)
    print('loadRotMapData atualizado para usar clientes!')
else:
    print('Padrão não encontrado! Buscando...')
    idx = content.find('async function loadRotMapData()')
    if idx != -1:
        ln = content[:idx].count('\n')+1
        print(f'loadRotMapData na linha {ln}')
        # Mostra a função atual
        print(repr(content[idx:idx+400]))

# Atualiza renderRotMapMarkers para mostrar mais info do cliente
old2 = """      var iw=new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:4px"><b>'+(o.recipient_name||'')+'</b><br>'+
        'Rota: <b>'+(o.regiao||'—')+'</b> | Peso: <b>'+o.weight_kg+' kg</b></div>'
      });"""

new2 = """      var tempoMin=parseInt(o.tempo_entrega)||0;
      var tempoStr=tempoMin>0?(tempoMin+' min'):'-';
      var iw=new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:6px;min-width:180px">'+
        '<b style="font-size:13px">'+(o.recipient_name||'')+'</b><br>'+
        '<span style="color:#666">📍 '+(o.regiao||o.rota||'—')+'</span><br>'+
        '<span style="color:#666">⏱️ Tempo médio: <b>'+tempoStr+'</b></span><br>'+
        '<span style="color:#666">📦 Peso: '+(o.weight_kg||0)+' kg</span><br>'+
        (o.address?'<span style="color:#888;font-size:10px">'+o.address+'</span>':'')+
        '</div>'
      });"""

if old2 in content:
    content = content.replace(old2, new2)
    print('InfoWindow atualizado com tempo médio!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
