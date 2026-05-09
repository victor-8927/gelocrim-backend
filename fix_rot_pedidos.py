path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """    var clientes = await api('GET','/clientes');
    console.log('Clientes:', clientes.length);
    var comGps = clientes.filter(function(c){return c.lat&&c.lng;});
    var items = comGps.map(function(c){
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
        tempo_entrega:c.tempo_entrega||'0',
        weight_kg:0,
        order_type:'',
        status:'pending'
      };
    });
    window._rotOrdersCache = items;
    console.log('Items com GPS:', items.length);"""

new = """    // Carrega pedidos pendentes E clientes
    var [orders, clientes] = await Promise.all([
      api('GET','/orders?status=pending&limit=500'),
      api('GET','/clientes')
    ]);
    console.log('Pedidos pendentes:', orders.length, 'Clientes:', clientes.length);

    // Cria mapa de clientes por codparc
    var cliMap = {};
    clientes.forEach(function(c){ if(c.codparc) cliMap[c.codparc]=c; });

    // Agrupa pedidos por cliente (codparc ou recipient_name)
    var clienteMap = {};
    orders.forEach(function(o){
      // Tenta encontrar o cliente pelo codparc
      var cli = o.codparc ? cliMap[o.codparc] : null;
      // Se não tem codparc, tenta pelo nome
      if(!cli && o.recipient_name){
        cli = clientes.find(function(c){
          return c.nome && c.nome.toUpperCase().trim() === (o.recipient_name||'').toUpperCase().trim();
        });
      }
      var key = o.codparc || o.recipient_name || o.id;
      if(!clienteMap[key]){
        clienteMap[key] = {
          id: 'cli-'+(o.codparc||key),
          codparc: o.codparc || (cli?cli.codparc:null),
          recipient_name: (cli?cli.nome:null)||o.recipient_name||'—',
          address: (cli?cli.endereco:null)||o.address||'',
          lat: cli&&cli.lat ? parseFloat(cli.lat) : (o.lat?parseFloat(o.lat):null),
          lng: cli&&cli.lng ? parseFloat(cli.lng) : (o.lng?parseFloat(o.lng):null),
          regiao: (cli?cli.regiao:null)||o.regiao||'',
          rota: cli?cli.rota:'',
          bairro: cli?cli.bairro:'',
          cidade: cli?cli.cidade:'Manaus',
          tempo_entrega: cli?cli.tempo_entrega:'0',
          weight_kg: 0,
          pedidos: [],
          order_type: o.order_type||'',
          status: 'pending'
        };
      }
      clienteMap[key].weight_kg += parseFloat(o.weight_kg)||0;
      clienteMap[key].pedidos.push(o.external_id||o.id);
    });

    // Filtra só clientes com GPS
    var items = Object.values(clienteMap).filter(function(c){
      return c.lat && c.lng && Math.abs(c.lat)>0.01;
    });

    window._rotOrdersCache = items;
    console.log('Clientes com pedidos e GPS:', items.length);"""

if old in content:
    content = content.replace(old, new)
    print('loadRotMapData atualizado para usar pedidos!')
else:
    print('Padrão não encontrado!')

# Atualiza InfoWindow para mostrar pedidos
old2 = """      var iw = new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:6px;min-width:200px">'+
        '<b style="font-size:13px">'+(o.recipient_name||'—')+'</b><br>'+
        '<span style="color:#e8521a;font-weight:700">Rota '+(o.rota||o.regiao||'—')+'</span><br>'+
        (o.bairro?'<span style="color:#666">🏘️ '+o.bairro+'</span><br>':'')+
        '<span style="color:#666">⏱️ '+(tempoMin>0?tempoMin+' min':'—')+'</span>'+
        '</div>'
      });"""

new2 = """      var nPedidos = (o.pedidos||[]).length;
      var iw = new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:6px;min-width:200px">'+
        '<b style="font-size:13px">'+(o.recipient_name||'—')+'</b><br>'+
        '<span style="color:#e8521a;font-weight:700">Rota '+(o.rota||o.regiao||'—')+'</span><br>'+
        (o.bairro?'<span style="color:#555">🏘️ '+o.bairro+'</span><br>':'')+
        '<span style="color:#555">📦 '+nPedidos+' pedido(s) | '+o.weight_kg.toFixed(0)+' kg</span><br>'+
        '<span style="color:#555">⏱️ '+(tempoMin>0?tempoMin+' min':'—')+'</span>'+
        '</div>'
      });"""

if old2 in content:
    content = content.replace(old2, new2)
    print('InfoWindow com pedidos!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
