path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona loadRotMapData no script 3, após as funções de roteirização
old = '''// ── VEÍCULOS EDIÇÃO ──────────────────────────────────────────────'''

new = '''// ── ROTEIRIZAÇÃO LOAD ────────────────────────────────────────────
async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando clientes...';
  console.log('loadRotMapData iniciado!');
  try{
    var clientes = await api('GET','/clientes');
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
    console.log('Items com GPS:', items.length);

    // Popula filtro de rotas
    var selRota=document.getElementById('rot-filtro-rota');
    if(selRota){
      var rotasFixas=['801','802','803','804','805','811','821','822'];
      selRota.innerHTML='<option value="">🗺️ Todas as rotas</option>'+
        rotasFixas.map(function(r){
          var count=items.filter(function(o){return (o.rota||o.regiao||'').indexOf(r)>=0;}).length;
          return count>0?'<option value="'+r+'">Rota '+r+' ('+count+')</option>':'';
        }).join('');
    }
    // Popula filtro de regiões
    var selReg=document.getElementById('rot-filtro-regiao');
    if(selReg){
      var regs={};
      items.forEach(function(o){if(o.regiao)regs[o.regiao]=1;});
      selReg.innerHTML='<option value="">📍 Todas regiões</option>'+
        Object.keys(regs).sort().map(function(r){return '<option value="'+r+'">'+r+'</option>';}).join('');
    }
    // Popula filtro de bairros
    var selB=document.getElementById('rot-filtro-bairro');
    if(selB){
      var bairros={};
      items.forEach(function(o){if(o.bairro)bairros[o.bairro]=1;});
      selB.innerHTML='<option value="">🏘️ Todos bairros</option>'+
        Object.keys(bairros).sort().map(function(b){return '<option value="'+b+'">'+b+'</option>';}).join('');
    }

    if(statusEl) statusEl.textContent=items.length+' clientes com GPS';
    renderRotMapMarkers(items);
  }catch(e){
    console.error('Erro loadRotMapData:',e);
    if(statusEl) statusEl.textContent='Erro: '+e.message;
  }
}

// ── VEÍCULOS EDIÇÃO ──────────────────────────────────────────────'''

if old in content:
    content = content.replace(old, new, 1)
    print('loadRotMapData adicionado!')
else:
    print('Âncora não encontrada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re, subprocess
matches = list(re.finditer(r'async function loadRotMapData\(\)', content))
print(f'loadRotMapData: {len(matches)} versões')
for m in matches:
    ln = content[:m.start()].count('\n')+1
    print(f'  linha {ln}')
print('Pronto! Ctrl+Shift+R.')
