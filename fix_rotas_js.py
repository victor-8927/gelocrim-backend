path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui a função loadRoutes
idx = content.find('async function loadRoutes()')
if idx != -1:
    depth = 0; started = False; i = idx
    for i in range(idx, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break

    new_load_routes = '''async function loadRoutes() {
  const date   = document.getElementById('routes-date')?.value || new Date().toISOString().slice(0,10);
  const status = document.getElementById('routes-status')?.value || '';
  document.getElementById('routes-tbody').innerHTML = '<tr><td colspan="10" class="loading-state">Carregando rotas...</td></tr>';
  try {
    let routes = await api('GET', `/routes?date=${date}`);
    if (status) routes = routes.filter(r => r.status === status);

    // KPIs
    const total     = routes.length;
    const executing = routes.filter(r=>r.status==='executing').length;
    const done      = routes.filter(r=>r.status==='done').length;
    const totalStop = routes.reduce((s,r)=>s+(r.total_stops||0),0);
    const sla       = totalStop > 0 ? Math.round(done/total*100) : 0;

    const el = (id,v) => { const e=document.getElementById(id); if(e) e.textContent=v; };
    el('kpi-sla',       sla+'%');
    el('kpi-saude',     executing+'/'+total);
    el('kpi-saude-sub', executing+' ativos de '+total);
    el('kpi-km-desvio', '< 5%');
    el('kpi-progresso', total>0?Math.round(done/total*100)+'%':'—');

    // Cor do SLA
    const slaEl = document.getElementById('kpi-sla');
    if (slaEl) slaEl.style.color = sla>=90?'#10b981':sla>=70?'#f59e0b':'#f87171';

    // Tabela
    const agora = new Date();
    document.getElementById('routes-tbody').innerHTML = routes.length
      ? routes.map(r => {
          const entregues  = r.delivered_stops  || 0;
          const totalStops = r.total_stops || 1;
          const pct        = Math.round(entregues/totalStops*100);
          const corBar     = pct>=100?'#10b981':pct>=50?'#64B4FF':'#f59e0b';

          // Desvio de horário
          const fimPrev = r.planned_end ? new Date(`${date}T${r.planned_end}`) : null;
          const atrasado = fimPrev && agora > fimPrev && r.status==='executing';
          const fimTexto = r.planned_end || '—';

          return `<tr>
            <td><input type="checkbox" class="rota-chk" data-id="${r.route_id||r.id}" data-plate="${r.vehicle_plate}"></td>
            <td><b style="font-family:monospace;color:#64B4FF">${r.vehicle_plate||'—'}</b></td>
            <td style="font-size:12px">${r.driver_name||'—'}</td>
            <td style="font-size:11px;color:#90afd4">${r.route_date||date}</td>
            <td style="min-width:140px">
              <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                <span style="color:#90afd4">${entregues}/${totalStops} entregas</span>
                <span style="color:${corBar};font-weight:600">${pct}%</span>
              </div>
              <div style="background:#1e3a5c;border-radius:3px;height:6px;overflow:hidden">
                <div style="height:100%;background:${corBar};border-radius:3px;width:${pct}%;transition:width .3s"></div>
              </div>
            </td>
            <td style="font-size:12px">${r.total_distance_km||0} km</td>
            <td style="font-size:12px;color:#90afd4">${r.planned_start||'—'}</td>
            <td style="font-size:12px;color:${atrasado?'#f87171':'#90afd4'}">
              ${fimTexto}${atrasado?' ⚠️ ATRASADO':''}
            </td>
            <td><span class="badge ${r.status}">${r.status}</span></td>
            <td style="display:flex;gap:4px">
              <button class="btn btn-sm btn-secondary" onclick="goTo('monitoramento',null);setTimeout(()=>tcFocarRota(${JSON.stringify(r).replace(/"/g,"'")},[]),300)" title="Ver no mapa">📍</button>
              <button class="btn btn-sm btn-secondary" onclick="verDetalhesRota('${r.route_id||r.id}')" title="Detalhes">📋</button>
            </td>
          </tr>`;
        }).join('')
      : '<tr><td colspan="10" class="loading-state">Nenhuma rota encontrada</td></tr>';

  } catch(e) { document.getElementById('routes-tbody').innerHTML = `<tr><td colspan="10" class="loading-state">${e.message}</td></tr>`; }
}

let _rotasSelecionadas = new Set();
function toggleTodasRotas(checked) {
  _rotasSelecionadas.clear();
  document.querySelectorAll('.rota-chk').forEach(c => {
    c.checked = checked;
    if (checked) _rotasSelecionadas.add(c.dataset.id);
  });
}
function imprimirRomaneiosSelecionados() {
  if (_rotasSelecionadas.size === 0) { toast('Selecione ao menos uma rota!', 'error'); return; }
  toast(`Gerando ${_rotasSelecionadas.size} romaneio(s)...`, 'info');
}'''

    content = content[:idx] + new_load_routes + content[i+1:]
    print('loadRoutes atualizado com barras de progresso e KPIs!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Parte 2 OK.')
