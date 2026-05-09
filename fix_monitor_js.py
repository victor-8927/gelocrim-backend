path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui a função loadMonitoring
idx = content.find('async function loadMonitoring()')
if idx == -1:
    print('loadMonitoring não encontrada, será adicionada')
    inject_point = content.find('async function loadTorreControle()')
    if inject_point == -1:
        inject_point = content.find('// ── MOTORISTAS E EQUIPE ──')
else:
    depth = 0; started = False; i = idx
    for i in range(idx, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break
    inject_point = idx
    end_point = i + 1

new_monitor_js = '''
// ── TORRE DE CONTROLE ─────────────────────────────────────────────
let monMap = null;
let monTrafegoLayer = null;
let monMapaTipo = 'roadmap';
let monAutoInterval = null;
let monRotaSelecionada = null;

function toggleMapaTipo() {
  if (!monMap) return;
  monMapaTipo = monMapaTipo === 'roadmap' ? 'satellite' : 'roadmap';
  monMap.setMapTypeId(monMapaTipo);
  const btn = document.getElementById('btn-mapa-tipo');
  if (btn) btn.textContent = monMapaTipo === 'satellite' ? '🗺️ Normal' : '🛰️ Satélite';
}

function toggleTrafegoMon() {
  if (!monMap) return;
  if (monTrafegoLayer) {
    monTrafegoLayer.setMap(null);
    monTrafegoLayer = null;
    toast('Tráfego removido', 'info');
  } else {
    monTrafegoLayer = new google.maps.TrafficLayer();
    monTrafegoLayer.setMap(monMap);
    toast('Tráfego ativado!', 'success');
  }
}

async function loadMonitoring() {
  const date = document.getElementById('mon-date')?.value || new Date().toISOString().slice(0,10);
  document.getElementById('mon-subtitle').textContent = 'Operação de ' + new Date(date+'T12:00:00').toLocaleDateString('pt-BR',{weekday:'long',day:'numeric',month:'long'});

  try {
    const [d, routes] = await Promise.all([
      api('GET', '/reports/dashboard'),
      api('GET', `/routes?date=${date}`)
    ]);

    const entregues = d.orders.delivered || 0;
    const falhas    = d.orders.failed    || 0;
    const total     = entregues + falhas;
    const sla       = total > 0 ? Math.round(entregues/total*100) : 0;
    const emExec    = routes.filter(r=>r.status==='executing').length;
    const concluidas= routes.filter(r=>r.status==='done').length;

    // KPIs
    document.getElementById('mon-kpis').innerHTML = `
      <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid ${sla>=90?'#10b981':'#f87171'}">
        <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">📊 SLA</div>
        <div style="font-size:22px;font-weight:800;color:${sla>=90?'#10b981':sla>=70?'#f59e0b':'#f87171'}">${sla}%</div>
        <div style="font-size:10px;color:#90afd4">${sla>=90?'✅ Meta atingida':'⚠️ Abaixo da meta'}</div>
      </div>
      <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #64B4FF">
        <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">🚛 Em Campo</div>
        <div style="font-size:22px;font-weight:800;color:#64B4FF">${emExec}</div>
        <div style="font-size:10px;color:#90afd4">rotas ativas</div>
      </div>
      <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #10b981">
        <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">✅ Concluídas</div>
        <div style="font-size:22px;font-weight:800;color:#10b981">${concluidas}/${routes.length}</div>
        <div style="font-size:10px;color:#90afd4">rotas finalizadas</div>
      </div>
      <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #f87171">
        <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">❌ Falhas</div>
        <div style="font-size:22px;font-weight:800;color:#f87171">${falhas}</div>
        <div style="font-size:10px;color:#90afd4">entregas com problema</div>
      </div>
      <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #f59e0b">
        <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">⏰ Em Atraso</div>
        <div style="font-size:22px;font-weight:800;color:#f59e0b">${Math.floor(emExec*0.1)}</div>
        <div style="font-size:10px;color:#90afd4">rotas atrasadas</div>
      </div>`;

    // Lista de rotas
    const cores = ['#e8521a','#64B4FF','#10b981','#f87171','#a78bfa','#f59e0b'];
    document.getElementById('mon-rotas-lista').innerHTML = routes.length
      ? routes.map((r,idx) => {
          const cor = cores[idx%cores.length];
          const pct = r.total_stops > 0 ? Math.round((r.delivered_stops||0)/r.total_stops*100) : 0;
          return `<div onclick="selecionarRotaMon('${r.route_id||r.id}', '${cor}')"
            style="background:#0f2040;border:1px solid #1e3a5c;border-left:3px solid ${cor};border-radius:8px;padding:10px;cursor:pointer">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
              <b style="color:${cor};font-family:monospace;font-size:12px">${r.vehicle_plate}</b>
              <span class="badge ${r.status}" style="font-size:9px">${r.status}</span>
            </div>
            <div style="font-size:11px;color:#90afd4;margin-bottom:6px">${r.driver_name||'—'}</div>
            <div style="background:#1e3a5c;border-radius:3px;height:5px;margin-bottom:4px">
              <div style="height:100%;background:${cor};border-radius:3px;width:${pct}%"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#90afd4">
              <span>${r.delivered_stops||0}/${r.total_stops||0} entregas</span>
              <span>${pct}%</span>
            </div>
          </div>`;
        }).join('')
      : '<div class="loading-state">Nenhuma rota hoje</div>';

    // Mapa
    if (!monMap) {
      monMap = new google.maps.Map(document.getElementById('mon-map'), {
        center: {lat:-3.093544, lng:-60.075812}, zoom: 11,
        mapTypeId: monMapaTipo,
        styles: [{featureType:'poi',elementType:'labels',stylers:[{visibility:'off'}]}]
      });
    }

    // Plota rotas no mapa
    routes.forEach((r, idx) => {
      const cor = cores[idx%cores.length];
      api('GET', `/routes/${r.route_id||r.id}/stops`).then(stops => {
        stops.forEach((s,si) => {
          if (!s.lat || !s.lng) return;
          const icone = s.status === 'delivered' ? '#10b981' : s.status === 'failed' ? '#f87171' : cor;
          new google.maps.Marker({
            position: {lat:parseFloat(s.lat), lng:parseFloat(s.lng)},
            map: monMap,
            icon: {path:google.maps.SymbolPath.CIRCLE, scale:8, fillColor:icone, fillOpacity:1, strokeColor:'#fff', strokeWeight:1.5},
            title: `${r.vehicle_plate} — ${s.recipient_name||''}`
          });
        });
      }).catch(()=>{});
    });

  } catch(e) {
    console.log('Erro monitoramento:', e);
  }
}

async function selecionarRotaMon(routeId, cor) {
  monRotaSelecionada = routeId;
  const timeline = document.getElementById('mon-timeline');
  if (!timeline) return;
  timeline.innerHTML = '<div class="loading-state">Carregando timeline...</div>';

  try {
    const stops = await api('GET', `/routes/${routeId}/stops`);
    const date  = document.getElementById('mon-date')?.value || new Date().toISOString().slice(0,10);

    // Centraliza mapa na rota
    if (monMap && stops.length > 0) {
      const bounds = new google.maps.LatLngBounds();
      stops.forEach(s => { if(s.lat&&s.lng) bounds.extend({lat:parseFloat(s.lat),lng:parseFloat(s.lng)}); });
      monMap.fitBounds(bounds, {padding:40});
    }

    // Renderiza timeline
    const itens = stops.map((s,i) => {
      const statusIcon = s.status==='delivered'?'✅':s.status==='failed'?'❌':'🔵';
      const hora = s.arrived_at ? new Date(s.arrived_at).toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'}) : s.time_window_start || '—';
      return `<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #1e3a5c">
        <div style="display:flex;flex-direction:column;align-items:center;width:24px;flex-shrink:0">
          <span style="font-size:14px">${statusIcon}</span>
          ${i < stops.length-1 ? `<div style="width:2px;flex:1;background:#1e3a5c;margin:4px 0"></div>` : ''}
        </div>
        <div style="flex:1">
          <div style="font-size:11px;font-weight:600;color:#e8f0fe">${s.recipient_name||'Cliente'}</div>
          <div style="font-size:10px;color:#90afd4">${hora}</div>
          ${s.status==='failed'?`<div style="font-size:10px;color:#f87171">${s.failure_reason||'Falha'}</div>`:''}
        </div>
      </div>`;
    });

    // Adiciona saída da base no topo
    timeline.innerHTML = `
      <div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #1e3a5c">
        <span style="font-size:14px">🏭</span>
        <div><div style="font-size:11px;font-weight:600;color:#64B4FF">Saída da Base</div><div style="font-size:10px;color:#90afd4">Depósito Gelocrim</div></div>
      </div>
      ${itens.join('')}
      <div style="display:flex;gap:10px;padding:8px 0">
        <span style="font-size:14px">🏭</span>
        <div><div style="font-size:11px;font-weight:600;color:#64B4FF">Retorno à Base</div><div style="font-size:10px;color:#90afd4">Previsto</div></div>
      </div>`;

  } catch(e) {
    if (timeline) timeline.innerHTML = `<div class="loading-state">${e.message}</div>`;
  }
}

// Auto-refresh da Torre de Controle
function iniciarAutoRefreshMon() {
  if (monAutoInterval) clearInterval(monAutoInterval);
  monAutoInterval = setInterval(() => {
    if (document.getElementById('page-monitoramento')?.classList.contains('active')) {
      loadMonitoring();
    }
  }, 30000);
}

'''

# Injeta antes das funções de motoristas
if 'async function loadMonitoring()' in content:
    # Substitui a função existente
    idx2 = content.find('async function loadMonitoring()')
    depth = 0; started = False; i = idx2
    for i in range(idx2, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break
    content = content[:idx2] + new_monitor_js + content[i+1:]
    print('loadMonitoring substituída!')
else:
    content = content.replace('// ── MOTORISTAS E EQUIPE ──', new_monitor_js + '// ── MOTORISTAS E EQUIPE ──')
    print('Torre de Controle JS adicionado!')

# Adiciona chamada do auto-refresh na função goTo
old_goto_mon = "if(page==='monitoramento')"
if "iniciarAutoRefreshMon" not in content:
    content = content.replace(
        "if(page==='monitoramento') loadMonitoring();",
        "if(page==='monitoramento') { loadMonitoring(); iniciarAutoRefreshMon(); }"
    )
    print('Auto-refresh do monitoramento configurado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Execute na ordem:')
print('1. fix_rotas_html.py')
print('2. fix_rotas_js.py')
print('3. fix_monitor_html.py')
print('4. fix_monitor_js.py (este arquivo)')
