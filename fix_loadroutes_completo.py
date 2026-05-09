path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re, subprocess

# Encontra a função loadRoutes completa e substitui
idx_start = content.find('async function loadRoutes()')
# Encontra o fim da função
depth = 0
i = idx_start
started = False
while i < len(content):
    if content[i] == '{':
        depth += 1
        started = True
    elif content[i] == '}':
        depth -= 1
        if started and depth == 0:
            idx_end = i + 1
            break
    i += 1

print(f'loadRoutes: linha {content[:idx_start].count(chr(10))+1} ate {content[:idx_end].count(chr(10))+1}')

nova_func = r"""async function loadRoutes() {
  var dateEl=document.getElementById('routes-date');
  var statusEl=document.getElementById('routes-status');
  var date=dateEl?dateEl.value:new Date().toISOString().slice(0,10);
  var status=statusEl?statusEl.value:'';
  try{
    var data=await api('GET','/routes?date='+date+(status?'&status='+status:''));
    var tbody=document.getElementById('routes-tbody');
    if(!tbody) return;
    if(!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhuma rota — grave uma carga na Conferência Master</td></tr>';return;}
    var statusLabel={optimized:'Conferida',released:'Liberada',executing:'Em Execução',done:'Concluída',draft:'Rascunho',cancelled:'Cancelada'};
    var rows = data.map(function(r){
      var pct=r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;
      var trip=r.trip_number||'—';
      var btnLib='';
      if(r.status==='optimized'){
        btnLib='<button class="btn btn-sm" style="background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981" onclick="liberarRota(this.dataset.id)" data-id="'+r.route_id+'" title="Liberar">🟢 Liberar</button>';
      }
      var btnExc='';
      if(r.status!=='executing'&&r.status!=='done'){
        btnExc='<button class="btn btn-sm btn-danger" onclick="excluirRota(this.dataset.id)" data-id="'+r.route_id+'" title="Excluir">🗑️</button>';
      }
      var tr='<tr>';
      tr+='<td><input type="checkbox" class="rota-chk" data-id="'+r.route_id+'"></td>';
      tr+='<td><b style="font-family:monospace;color:#64B4FF;font-size:12px">'+trip+'</b></td>';
      tr+='<td><b style="color:#64B4FF">'+(r.vehicle_plate||r.vda||'—')+'</b></td>';
      tr+='<td>'+(r.driver_name||'—')+'</td>';
      tr+='<td style="font-size:12px">'+(r.date||'—')+'</td>';
      tr+='<td><div style="display:flex;align-items:center;gap:8px"><div style="flex:1;background:#1e3a5c;border-radius:3px;height:6px"><div style="height:100%;background:#10b981;border-radius:3px;width:'+pct+'%"></div></div><span style="font-size:11px;color:#90afd4">'+pct+'% ('+r.total_stops+' paradas)</span></div></td>';
      tr+='<td style="font-size:11px">'+(r.total_distance_km||'—')+' km</td>';
      tr+='<td style="font-size:12px">'+(r.planned_start||'—')+'</td>';
      tr+='<td><span class="badge '+(r.status||'draft')+'">'+(statusLabel[r.status]||r.status||'draft')+'</span></td>';
      tr+='<td style="display:flex;gap:6px;flex-wrap:wrap">'+btnLib+'<button class="btn btn-sm btn-secondary" onclick="verProgressoRota(this.dataset.id)" data-id="'+r.route_id+'">👁 Ver</button>'+btnExc+'</td>';
      tr+='</tr>';
      return tr;
    });
    tbody.innerHTML=rows.join('');
  }catch(e){toast('Erro: '+e.message,'error');}
}"""

content = content[:idx_start] + nova_func + content[idx_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeInfo:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('Script 2 VALIDO! Ctrl+Shift+R')
else:
    print('ERRO:', stderr[:400])
