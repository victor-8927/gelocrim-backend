path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = """async function gravarCarga(){
  if(!confOrdem||!confOrdem.length){toast('Nenhum cliente na carga!','error');return;}
  var veicSel=document.getElementById('rot-veiculo-select')?document.getElementById('rot-veiculo-select').value:'';
  var motSel=document.getElementById('sel-motorista')?document.getElementById('sel-motorista').value:'';
  if(!veicSel||!motSel){toast('Selecione veiculo e motorista!','error');return;}
  try{
    var dataSaida=document.getElementById('conf-data-saida')?document.getElementById('conf-data-saida').value:new Date().toISOString().slice(0,10);
    var horaInicio=document.getElementById('conf-hora-inicio')?document.getElementById('conf-hora-inicio').value:'07:30';
    await api('POST','/routes',{vehicle_id:veicSel,driver_id:motSel,date:dataSaida,planned_start:horaInicio,order_ids:confOrdem.map(function(o){return o.id;})});
    toast('Carga gravada com sucesso!','success');
    fecharConferencia();
    loadRoutes();
  }catch(e){toast('Erro ao gravar: '+e.message,'error');}
}"""

new = """async function gravarCarga(){
  if(!confOrdem||!confOrdem.length){toast('Nenhum cliente na carga!','error');return;}
  var veicSel=document.getElementById('rot-veiculo-select')?document.getElementById('rot-veiculo-select').value:'';
  var motSel=document.getElementById('sel-motorista')?document.getElementById('sel-motorista').value:'';
  if(!veicSel||!motSel){toast('Selecione veiculo e motorista!','error');return;}
  try{
    var dataSaida=document.getElementById('conf-data-saida')?document.getElementById('conf-data-saida').value:new Date().toISOString().slice(0,10);
    var horaInicio=document.getElementById('conf-hora-inicio')?document.getElementById('conf-hora-inicio').value:'07:30';
    var orderIds=confOrdem.map(function(o){return o.id;}).filter(function(x){return !!x;});
    console.log('Gravando carga:', orderIds.length, 'pedidos', orderIds);
    var res=await api('POST','/routes',{
      vehicle_id:veicSel,
      driver_id:motSel,
      date:dataSaida,
      planned_start:horaInicio,
      order_ids:orderIds
    });
    toast('Carga gravada! Viagem '+res.trip_number,'success');
    fecharConferencia();
    goTo('rotas',document.querySelector('[data-page="rotas"]'));
  }catch(e){
    console.error('Erro gravarCarga:',e);
    toast('Erro ao gravar: '+e.message,'error');
  }
}"""

if old in content:
    content = content.replace(old, new)
    print('gravarCarga corrigida!')
else:
    print('Padrão não encontrado! Substituindo por posição...')
    idx = content.find('async function gravarCarga()')
    # Encontra o fim da função
    depth = 0
    i = idx
    started = False
    while i < len(content):
        if content[i] == '{':
            depth += 1
            started = True
        elif content[i] == '}':
            depth -= 1
            if started and depth == 0:
                end = i + 1
                break
        i += 1
    content = content[:idx] + new + content[end:]
    print('Substituído por posição!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Limpa rotas antigas sem stops e sem trip_number
import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
deleted = conn.execute("""
    DELETE FROM routes 
    WHERE id NOT IN (SELECT DISTINCT route_id FROM route_stops)
    AND trip_number IS NULL
""").rowcount
conn.commit()
conn.close()
print(f'{deleted} rotas antigas sem stops removidas!')
print('Pronto! Ctrl+Shift+R')
