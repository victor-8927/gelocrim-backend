path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Atualiza o cabeçalho da tabela de rotas para incluir Nº Viagem
old_th = '''<th style="width:30px"><input type="checkbox" id="chk-all-rotas" onchange="toggleTodasRotas(this.checked)"></th>
                <th>Veículo</th>
                <th>Motorista</th>
                <th>Data</th>
                <th>Progresso</th>
                <th>Distância</th>
                <th>Início Prev.</th>
                <th>Fim Prev. / Real</th>
                <th>Status</th>
                <th>Ações</th>'''

new_th = '''<th style="width:30px"><input type="checkbox" id="chk-all-rotas" onchange="toggleTodasRotas(this.checked)"></th>
                <th>Nº Viagem</th>
                <th>Veículo</th>
                <th>Motorista</th>
                <th>Data</th>
                <th>Progresso</th>
                <th>Distância</th>
                <th>Início Prev.</th>
                <th>Status</th>
                <th>Ações</th>'''

if old_th in content:
    content = content.replace(old_th, new_th)
    print('Cabeçalho tabela rotas atualizado!')
else:
    print('Cabeçalho não encontrado!')

# 2. Substitui a função loadRoutes para mostrar trip_number e botão Liberar
old_func = '''async function loadRoutes() {
  var dateEl=document.getElementById('routes-date');
  var statusEl=document.getElementById('routes-status');
  var date=dateEl?dateEl.value:new Date().toISOString().slice(0,10);
  var status=statusEl?statusEl.value:'';
  try{
    var data=await api('GET','/routes?date='+date+(status?'&status='+status:''));
    var tbody=document.getElementById('routes-tbody');
    if(!tbody) return;
    if(!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhuma rota</td></tr>';return;}
    tbody.innerHTML=data.map(function(r){
      var pct=r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;
      return '<tr>'+
        '<td><input type="checkbox" class="rota-chk" data-id="'+r.route_id+'"></td>'+
        '<td><b style="color:#64B4FF">'+r.vehicle_plate+'</b></td>'+
        '<td>'+(r.driver_name||'—')+'</td>'+
        '<td>'+r.date+'</td>'+
        '<td><div style="display:flex;align-items:center;gap:8px">'+
        '<div style="flex:1;background:#1e3a5c;border-radius:3px;height:6px">'+
        '<div style="height:100%;background:#10b981;border-radius:3px;width:'+pct+'%"></div></div>'+
        '<span style="font-size:11px;color:#90afd4">'+pct+'%</span></div></td>'+
        '<td style="font-size:11px">'+(r.total_distance_km||'—')+' km</td>'+
        '<td>'+(r.planned_start||'—')+'</td>'+
        '<td>'+(r.planned_end||'—')+'</td>'+
        '<td><span class="badge '+(r.status||'draft')+'">'+(r.status||'draft')+'</span></td>'+
        '<td><button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">Ver</button></td>'+
        '</tr>';
    }).join('');
  }catch(e){toast('Erro: '+e.message,'error');}
}'''

new_func = '''async function loadRoutes() {
  var dateEl=document.getElementById('routes-date');
  var statusEl=document.getElementById('routes-status');
  var date=dateEl?dateEl.value:new Date().toISOString().slice(0,10);
  var status=statusEl?statusEl.value:'';
  try{
    var data=await api('GET','/routes?date='+date+(status?'&status='+status:''));
    var tbody=document.getElementById('routes-tbody');
    if(!tbody) return;
    if(!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhuma rota — grave uma carga na Conferência Master</td></tr>';return;}
    var statusLabel={'optimized':'Conferida','released':'Liberada','executing':'Em Execução','done':'Concluída','draft':'Rascunho','cancelled':'Cancelada'};
    tbody.innerHTML=data.map(function(r){
      var pct=r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;
      var trip=r.trip_number||'—';
      var btnLiberar='';
      if(r.status==='optimized'){
        btnLiberar='<button class="btn btn-sm" style="background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981" '+
          'onclick="liberarRota(\''+r.route_id+'\')" title="Liberar para motorista">🟢 Liberar</button>';
      }
      return '<tr>'+
        '<td><input type="checkbox" class="rota-chk" data-id="'+r.route_id+'"></td>'+
        '<td><b style="font-family:monospace;color:#64B4FF;font-size:12px">'+trip+'</b></td>'+
        '<td><b style="color:#64B4FF">'+(r.vehicle_plate||r.vda||'—')+'</b></td>'+
        '<td>'+(r.driver_name||'—')+'</td>'+
        '<td style="font-size:12px">'+(r.date||'—')+'</td>'+
        '<td><div style="display:flex;align-items:center;gap:8px">'+
        '<div style="flex:1;background:#1e3a5c;border-radius:3px;height:6px">'+
        '<div style="height:100%;background:#10b981;border-radius:3px;width:'+pct+'%"></div></div>'+
        '<span style="font-size:11px;color:#90afd4">'+pct+'% ('+r.total_stops+' paradas)</span></div></td>'+
        '<td style="font-size:11px">'+(r.total_distance_km||'—')+' km</td>'+
        '<td style="font-size:12px">'+(r.planned_start||'—')+'</td>'+
        '<td><span class="badge '+(r.status||'draft')+'">'+(statusLabel[r.status]||r.status||'draft')+'</span></td>'+
        '<td style="display:flex;gap:6px;flex-wrap:wrap">'+
          btnLiberar+
          '<button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">👁 Ver</button>'+
        '</td>'+
        '</tr>';
    }).join('');
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function liberarRota(routeId) {
  if(!confirm('Liberar esta rota para o motorista?')) return;
  try{
    await api('POST', '/routes/'+routeId+'/liberar');
    toast('✅ Rota liberada! Motorista já pode ver no app.','success');
    loadRoutes();
  }catch(e){toast('Erro: '+e.message,'error');}
}'''

if old_func in content:
    content = content.replace(old_func, new_func)
    print('loadRoutes atualizado com trip_number e botão Liberar!')
else:
    print('loadRoutes não encontrado! Buscando variação...')
    idx = content.find('async function loadRoutes()')
    print(f'  loadRoutes encontrada na linha: {content[:idx].count(chr(10))+1}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
