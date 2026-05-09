path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a função verProgressoRota (atualmente vazia)
old = 'function verProgressoRota(id){}'

new = '''async function verProgressoRota(id) {
  var modal = document.getElementById('modal-progresso');
  var body  = document.getElementById('modal-prog-body');
  var titulo= document.getElementById('modal-prog-titulo');
  if(!modal) return;
  modal.style.display='flex';
  body.innerHTML='<div class="loading-state">Carregando...</div>';

  try {
    // Busca stops da rota
    var stops = await api('GET', '/routes/'+id+'/stops');
    var rotas = await api('GET', '/routes');
    var rota  = rotas.find(function(r){return r.route_id===id;}) || {};

    if(titulo) titulo.textContent = '🗺️ ' + (rota.trip_number||'Rota') + ' — ' + (rota.vehicle_plate||'');

    var completadas = stops.filter(function(s){return s.status==='completed';}).length;
    var falhas      = stops.filter(function(s){return s.status==='failed';}).length;
    var pendentes   = stops.filter(function(s){return s.status==='pending';}).length;
    var pct = stops.length > 0 ? Math.round(completadas/stops.length*100) : 0;

    var statusLabel = {pending:'⏳ Pendente', completed:'✅ Entregue', failed:'❌ Falhou'};
    var statusBadge = {pending:'#f59e0b', completed:'#10b981', failed:'#f87171'};

    var linhas = stops.map(function(s, i) {
      var cor = statusBadge[s.status] || '#90afd4';
      var lbl = statusLabel[s.status] || s.status;
      return '<tr style="border-bottom:1px solid #1e3a5c">'+
        '<td style="padding:8px;text-align:center;font-weight:700;color:#64B4FF">'+(s.sequence+1)+'</td>'+
        '<td style="padding:8px"><b style="color:#e8f0fe">'+(s.recipient_name||'—')+'</b>'+
          '<div style="font-size:10px;color:#90afd4">'+(s.address||'')+'</div></td>'+
        '<td style="padding:8px;text-align:center;color:#a78bfa">'+(s.weight_kg||0)+' kg</td>'+
        '<td style="padding:8px;text-align:center"><span style="font-size:11px;font-weight:700;color:'+cor+'">'+lbl+'</span></td>'+
        '<td style="padding:8px;text-align:center;font-size:11px;color:#90afd4">'+(s.ata||s.eta||'—')+'</td>'+
      '</tr>';
    }).join('');

    body.innerHTML =
      '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">'+
        '<div style="background:#0a1628;border:1px solid #10b981;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:22px;font-weight:800;color:#10b981">'+completadas+'</div>'+
          '<div style="font-size:10px;color:#90afd4">Entregues</div></div>'+
        '<div style="background:#0a1628;border:1px solid #f87171;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:22px;font-weight:800;color:#f87171">'+falhas+'</div>'+
          '<div style="font-size:10px;color:#90afd4">Falhas</div></div>'+
        '<div style="background:#0a1628;border:1px solid #f59e0b;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:22px;font-weight:800;color:#f59e0b">'+pendentes+'</div>'+
          '<div style="font-size:10px;color:#90afd4">Pendentes</div></div>'+
        '<div style="background:#0a1628;border:1px solid #64B4FF;border-radius:8px;padding:12px;text-align:center">'+
          '<div style="font-size:22px;font-weight:800;color:#64B4FF">'+pct+'%</div>'+
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
}'''

if old in content:
    content = content.replace(old, new)
    print('verProgressoRota implementada!')
else:
    print('Função não encontrada!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R')
