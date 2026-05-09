path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza e substitui a função verProgressoRota
idx_start = content.find('async function verProgressoRota(')
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

print(f'verProgressoRota: linha {content[:idx_start].count(chr(10))+1}')

nova_func = r"""async function verProgressoRota(id) {
  var modal = document.getElementById('modal-progresso');
  var body  = document.getElementById('modal-prog-body');
  var titulo= document.getElementById('modal-prog-titulo');
  if(!modal) return;
  modal.style.display='flex';
  body.innerHTML='<div class="loading-state">Carregando...</div>';

  function fmtHora(iso) {
    if(!iso) return '—';
    try {
      var d = new Date(iso);
      return d.toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'});
    } catch(e){ return iso; }
  }

  try {
    var stops = await api('GET', '/routes/'+id+'/stops');
    var rotas = await api('GET', '/routes');
    var rota  = rotas.find(function(r){return r.route_id===id;}) || {};

    if(titulo) titulo.textContent = '🗺️ ' + (rota.trip_number||'Rota') + ' — ' + (rota.vehicle_plate||'');

    var completadas = stops.filter(function(s){return s.status==='completed';}).length;
    var falhas      = stops.filter(function(s){return s.status==='failed';}).length;
    var pendentes   = stops.filter(function(s){return s.status==='pending';}).length;
    var pct = stops.length > 0 ? Math.round(completadas/stops.length*100) : 0;

    var corStatus = {pending:'#f59e0b', completed:'#10b981', failed:'#f87171'};
    var lblStatus = {pending:'⏳ Pendente', completed:'✅ Entregue', failed:'❌ Falhou'};

    var linhas = stops.map(function(s) {
      var cor = corStatus[s.status] || '#90afd4';
      var lbl = lblStatus[s.status] || s.status;
      var hora = s.status==='completed' ? fmtHora(s.ata) : (s.status==='failed' ? fmtHora(s.atd) : '—');
      var extra = s.failure_reason ? '<div style="font-size:10px;color:#f87171;margin-top:2px">Motivo: '+s.failure_reason+'</div>' : '';
      return '<tr style="border-bottom:1px solid #1e3a5c">' +
        '<td style="padding:8px;text-align:center;font-weight:700;color:#64B4FF">'+(s.sequence+1)+'</td>'+
        '<td style="padding:8px">'+
          '<b style="color:#e8f0fe">'+(s.recipient_name||'—')+'</b>'+
          '<div style="font-size:10px;color:#90afd4">'+(s.address||'')+'</div>'+
          extra+
        '</td>'+
        '<td style="padding:8px;text-align:center;color:#a78bfa">'+(s.weight_kg||0).toFixed(0)+' kg</td>'+
        '<td style="padding:8px;text-align:center"><span style="font-size:11px;font-weight:700;color:'+cor+'">'+lbl+'</span></td>'+
        '<td style="padding:8px;text-align:center;font-size:12px;color:#90afd4">'+hora+'</td>'+
      '</tr>';
    }).join('');

    var statusRota = {optimized:'⚙️ Conferida',released:'🟢 Liberada',executing:'🚛 Em Execução',done:'✅ Concluída'};
    var badgeRota = statusRota[rota.status] || rota.status || '—';

    body.innerHTML =
      '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">'+
        '<span style="font-size:12px;color:#90afd4">Motorista: <b style="color:#e8f0fe">'+(rota.driver_name||'—')+'</b></span>'+
        '<span style="font-size:12px;color:#64B4FF;font-weight:700">'+badgeRota+'</span>'+
      '</div>'+
      '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">'+
        '<div style="background:#0a1628;border:1px solid #10b981;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:24px;font-weight:800;color:#10b981">'+completadas+'</div>'+
          '<div style="font-size:10px;color:#90afd4">Entregues</div></div>'+
        '<div style="background:#0a1628;border:1px solid #f87171;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:24px;font-weight:800;color:#f87171">'+falhas+'</div>'+
          '<div style="font-size:10px;color:#90afd4">Falhas</div></div>'+
        '<div style="background:#0a1628;border:1px solid #f59e0b;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:24px;font-weight:800;color:#f59e0b">'+pendentes+'</div>'+
          '<div style="font-size:10px;color:#90afd4">Pendentes</div></div>'+
        '<div style="background:#0a1628;border:1px solid #64B4FF;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:24px;font-weight:800;color:#64B4FF">'+pct+'%</div>'+
          '<div style="font-size:10px;color:#90afd4">Progresso</div></div>'+
      '</div>'+
      '<div style="background:#0a1628;border-radius:6px;height:8px;margin-bottom:16px;overflow:hidden">'+
        '<div style="height:100%;background:linear-gradient(90deg,#10b981,#64B4FF);border-radius:6px;width:'+pct+'%;transition:width .5s"></div>'+
      '</div>'+
      '<div style="overflow-x:auto">'+
      '<table style="width:100%;border-collapse:collapse">'+
        '<thead><tr style="background:#061828">'+
          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">#</th>'+
          '<th style="padding:8px;font-size:10px;color:#64B4FF">Cliente</th>'+
          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">Peso</th>'+
          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">Status</th>'+
          '<th style="padding:8px;font-size:10px;color:#64B4FF;text-align:center">Hora</th>'+
        '</tr></thead>'+
        '<tbody>'+linhas+'</tbody>'+
      '</table></div>';

  } catch(e) {
    body.innerHTML = '<div class="loading-state">Erro: '+e.message+'</div>';
  }
}"""

content = content[:idx_start] + nova_func + content[idx_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re, subprocess
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js', 'w', encoding='utf-8') as f:
    f.write(stub + '\n' + js)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr = r.stderr.decode('utf-8', errors='replace')
if r.returncode==0:
    print('VALIDO! Ctrl+Shift+R')
else:
    print('ERRO:', stderr[:300])
