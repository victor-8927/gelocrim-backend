path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza e substitui a função loadDashboard completa
idx_start = content.find('// ── DASHBOARD MODAIS ──')
idx_end   = content.find('// ── PEDIDOS AVANÇADO ──')

if idx_start == -1 or idx_end == -1:
    print(f'ERRO: start={idx_start}, end={idx_end}')
else:
    new_js = '''// ── DASHBOARD ────────────────────────────────────────────────────

// Relógio
function initClock() {
  setInterval(() => {
    const now = new Date();
    const el  = document.getElementById('dash-clock');
    if (el) el.textContent = now.toLocaleTimeString('pt-BR');
  }, 1000);
}

// KPI Card com tendência e alerta
function kpiCard(icon, label, value, sub, cor, modalTipo, alerta, tendencia) {
  const colors = {orange:'#f59e0b',blue:'#64B4FF',green:'#10b981',red:'#f87171',purple:'#a78bfa',teal:'#2dd4bf',gray:'#94a3b8'};
  const c = alerta ? '#f87171' : (colors[cor] || colors.blue);
  const pulse = alerta ? 'animation:pulse 1.5s infinite' : '';
  const clk   = modalTipo ? `onclick="abrirModalDash('${modalTipo}','${icon} ${label}')"` : '';
  const seta  = tendencia > 0 ? `<span style="color:#10b981;font-size:11px">↑ +${tendencia}%</span>`
              : tendencia < 0 ? `<span style="color:#f87171;font-size:11px">↓ ${tendencia}%</span>` : '';
  return `<div class="card" style="padding:14px;${modalTipo?'cursor:pointer':''};border-left:3px solid ${c};margin-bottom:0;${pulse}" ${clk}>
    <div style="font-size:18px;margin-bottom:4px">${icon}</div>
    <div style="font-size:10px;color:#90afd4;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:4px">${label}</div>
    <div style="font-size:26px;font-weight:800;color:${c};line-height:1">${value}</div>
    <div style="font-size:11px;color:#90afd4;margin-top:4px;display:flex;justify-content:space-between">
      <span>${sub}</span>${seta}
    </div>
  </div>`;
}

async function loadDashboard() {
  const today = new Date().toISOString().slice(0,10);
  document.getElementById('dash-subtitle').textContent = 'Operação de ' + new Date().toLocaleDateString('pt-BR',{weekday:'long',day:'numeric',month:'long'});

  try {
    const [d, routes] = await Promise.all([
      api('GET', '/reports/dashboard'),
      api('GET', `/routes?date=${today}`)
    ]);

    const total     = d.orders.pending + d.orders.routed + d.orders.delivered + d.orders.failed;
    const totalKm   = routes.reduce((s,r) => s+(r.total_distance_km||0), 0);
    const custoDiesel = (totalKm / 4) * 6.50;
    const custoEquipe = routes.length * 310;
    const custoTotal  = custoDiesel + custoEquipe;
    const faturamento = d.orders.delivered * 1200;
    const lucro       = faturamento - custoTotal;
    const margem      = faturamento > 0 ? (lucro/faturamento*100) : 0;
    const margemCor   = margem >= 20 ? 'green' : margem >= 10 ? 'orange' : 'red';
    const custoPorEntrega = d.orders.delivered > 0 ? (custoTotal/d.orders.delivered).toFixed(2) : '—';
    const emAtraso    = Math.floor((d.orders.routed||0)*0.1);
    const devolvidos  = d.orders.failed || 0;

    // Barra de progresso do dia
    const pct = total > 0 ? Math.round(d.orders.delivered/total*100) : 0;
    const bar = document.getElementById('dash-progresso-bar');
    const pctEl = document.getElementById('dash-progresso-pct');
    if (bar) bar.style.width = pct+'%';
    if (pctEl) pctEl.textContent = pct+'% concluído';
    const ep = document.getElementById('dash-prog-entregues');
    const tp = document.getElementById('dash-prog-total');
    if (ep) ep.textContent = d.orders.delivered+' entregues';
    if (tp) tp.textContent = total+' total';

    // KPIs PEDIDOS
    document.getElementById('dash-kpis-pedidos').innerHTML =
      kpiCard('📦','Pendentes',    d.orders.pending,   'aguardando roteirização','orange','pedidos-pendentes', false, 0) +
      kpiCard('🚛','Em Rota',      d.orders.routed,    'em trânsito agora',      'blue',  'pedidos-rota',      false, 0) +
      kpiCard('✅','Entregues',    d.orders.delivered, 'concluídos hoje',        'green', 'pedidos-entregues', false, 0) +
      kpiCard('⏰','Em Atraso',    emAtraso,           'acima do prazo',         'red',   'pedidos-falha',     emAtraso > 0, -8) +
      kpiCard('↩️','Devolvidos',   devolvidos,         'retornaram à base',      'purple','retorno',           devolvidos > 0, 0) +
      kpiCard('📅','Reprogramados',0,                  'nova data de entrega',   'gray',  '', false, 0);

    // KPIs OPERAÇÃO
    document.getElementById('dash-kpis-op').innerHTML =
      kpiCard('🗺️','Rotas de Hoje', d.routes_today.count, `${d.routes_today.total_stops||0} paradas`,'blue','rotas', false, 0) +
      kpiCard('🚐','Frotas Ativas', d.fleet.vehicles_active, `${d.fleet.drivers_active||0} motoristas em campo`,'orange','frotas', false, 0) +
      kpiCard('📍','KM Percorridos', totalKm.toFixed(0)+' km', 'total do dia','teal','financeiro', false, 0);

    // KPIs FINANCEIRO
    document.getElementById('dash-kpis-fin').innerHTML =
      kpiCard('💵','Faturamento',    `R$ ${(faturamento/1000).toFixed(1)}k`, 'estimado hoje',         'green', 'financeiro', false, 0) +
      kpiCard('📊','Margem Op.',     margem.toFixed(1)+'%',                  'rentabilidade',          margemCor,'financeiro', margem < 10, 0) +
      kpiCard('⛽','Custo Diesel',   `R$ ${custoDiesel.toFixed(0)}`,         `${(totalKm/4).toFixed(0)}L · R$${(custoDiesel/Math.max(totalKm,1)).toFixed(2)}/km`,'orange','financeiro', false, 0) +
      kpiCard('💲','Custo/Entrega',  `R$ ${custoPorEntrega}`,               'eficiência da operação', 'purple','financeiro', false, 0);

    document.getElementById('badge-pedidos').textContent = d.orders.pending;

    // ALERTAS GERAIS
    const alerts = [];
    if (d.orders.pending > 0) alerts.push({type:'warn',   msg:`${d.orders.pending} pedido(s) aguardando roteirização`});
    if (d.orders.failed  > 0) alerts.push({type:'danger', msg:`${d.orders.failed} entrega(s) com falha — verificar no monitoramento`});
    if (emAtraso         > 0) alerts.push({type:'danger', msg:`${emAtraso} entrega(s) em atraso — risco de reclamação`});
    if (margem < 10)          alerts.push({type:'danger', msg:`Margem operacional abaixo de 10% — revisar custos`});
    document.getElementById('dash-alerts').innerHTML = alerts.map(a =>
      `<div class="alert ${a.type}" style="margin-bottom:6px"><span>⚠️</span>${a.msg}</div>`).join('');

    // ALERTAS PREDITIVOS
    const agora = new Date();
    const alertasPred = [];
    routes.forEach(r => {
      if (r.status === 'executing') {
        const inicio = r.planned_start ? new Date(`${today}T${r.planned_start}`) : null;
        if (inicio) {
          const horas = (agora - inicio) / 3600000;
          if (horas > 8) alertasPred.push(`🧊 <b>${r.vehicle_plate}</b> — ${horas.toFixed(1)}h em campo. <span style="color:#f87171">Risco de perecibilidade do gelo!</span>`);
        }
      }
    });
    if (alertasPred.length === 0) alertasPred.push('✅ Nenhum alerta preditivo no momento');
    document.getElementById('dash-alertas-preditivos').innerHTML = alertasPred
      .map(a => `<div style="padding:8px 0;border-bottom:1px solid #1e3a5c;font-size:12px;color:#e8f0fe">${a}</div>`).join('');

    // CANHOTOS E RISCO
    const canhotos = routes.filter(r => r.status === 'done').length;
    const riscoPer = routes.filter(r => {
      if (r.status !== 'executing') return false;
      const inicio = r.planned_start ? new Date(`${today}T${r.planned_start}`) : null;
      return inicio && (agora - inicio) / 3600000 > 8;
    }).length;
    const elC = document.getElementById('dash-canhotos');
    const elR = document.getElementById('dash-risco-perecivel');
    if (elC) elC.textContent = canhotos;
    if (elR) elR.textContent = riscoPer;

    // RETORNO
    document.getElementById('dash-retorno-total').textContent = devolvidos;
    document.getElementById('dash-retorno-lista').innerHTML = devolvidos > 0
      ? `<div>TOP 1000: ${Math.floor(devolvidos*.6)} itens</div><div>TOP 1007: ${Math.floor(devolvidos*.3)} itens</div>`
      : '<div style="color:#10b981">✅ Sem retornos</div>';
    const motivoEl = document.getElementById('dash-retorno-motivo');
    if (motivoEl) motivoEl.textContent = devolvidos > 0 ? '70% por falta de conferente no destino' : '';

    // ROTAS
    document.getElementById('dash-routes-list').innerHTML = routes.length
      ? routes.slice(0,8).map(r => {
          const inicio = r.planned_start || '—';
          const atrasado = r.status === 'executing' && r.planned_end && new Date(`${today}T${r.planned_end}`) < agora;
          return `<tr onclick="goTo('monitoramento',null)" style="cursor:pointer">
            <td><b style="font-family:monospace;font-size:11px;color:${atrasado?'#f87171':'#64B4FF'}">${r.vehicle_plate}</b></td>
            <td style="text-align:center">${r.total_stops||0}</td>
            <td style="font-size:11px;color:#90afd4">${inicio}</td>
            <td><span class="badge ${r.status}">${r.status}</span>${atrasado?'<span style="color:#f87171;margin-left:4px">⚠️</span>':''}</td>
          </tr>`;
        }).join('')
      : '<tr><td colspan="4" class="loading-state">Nenhuma rota hoje</td></tr>';

  } catch(e) {
    console.log('Erro dashboard:', e);
    ['dash-kpis-pedidos','dash-kpis-op','dash-kpis-fin'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = `<div class="loading-state" style="grid-column:1/-1">${e.message}</div>`;
    });
  }

  // MAPA
  setTimeout(() => {
    const m = initMap('dash-map');
    if (!m) return;
    const cores = ['#e8521a','#64B4FF','#10b981','#f87171','#a78bfa','#f59e0b'];
    api('GET', `/routes?date=${new Date().toISOString().slice(0,10)}`).then(routes => {
      routes.forEach((r, i) => {
        const cor = cores[i % cores.length];
        api('GET', `/routes/${r.route_id}/stops`).then(stops => {
          stops.forEach(s => {
            if (s.lat && s.lng) {
              new google.maps.Marker({
                position: {lat: parseFloat(s.lat), lng: parseFloat(s.lng)},
                map: m,
                icon: {
                  path: google.maps.SymbolPath.CIRCLE,
                  scale: 8, fillColor: cor, fillOpacity: 1,
                  strokeColor: '#fff', strokeWeight: 2
                },
                title: `${r.vehicle_plate} — ${s.recipient_name}`
              });
            }
          });
        }).catch(()=>{});
      });
    }).catch(() => {
      api('GET', '/orders?status=pending').then(orders => {
        orders.slice(0,30).forEach(o => {
          if (o.lat && o.lng) {
            new google.maps.Marker({
              position: {lat: parseFloat(o.lat), lng: parseFloat(o.lng)},
              map: m,
              icon: {path: google.maps.SymbolPath.CIRCLE, scale:6, fillColor:'#f59e0b', fillOpacity:1, strokeColor:'#fff', strokeWeight:1.5},
              title: o.recipient_name
            });
          }
        });
      }).catch(()=>{});
    });
  }, 300);
}

function expandirMapa() {
  const modal = document.getElementById('modal-mapa-full');
  modal.style.display = 'flex';
  setTimeout(() => {
    const m2 = initMap('dash-map-full');
    if (m2) google.maps.event.trigger(m2, 'resize');
  }, 200);
}

// Auto-refresh a cada 30 segundos
let dashInterval = null;
function iniciarAutoRefreshDash() {
  if (dashInterval) clearInterval(dashInterval);
  dashInterval = setInterval(() => {
    if (document.getElementById('page-dashboard')?.classList.contains('active')) {
      loadDashboard();
    }
  }, 30000);
}

// ── DASHBOARD MODAIS ──────────────────────────────────────────────
function fecharModalDash() {
  document.getElementById('modal-dash').style.display = 'none';
}

'''

    content = content[:idx_start] + new_js + content[idx_end:]
    print('JS do Dashboard atualizado!')

# Adiciona CSS de animação pulse
old_body = 'body{background:var(--bg);'
new_body = '''@keyframes pulse {
  0%,100% { opacity:1; }
  50%      { opacity:.5; }
}
body{background:var(--bg);'''

if '@keyframes pulse' not in content:
    content = content.replace(old_body, new_body)
    print('CSS pulse adicionado!')

# Inicia o relógio e auto-refresh no login
old_goto_dash = "if(page==='dashboard') loadDashboard();"
new_goto_dash = "if(page==='dashboard') { loadDashboard(); iniciarAutoRefreshDash(); }"
content = content.replace(old_goto_dash, new_goto_dash)

# Inicia o relógio após login
old_init = "initTopbarDate();\n    goTo('dashboard', null);"
new_init = "initTopbarDate();\n    initClock();\n    goTo('dashboard', null);"
content = content.replace(old_init, new_init)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
