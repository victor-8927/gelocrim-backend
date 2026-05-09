var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){};},SymbolPath:{CIRCLE:0},InfoWindow:function(){this.open=function(){};},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){}function alert(){}function confirm(){return true;}function parseInt(x){return x;}function parseFloat(x){return x;}

const API = 'http://localhost:8000/api/v1';
let token = localStorage.getItem('fleet_token') || '';
let currentUser = null;
let maps = {};
let ordersData = [];
let currentRouteId = null;
let ocorrencias = [];
var _editVeiculoId = null;
var _editMotoId = null;
window.rotSelecionados = {};
window._rotMapMarkers = [];
window._rotOrdersCache = [];

// ── AUTH ──
async function doLogin() {
  const btn = document.getElementById('btn-entrar');
  const err = document.getElementById('login-err');
  btn.disabled = true; btn.textContent = 'Entrando...'; err.textContent = '';
  try {
    const r = await fetch(`${API}/auth/login`, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({email: document.getElementById('login-email').value, password: document.getElementById('login-pass').value})
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Credenciais inválidas');
    token = d.access_token;
    localStorage.setItem('fleet_token', token);
    await loadMe();
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app').classList.add('show');
    initTopbarDate();
    initClock();
    goTo('dashboard', null);
  } catch(e) { err.textContent = e.message; }
  btn.disabled = false; btn.textContent = 'Entrar no Sistema';
}

document.getElementById('login-pass').addEventListener('keydown', e => { if(e.key==='Enter') doLogin(); });

async function loadMe() {
  const u = await api('GET', '/auth/me');
  currentUser = u;
  document.getElementById('topbar-username').textContent = u.name;
  document.getElementById('topbar-role').textContent = u.role;
  document.getElementById('topbar-avatar').textContent = u.name.charAt(0).toUpperCase();
}

function logout() {
  token = ''; localStorage.removeItem('fleet_token');
  document.getElementById('login-screen').style.display = 'flex';
  document.getElementById('app').classList.remove('show');
}

async function api(method, path, body) {
  const opts = {method, headers: {'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'}};
  if (body) opts.body = JSON.stringify(body);
  const r = await fetch(API + path, opts);
  if (r.status === 401) { logout(); throw new Error('Sessão expirada'); }
  if (!r.ok) { const d = await r.json().catch(()=>({detail:'Erro'})); throw new Error(d.detail || 'Erro na requisição'); }
  return r.json().catch(() => ({}));
}

function initTopbarDate() {
  const update = () => {
    const now = new Date();
    document.getElementById('topbar-date').textContent = now.toLocaleString('pt-BR', {day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'});
  };
  update(); setInterval(update, 60000);
}

// ── NAVIGATION ──
function goTo(page, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
  document.getElementById('page-' + page).classList.add('active');
  if (el) el.classList.add('active');
  else { const found = document.querySelector(`[data-page="${page}"]`); if(found) found.classList.add('active'); }
  const titles = {dashboard:'Painel Operacional',pedidos:'Gestão de Pedidos',roteirizacao:'Motor de Roteirização',rotas:'Gestão de Rotas',monitoramento:'Monitoramento',ocorrencias:'Ocorrências',veiculos:'Veículos',motoristas:'Motoristas',integracao:'Integração Sankhya',relatorios:'Relatórios'};
  document.getElementById('topbar-page-title').textContent = titles[page] || page;
  if(page==='dashboard') { loadDashboard(); iniciarAutoRefreshDash(); }
  if(page==='pedidos') loadOrders();
  if(page==='roteirizacao') { const today=new Date().toISOString().slice(0,10); document.getElementById('opt-date').value=today; loadRotMapData(); carregarFrota(); carregarVeiculosSelect(); }
  if(page==='rotas') loadRoutes();
  if(page==='monitoramento') { const today=new Date().toISOString().slice(0,10); document.getElementById('mon-date').value=today; loadTorreControle(); } if(page==='monitoramento_unused') loadMonitoring();
  if(page==='veiculos') loadVehicles();
  if(page==='motoristas') loadDrivers();
  if(page==='producao') { switchProducaoTab('pallet'); }
  if(page==='ocorrencias') loadOcorrencias();
  if(page==='relatorios') setRelPeriodo(30);
  if(page==='clientes') loadClientes();
}

// ── TOAST ──
function toast(msg, type='success') {
  const icons = {success:'✅',error:'❌',info:'ℹ️',warn:'⚠️'};
  const t = document.createElement('div');
  t.className = `toast-item ${type}`;
  t.innerHTML = `<span>${icons[type]||'📌'}</span> ${msg}`;
  document.getElementById('toast').appendChild(t);
  setTimeout(() => t.remove(), 4000);
}

function openModal(n) { document.getElementById('modal-'+n).classList.add('open'); }
function closeModal(n) { document.getElementById('modal-'+n).classList.remove('open'); }

// ── MAP HELPER (Google Maps) ──
function initMap(id, lat=-3.093544, lng=-60.075812, zoom=12) {
  if (maps[id]) return maps[id];
  const el = document.getElementById(id);
  if (!el) return null;
  const m = new google.maps.Map(el, {
    center: {lat, lng},
    zoom,
    mapTypeId: 'roadmap',
    gestureHandling: 'greedy',
    styles: [
      {featureType:'poi',elementType:'labels',stylers:[{visibility:'off'}]},
      {featureType:'transit',stylers:[{visibility:'off'}]}
    ]
  });
  // Marcador do depósito
  new google.maps.Marker({
    position: {lat, lng},
    map: m,
    title: 'Depósito Gelocrim',
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: '#e8521a',
      fillOpacity: 1,
      strokeColor: '#fff',
      strokeWeight: 2
    }
  });
  maps[id] = m;
  return m;
}

function addMarker(map, lat, lng, color, title, info) {
  const marker = new google.maps.Marker({
    position: {lat, lng},
    map,
    title,
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 8,
      fillColor: color,
      fillOpacity: 1,
      strokeColor: '#fff',
      strokeWeight: 2
    }
  });
  if (info) {
    const iw = new google.maps.InfoWindow({content: info});
    marker.addListener('click', () => iw.open(map, marker));
  }
  return marker;
}

async function drawRoute(map, stops, color) {
  if (!stops || stops.length < 1) return;
  await desenharRotaReal(map, stops, color);
}

// ── DASHBOARD ──

// ── DASHBOARD ────────────────────────────────────────────────────

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

// ── PEDIDOS AVANÇADO ──────────────────────────────────────────────
let _ordersSelected = new Set();

function toggleTodosOrders(checked) {
  _ordersSelected.clear();
  if (checked) {
    document.querySelectorAll('.order-chk').forEach(chk => {
      chk.checked = true;
      _ordersSelected.add(chk.dataset.id);
    });
  } else {
    document.querySelectorAll('.order-chk').forEach(chk => chk.checked = false);
  }
  atualizarAcoesLote();
}

function toggleOrderChk(id, checked) {
  if (checked) _ordersSelected.add(id);
  else _ordersSelected.delete(id);
  atualizarAcoesLote();
}

function atualizarAcoesLote() {
  const lote = document.getElementById('orders-acoes-lote');
  const sel  = document.getElementById('orders-selecionados');
  if (_ordersSelected.size > 0) {
    lote.style.display = 'flex';
    sel.textContent = `${_ordersSelected.size} pedido(s) selecionado(s)`;
  } else {
    lote.style.display = 'none';
  }
}


function alterarPrioridadeLote(prio) {
  if (_ordersSelected.size === 0) return;
  const label = {2:'Alta',3:'Urgente'}[prio];
  toast(`Prioridade ${label} aplicada a ${_ordersSelected.size} pedido(s)`, 'success');
  // Aplica localmente na tabela
  _ordersSelected.forEach(id => {
    const row = document.querySelector(`[data-id="${id}"]`)?.closest('tr');
    if (row) {
      const badge = row.querySelector('.badge.draft, .badge.pending, .badge.failed');
      if (badge) { badge.className = `badge ${prio===3?'failed':'pending'}`; badge.textContent = label; }
    }
  });
}

function cancelarAlocacaoLote() {
  if (_ordersSelected.size === 0) return;
  if (!confirm(`Cancelar alocação de ${_ordersSelected.size} pedido(s)?`)) return;
  toast(`${_ordersSelected.size} pedido(s) com alocação cancelada`, 'info');
  limparSelecaoOrders();
}

function limparSelecaoOrders() {
  _ordersSelected.clear();
  document.querySelectorAll('.order-chk').forEach(c => c.checked = false);
  document.getElementById('chk-all').checked = false;
  atualizarAcoesLote();
}

function adicionarSelecionadosRota() {
  if (_ordersSelected.size === 0) return;
  toast(`${_ordersSelected.size} pedido(s) marcado(s) para roteirização`, 'success');
  goTo('roteirizacao', null);
}

async function verDetalhePedido(id) {
  const modal = document.getElementById('modal-pedido-detalhe');
  modal.style.display = 'flex';
  const body = document.getElementById('modal-ped-body');
  body.innerHTML = '<div class="loading-state">Carregando...</div>';
  try {
    const orders = ordersData || [];
    const o = orders.find(x => x.id === id);
    if (!o) { body.innerHTML = '<div class="loading-state">Pedido não encontrado</div>'; return; }
    document.getElementById('modal-ped-titulo').textContent = `Pedido ${o.external_id||o.id.slice(0,8)}`;
    body.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
        <div>
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Cliente</div>
          <div style="font-size:16px;font-weight:700;color:#e8f0fe">${o.recipient_name}</div>
          <div style="font-size:12px;color:#90afd4;margin-top:4px">${o.address||'—'}</div>
        </div>
        <div>
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Identificação</div>
          <div style="font-family:monospace;font-size:14px;color:#64B4FF">${o.external_id||'—'}</div>
          <div style="font-size:12px;color:#90afd4;margin-top:4px">Status: <span class="badge ${o.status}">${o.status}</span></div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px">
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#90afd4;margin-bottom:4px">Peso Total</div>
          <div style="font-size:20px;font-weight:700;color:#a78bfa">${o.weight_kg||0} kg</div>
        </div>
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#90afd4;margin-bottom:4px">Volume</div>
          <div style="font-size:20px;font-weight:700;color:#2dd4bf">${o.volume_m3||0} m³</div>
        </div>
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#90afd4;margin-bottom:4px">Janela Entrega</div>
          <div style="font-size:14px;font-weight:700;color:#f59e0b">${o.time_window_start||'—'} - ${o.time_window_end||'—'}</div>
        </div>
      </div>
      <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:14px;margin-bottom:12px">
        <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;font-weight:700">Detalhamento por TOP</div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px">
          ${['1000','1007','1008','1009','1010'].map(top=>`
          <div style="text-align:center;padding:8px;background:#061020;border-radius:6px">
            <div style="font-size:10px;color:#90afd4">TOP ${top}</div>
            <div style="font-size:16px;font-weight:700;color:#64B4FF;margin:4px 0">—</div>
            <div style="font-size:10px;color:#90afd4">kg</div>
          </div>`).join('')}
        </div>
        <div style="font-size:11px;color:#90afd4;margin-top:8px">* Detalhamento por TOP será disponível com integração Sankhya</div>
      </div>
      <div style="display:flex;gap:8px;justify-content:flex-end">
        <button class="btn btn-secondary" onclick="document.getElementById('modal-pedido-detalhe').style.display='none'">Fechar</button>
        <button class="btn btn-primary" onclick="document.getElementById('modal-pedido-detalhe').style.display='none';goTo('roteirizacao',null)">➕ Roteirizar</button>
      </div>`;
  } catch(e) { body.innerHTML = `<div class="loading-state">${e.message}</div>`; }
}

async function sincronizarSankhya() {
  const btn = event.target;
  btn.disabled = true;
  btn.textContent = '⏳ Sincronizando...';
  try {
    await api('POST', '/integration/sync');
    toast('Sincronização com Sankhya realizada!', 'success');
    loadOrders();
  } catch(e) {
    toast('Integração Sankhya pendente de configuração', 'info');
  } finally {
    btn.disabled = false;
    btn.textContent = '🔄 Sincronizar Sankhya';
  }
}


// ── CONFERÊNCIA MASTER ────────────────────────────────────────────
let confMap = null;
let confOrdem = [];

function abrirConferenciaMaster() {
  const itens = Object.values(rotSelecionados || {});
  if (itens.length === 0) { toast('Selecione clientes no mapa primeiro', 'error'); return; }

  const selecionados = itens.map(x => x.order);

  // Veículo
  const veicSelect = document.getElementById('rot-veiculo-select');
  const motSelect  = document.getElementById('sel-motorista');
  const aj1Select  = document.getElementById('sel-ajudante1');
  const aj2Select  = document.getElementById('sel-ajudante2');

  if (!veicSelect?.value) { toast('Selecione um veículo antes de roteirizar', 'error'); return; }

  const veicOpt  = veicSelect.options[veicSelect.selectedIndex];
  const veicNome = veicOpt?.text || '—';
  const capKg    = parseFloat(veicOpt?.dataset?.kg || 5000);
  const capM3    = parseFloat(veicOpt?.dataset?.m3 || 20);

  const motNome  = motSelect?.options[motSelect?.selectedIndex]?.text || '—';
  const aj1Nome  = aj1Select?.value ? aj1Select.options[aj1Select.selectedIndex].text : null;
  const aj2Nome  = aj2Select?.value ? aj2Select.options[aj2Select.selectedIndex].text : null;
  const equipeStr = [motNome, aj1Nome, aj2Nome].filter(Boolean).join(' · ');

  // Totais reais dos pedidos
  const pesoTotal = selecionados.reduce((s,o) => s + (parseFloat(o.weight_kg)||0), 0);
  const volTotal  = selecionados.reduce((s,o) => s + (parseFloat(o.volume_m3) || (parseFloat(o.weight_kg)||0)*0.002), 0);
  const fatTotal  = selecionados.reduce((s,o) => s + (parseFloat(o.total_value)||parseFloat(o.value)||0), 0);

  // Distância estimada (3km entre paradas + 15km depósito/retorno)
  const kmEst = 15 + selecionados.length * 3;

  // Custos — virão do cadastro futuramente
  const custoDia   = 0; // a configurar no cadastro de motoristas
  const custoDiesel= 0; // a configurar no cadastro de veículos
  const custoManut = 0; // a configurar no cadastro de veículos
  const custoTotal = custoDia + custoDiesel + custoManut;

  // Margem
  const lucro  = fatTotal - custoTotal;
  const margem = fatTotal > 0 ? (lucro / fatTotal * 100) : 0;

  // Previsão de fim
  const minTotal = selecionados.length * 20 + Math.round(kmEst / 40 * 60);
  const horaInicio = document.getElementById('conf-hora-inicio')?.value || '07:30';
  const [h, m] = horaInicio.split(':').map(Number);
  const fimMin = h*60 + m + minTotal;
  const fimH = Math.floor(fimMin/60).toString().padStart(2,'0');
  const fimM = Math.floor(fimMin%60).toString().padStart(2,'0');

  // Abre o painel
  // Reset fluxo
  rotaConfirmada = false;
  const bG = document.getElementById('btn-gravar-carga');
  const bC = document.getElementById('btn-confirmar-rota');
  const bA = document.getElementById('btn-atualizar-rota');
  if (bG) { bG.disabled=true; bG.style.background='#1e3a5c'; bG.style.color='#90afd4'; bG.style.cursor='not-allowed'; bG.style.opacity='0.5'; bG.textContent='💾 GRAVAR CARGA'; }
  if (bC) { bC.disabled=true; bC.style.background='#1e3a5c'; bC.style.color='#90afd4'; bC.style.cursor='not-allowed'; bC.style.opacity='0.5'; bC.textContent='✅ Confirmar Rota'; }
  if (bA) { bA.disabled=false; bA.style.opacity='1'; }
  const lista = document.getElementById('conf-lista-clientes');
  if (lista) lista.style.opacity='1';
  document.getElementById('painel-conferencia').style.display = 'flex';
  if (!document.getElementById('conf-data-saida').value)
    document.getElementById('conf-data-saida').value = new Date().toISOString().slice(0,10);

  const el = (id, val) => { const e = document.getElementById(id); if(e) e.textContent = val; };

  el('conf-subtitulo',  `${selecionados.length} clientes · ${pesoTotal.toFixed(0)}kg · ${motNome}`);
  el('conf-veiculo',    veicNome);
  el('conf-motorista',  equipeStr);
  el('conf-capacidade', capKg.toLocaleString('pt-BR') + ' kg / ' + capM3 + ' m³');
  el('conf-peso',       pesoTotal.toFixed(1) + ' kg (' + Math.round(pesoTotal/capKg*100) + '% cap.)');
  el('conf-entregas',   selecionados.length + ' paradas · ' + selecionados.filter(o=>o.lat&&o.lng).length + ' com GPS');
  el('conf-distancia',  kmEst + ' km estimados');
  el('conf-hora-fim',   fimH + ':' + fimM);

  // Financeiro
  if (fatTotal > 0) {
    el('conf-top1000', 'R$ ' + fatTotal.toFixed(2));
    el('conf-top1009', '—');
    el('conf-top1007', '—');
    el('conf-top1010', '—');
    el('conf-top1008', '—');
    el('conf-total-pedidos', 'R$ ' + fatTotal.toFixed(2));
  } else {
    el('conf-top1000', 'Integrar Sankhya');
    el('conf-top1009', '—'); el('conf-top1007', '—');
    el('conf-top1010', '—'); el('conf-top1008', '—');
    el('conf-total-pedidos', '⚠️ Sem valor cadastrado');
  }

  el('conf-custo-equipe', custoDia > 0 ? 'R$ '+custoDia.toFixed(2) : '⚙️ Configurar no cadastro');
  el('conf-custo-diesel',  custoDiesel > 0 ? 'R$ '+custoDiesel.toFixed(2) : '⚙️ Configurar no veículo');
  el('conf-custo-manut',   custoManut > 0 ? 'R$ '+custoManut.toFixed(2) : '⚙️ Configurar no veículo');
  el('conf-custo-total',   custoTotal > 0 ? 'R$ '+custoTotal.toFixed(2) : '⚙️ Preencher cadastros');

  // Semáforo
  const emoji = fatTotal === 0 ? '⚠️' : margem >= 20 ? '🟢' : margem >= 10 ? '🟡' : '🔴';
  const cor   = fatTotal === 0 ? '#f59e0b' : margem >= 20 ? '#10b981' : margem >= 10 ? '#f59e0b' : '#f87171';
  const bg    = fatTotal === 0 ? 'rgba(245,158,11,.15)' : margem >= 20 ? 'rgba(16,185,129,.15)' : margem >= 10 ? 'rgba(245,158,11,.15)' : 'rgba(248,113,113,.15)';
  el('conf-semaforo-emoji', emoji);
  el('conf-margem-valor', fatTotal > 0 ? margem.toFixed(1)+'%' : '—');
  el('conf-margem-label', fatTotal > 0 ? 'Margem Operacional' : 'Complete os cadastros para calcular');
  const sem = document.getElementById('conf-semaforo');
  if (sem) { sem.style.background = bg; sem.style.borderColor = cor; }
  const mv = document.getElementById('conf-margem-valor');
  if (mv) mv.style.color = cor;

  // Lista drag & drop
  confOrdem = [...selecionados];
  renderizarListaConf();

  // Mapa de verificação com Google Maps
  setTimeout(() => {
    // Limpa marcadores e polyline anteriores
    if (confMap && confMap._confMarkers) {
      confMap._confMarkers.forEach(m => m.setMap(null));
      confMap._confMarkers = [];
    }
    if (confMap && confMap._confLine) {
      confMap._confLine.setMap(null);
      confMap._confLine = null;
    }

    // Inicializa ou reutiliza o mapa
    if (!confMap) {
      confMap = initMap('conf-mapa', -3.093544, -60.075812, 12);
    }
    if (!confMap) return;
    confMap._confMarkers = [];

    const bounds = new google.maps.LatLngBounds();
    const coords = [];

    // Marcador do depósito
    const deposito = {lat: -3.093544, lng: -60.075812};
    const mDep = new google.maps.Marker({
      position: deposito,
      map: confMap,
      label: { text: '🏭', fontSize: '16px' },
      title: 'Depósito Gelocrim'
    });
    confMap._confMarkers.push(mDep);
    bounds.extend(deposito);
    coords.push(deposito);

    // Marcadores dos clientes
    confOrdem.forEach((o, i) => {
      const lat = parseFloat(o.lat);
      const lng = parseFloat(o.lng);
      if (!isNaN(lat) && !isNaN(lng) && Math.abs(lat) > 0.01) {
        const pos = {lat, lng};
        coords.push(pos);
        bounds.extend(pos);
        const marker = new google.maps.Marker({
          position: pos,
          map: confMap,
          label: {
            text: String(i+1),
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '11px'
          },
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 14,
            fillColor: '#e8521a',
            fillOpacity: 1,
            strokeColor: '#fff',
            strokeWeight: 2
          },
          title: o.recipient_name
        });
        const infoContent = `<div style="font-family:Arial,sans-serif;padding:4px;min-width:180px"><b style="font-size:13px">${i+1}. ${o.recipient_name}</b><br><span style="font-size:11px;color:#555">📍 ${o.address||'—'}</span><br><span style="font-size:11px">⚖️ ${o.weight_kg||0}kg &nbsp; 📦 ${o.volume_m3||0}m³</span><br><span style="font-size:11px">🕐 ${o.time_window_start||'—'} - ${o.time_window_end||'—'}</span><br><span style="font-size:10px;color:#888">Pedido: ${o.external_id||'—'}</span></div>`;
        const info = new google.maps.InfoWindow({ content: infoContent });
        marker.addListener('click', () => info.open(confMap, marker));
      }
    });


    // Fecha no depósito
    coords.push(deposito);

    // Trajeto real pelas ruas usando Directions API
    if (coords.length >= 2) {
      const directionsService  = new google.maps.DirectionsService();
      const directionsRenderer = new google.maps.DirectionsRenderer({
        map: confMap,
        suppressMarkers: true, // usa nossos marcadores numerados
        polylineOptions: {
          strokeColor: '#64B4FF',
          strokeOpacity: 0.85,
          strokeWeight: 4
        }
      });
      confMap._confLine = directionsRenderer;

      // Monta waypoints (paradas intermediárias — máx 25 no Google)
      const origem  = coords[0]; // depósito
      const destino = coords[coords.length - 1]; // volta ao depósito
      const waypoints = coords.slice(1, coords.length - 1).slice(0, 23).map(c => ({
        location: new google.maps.LatLng(c.lat, c.lng),
        stopover: true
      }));

      directionsService.route({
        origin:      new google.maps.LatLng(origem.lat, origem.lng),
        destination: new google.maps.LatLng(destino.lat, destino.lng),
        waypoints:   waypoints,
        travelMode:  google.maps.TravelMode.DRIVING,
        optimizeWaypoints: false // mantém a ordem do analista
      }, (result, status) => {
        if (status === 'OK') {
          directionsRenderer.setDirections(result);
          // Calcula distância real total
          let kmReal = 0;
          result.routes[0].legs.forEach(leg => {
            kmReal += leg.distance.value / 1000;
          });
          const el = document.getElementById('conf-distancia');
          if (el) el.textContent = kmReal.toFixed(1) + ' km (real)';
        } else {
          // Fallback: linha reta se Directions falhar
          confMap._confLine = new google.maps.Polyline({
            path: coords, geodesic: true,
            strokeColor: '#64B4FF', strokeOpacity: 0.7, strokeWeight: 3,
            map: confMap
          });
          confMap.fitBounds(bounds);
        }
      });

      confMap.fitBounds(bounds);
    }

    // Força resize do mapa
    google.maps.event.trigger(confMap, 'resize');
    if (!bounds.isEmpty()) confMap.fitBounds(bounds);
  }, 500);
}


// ── CONFERÊNCIA MASTER — MELHORIAS ───────────────────────────────
let trafegoAtivo = false;
let trafegoLayer = null;

function toggleTrafegoMapa() {
  if (!confMap) return;
  if (trafegoAtivo) {
    if (trafegoLayer) trafegoLayer.setMap(null);
    trafegoAtivo = false;
    toast('Camada de tráfego removida', 'info');
  } else {
    trafegoLayer = new google.maps.TrafficLayer();
    trafegoLayer.setMap(confMap);
    trafegoAtivo = true;
    toast('Tráfego em tempo real ativado!', 'success');
  }
}

function atualizarBarrasCapacidade(pesoTotal, capKg, volTotal, capM3) {
  const pctPeso    = capKg  > 0 ? Math.min(100, Math.round(pesoTotal/capKg*100))  : 0;
  const pctVol     = capM3  > 0 ? Math.min(100, Math.round(volTotal/capM3*100))   : 0;
  const pctPallets = 0; // virá do cadastro de pallets

  const barPeso = document.getElementById('conf-bar-peso');
  const barVol  = document.getElementById('conf-bar-vol');
  if (barPeso) {
    barPeso.style.width = pctPeso+'%';
    barPeso.style.background = pctPeso>90?'#f87171':pctPeso>70?'#f59e0b':'#10b981';
  }
  if (barVol) {
    barVol.style.width = pctVol+'%';
    barVol.style.background = pctVol>90?'#f87171':pctVol>70?'#f59e0b':'#2dd4bf';
  }
  const elPeso = document.getElementById('conf-peso');
  const elVol  = document.getElementById('conf-volume');
  if (elPeso) elPeso.textContent = `${pesoTotal.toFixed(0)}kg (${pctPeso}% cap.)`;
  if (elVol)  elVol.textContent  = `${volTotal.toFixed(2)}m³ (${pctVol}% cap.)`;
}

function atualizarBarrasTOP(fatTotal) {
  if (fatTotal <= 0) return;
  const tops = [
    {id:'1000', pct:80, el:'conf-bar-top1000'},
    {id:'1009', pct:8,  el:'conf-bar-top1009'},
    {id:'1007', pct:6,  el:'conf-bar-top1007'},
    {id:'1010', pct:4,  el:'conf-bar-top1010'},
  ];
  tops.forEach(t => {
    const bar = document.getElementById(t.el);
    if (bar) bar.style.width = t.pct+'%';
  });
}

function verificarMargemNegativa(margem) {
  const alerta = document.getElementById('conf-alerta-margem');
  const btnGravar = document.getElementById('btn-gravar-carga');
  if (margem < 0) {
    if (alerta) alerta.style.display = 'block';
    if (btnGravar) { btnGravar.style.background = '#f87171'; btnGravar.textContent = '⚠️ GRAVAR COM MARGEM NEGATIVA'; }
  } else {
    if (alerta) alerta.style.display = 'none';
    if (btnGravar) { btnGravar.style.background = '#10b981'; btnGravar.textContent = '💾 GRAVAR CARGA'; }
  }
}

function verificarCamposObrigatorios() {
  const veiculo   = document.getElementById('rot-veiculo-select')?.value;
  const motorista = document.getElementById('sel-motorista')?.value;
  const btn = document.getElementById('btn-gravar-carga');
  if (!veiculo || !motorista) {
    if (btn) { btn.disabled = true; btn.style.opacity = '0.5'; btn.title = 'Preencha veículo e motorista'; }
    return false;
  }
  if (btn) { btn.disabled = false; btn.style.opacity = '1'; btn.title = ''; }
  return true;
}

function gerarRomaneio() {
  if (confOrdem.length === 0) { toast('Nenhum cliente na carga!', 'error'); return; }
  const veicEl = document.getElementById('rot-veiculo-select');
  const motEl  = document.getElementById('sel-motorista');
  const veiculo  = veicEl?.options[veicEl?.selectedIndex]?.text || '—';
  const motorista= motEl?.options[motEl?.selectedIndex]?.text  || '—';
  const data     = document.getElementById('conf-data-saida')?.value || '—';
  const inicio   = document.getElementById('conf-hora-inicio')?.value || '—';
  const fim      = document.getElementById('conf-hora-fim')?.textContent || '—';

  const linhas = confOrdem.map((o,i) => `
    <tr style="border-bottom:1px solid #ddd">
      <td style="padding:6px;text-align:center;font-weight:bold">${i+1}</td>
      <td style="padding:6px">${o.external_id||'—'}</td>
      <td style="padding:6px">${o.recipient_name}</td>
      <td style="padding:6px">${o.address||'—'}</td>
      <td style="padding:6px;text-align:center">${o.weight_kg||0} kg</td>
      <td style="padding:6px;text-align:center">___________</td>
    </tr>`).join('');

  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8">
    <title>Romaneio — ${veiculo}</title>
    <style>body{font-family:Arial,sans-serif;font-size:12px;margin:20px}
    h1{font-size:16px;text-align:center}
    .header{display:flex;justify-content:space-between;margin-bottom:16px;padding:10px;border:1px solid #ccc;border-radius:4px}
    table{width:100%;border-collapse:collapse}
    th{background:#0a1628;color:#fff;padding:8px;text-align:left}
    </style>
</head><body>
    <h1>🧊 GELOCRIM — Romaneio de Entrega</h1>
    <div class="header">
      <div><b>Veículo:</b> ${veiculo}<br><b>Motorista:</b> ${motorista}</div>
      <div><b>Data:</b> ${data}<br><b>Saída:</b> ${inicio} | <b>Previsão fim:</b> ${fim}</div>
      <div><b>Total paradas:</b> ${confOrdem.length}<br><b>Gerado em:</b> ${new Date().toLocaleString('pt-BR')}</div>
    </div>
    <table><thead><tr><th>#</th><th>Pedido</th><th>Cliente</th><th>Endereço</th><th>Peso</th><th>Assinatura</th></tr></thead>
    <tbody>${linhas}</tbody></table>
    <div style="margin-top:40px;display:flex;justify-content:space-around">
      <div style="text-align:center">___________________<br>Motorista</div>
      <div style="text-align:center">___________________<br>Conferente</div>
      <div style="text-align:center">___________________<br>Supervisor</div>
    </div>
  `;
  const w = window.open('','_blank');
  if(w){w.document.write(html);w.document.close();}
}

// ── ROTEIRIZAÇÃO LOAD ────────────────────────────────────────────
async function loadRotMapData(){
  var statusEl=document.getElementById('rot-map-status');
  if(statusEl) statusEl.textContent='Carregando clientes...';
  console.log('loadRotMapData iniciado!');
  try{
    // Carrega pedidos pendentes E clientes
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
    console.log('Clientes com pedidos e GPS:', items.length);

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

// ── VEÍCULOS EDIÇÃO ──────────────────────────────────────────────
async function editarVeiculo(id){
  window.veiculoEditId = id;
  console.log('editarVeiculo chamado com id:', id);
  try{
    var data = await api('GET','/vehicles');
    var v = data.find(function(x){return x.id===id;});
    if(!v){ toast('Veículo não encontrado!','error'); return; }
    var modal = document.getElementById('modal-veiculo-completo');
    if(!modal){ toast('Modal não encontrado!','error'); return; }
    modal.style.display='flex';
    setTimeout(function(){
      function setV(eid,val){ var e=document.getElementById(eid); if(e&&val!=null&&val!==undefined&&val!=='') e.value=val; }
      setV('v-vda',v.vda); setV('v-plate',v.plate); setV('v-model',v.model);
      setV('v-type',v.type); setV('v-kg',v.capacity_kg); setV('v-m3',v.capacity_m3);
      setV('v-pallets',v.pallets); setV('v-comp',v.bau_comp); setV('v-larg',v.bau_larg);
      setV('v-alt',v.bau_alt); setV('v-combustivel',v.fuel_type||'diesel');
      setV('v-kml',v.km_per_liter); setV('v-preco-comb',v.fuel_price);
      setV('v-ipva',v.ipva_anual); setV('v-manut',v.manut_mes);
      setV('v-custo-dia',v.daily_cost); setV('v-status',v.status||'active');
      var h=document.getElementById('v-edit-id'); if(h) h.value=id;
      var t=document.getElementById('modal-veic-titulo'); if(t) t.textContent='Editar — '+(v.vda||v.plate);
      console.log('Campos preenchidos, v-edit-id:', document.getElementById('v-edit-id')?.value);
    },200);
  }catch(e){ toast('Erro: '+e.message,'error'); }
}

async function salvarVeiculoCompleto(editId){
  var h = document.getElementById('v-edit-id');
  editId = editId || (h?h.value:null) || window.veiculoEditId || null;
  console.log('Salvando veiculo, editId:', editId);
  var body={
    vda:document.getElementById('v-vda').value,
    plate:document.getElementById('v-plate').value,
    model:document.getElementById('v-model').value,
    type:document.getElementById('v-type').value,
    capacity_kg:parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:parseFloat(document.getElementById('v-m3').value)||0,
    pallets:parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:document.getElementById('v-combustivel').value,
    km_per_liter:parseFloat(document.getElementById('v-kml').value)||0,
    fuel_price:parseFloat(document.getElementById('v-preco-comb').value)||0,
    ipva_anual:parseFloat(document.getElementById('v-ipva').value)||0,
    manut_mes:parseFloat(document.getElementById('v-manut').value)||0,
    daily_cost:parseFloat(document.getElementById('v-custo-dia').value)||0,
    status:document.getElementById('v-status').value,
  };
  if(!body.plate||!body.model){toast('Placa e modelo obrigatórios!','error');return;}
  try{
    if(editId){
      await api('PATCH','/vehicles/'+editId,body);
      toast('Veículo atualizado!','success');
    } else {
      await api('POST','/vehicles',body);
      toast('Veículo cadastrado!','success');
    }
    window.veiculoEditId=null;
    if(h) h.value='';
    document.getElementById('modal-veiculo-completo').style.display='none';
    loadVehicles();
  }catch(e){toast('Erro: '+e.message,'error');}
}

// ── ROTEIRIZAÇÃO ─────────────────────────────────────────────────
var COR_ROTAS={'801':'#e8521a','802':'#64B4FF','803':'#10b981','804':'#f59e0b','805':'#a78bfa','811':'#f87171','822':'#2dd4bf'};
var _rotMapMarkers=[];
var _rotOrdersCache=[];











// ── ROTEIRIZAÇÃO VISUAL ───────────────────────────────────────────
var COR_ROTAS = {'801':'#FF6B35','802':'#4FC3F7','803':'#66BB6A','804':'#FFA726','805':'#AB47BC','811':'#EF5350','821':'#26C6DA','822':'#26C6DA'};

function getCorRota(val){
  if(!val) return '#90afd4';
  for(var k in COR_ROTAS){ if(val.toString().indexOf(k)>=0) return COR_ROTAS[k]; }
  return '#90afd4';
}

function filtrarRotMapa(){
  var cache = window._rotOrdersCache||[];
  if(!cache.length){ toast('Clique em Atualizar primeiro!','warn'); return; }
  renderRotMapMarkers(cache);
}

function buscarFiltrados(){
  var cache = window._rotOrdersCache||[];
  var fr  = document.getElementById('rot-filtro-rota');
  var freg= document.getElementById('rot-filtro-regiao');
  var fb  = document.getElementById('rot-filtro-bairro');
  var fs  = document.getElementById('rot-filtro-busca');
  var vr  = fr  ? fr.value  : '';
  var vreg= freg? freg.value: '';
  var vb  = fb  ? fb.value  : '';
  var vs  = fs  ? fs.value.toLowerCase() : '';
  if(!vr&&!vreg&&!vb&&!vs){ toast('Selecione ao menos um filtro!','warn'); return; }
  var candidatos = cache.filter(function(o){
    if(!o.lat||!o.lng) return false;
    if(vr   && (o.rota||o.regiao||'').indexOf(vr)<0)   return false;
    if(vreg && (o.regiao||'').indexOf(vreg)<0)          return false;
    if(vb   && (o.bairro||'').toLowerCase().indexOf(vb.toLowerCase())<0) return false;
    if(vs   && (o.recipient_name||'').toLowerCase().indexOf(vs)<0) return false;
    return true;
  });
  var novos=0;
  candidatos.forEach(function(o){
    if(!window.rotSelecionados[o.id]){ window.rotSelecionados[o.id]={order:o,marker:null}; novos++; }
  });
  renderRotMapMarkers(cache);
  atualizarSelecaoRot();
  toast(novos+' clientes selecionados!','success');
}

function renderRotMapMarkers(orders){
  setTimeout(function(){
    var m = initMap('rot-map');
    if(!m) return;
    (window._rotMapMarkers||[]).forEach(function(mk){ mk.setMap(null); });
    window._rotMapMarkers = [];

    var fr  = document.getElementById('rot-filtro-rota');
    var freg= document.getElementById('rot-filtro-regiao');
    var fb  = document.getElementById('rot-filtro-bairro');
    var fs  = document.getElementById('rot-filtro-busca');
    var vr  = fr  ? fr.value  : '';
    var vreg= freg? freg.value: '';
    var vb  = fb  ? fb.value  : '';
    var vs  = fs  ? fs.value.toLowerCase() : '';

    var filtrados = (orders||[]).filter(function(o){
      if(!o.lat||!o.lng) return false;
      if(vr   && (o.rota||o.regiao||'').indexOf(vr)<0)   return false;
      if(vreg && (o.regiao||'').indexOf(vreg)<0)          return false;
      if(vb   && (o.bairro||'').toLowerCase().indexOf(vb.toLowerCase())<0) return false;
      if(vs   && (o.recipient_name||'').toLowerCase().indexOf(vs)<0) return false;
      return true;
    });

    var st = document.getElementById('rot-map-status');
    if(st) st.textContent = filtrados.length+' clientes no mapa';

    var bounds = new google.maps.LatLngBounds();
    var openIW = null; // InfoWindow atualmente aberto
    var fixedIW = null; // InfoWindow fixo (duplo clique)

    filtrados.forEach(function(o){
      var sel = !!window.rotSelecionados[o.id];
      var cor = sel ? '#10b981' : getCorRota(o.rota||o.regiao);
      var nPedidos = (o.pedidos||[]).length;
      var tempoMin = parseInt(o.tempo_entrega)||0;

      var mk = new google.maps.Marker({
        position: {lat:parseFloat(o.lat), lng:parseFloat(o.lng)},
        map: m,
        title: (o.recipient_name||'')+'|'+(o.rota||o.regiao||''),
        animation: sel ? google.maps.Animation.BOUNCE : null,
        icon: {
          path: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',
          fillColor: cor,
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 1,
          scale: sel ? 2.2 : 1.7,
          anchor: new google.maps.Point(12, 22),
          rotation: 0
        }
      });

      if(sel) setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);

      var iwContent =
        '<div style="font-family:Arial;font-size:12px;padding:8px;min-width:210px;max-width:260px">'+
        '<b style="font-size:14px;color:#1a3a5c">'+(o.recipient_name||'—')+'</b><br>'+
        '<span style="color:#e8521a;font-weight:700;font-size:12px">🗺️ Rota '+(o.rota||o.regiao||'—')+'</span><br>'+
        (o.bairro?'<span style="color:#555">🏘️ '+o.bairro+'</span><br>':'')+
        '<span style="color:#555">📦 '+nPedidos+' pedido(s) | '+(o.weight_kg||0).toFixed(0)+' kg total</span><br>'+
        '<span style="color:#555">⏱️ Tempo médio: '+(tempoMin>0?tempoMin+' min':'—')+'</span>'+
        '</div>';

      var iw = new google.maps.InfoWindow({content: iwContent});

      // 1 clique: seleciona + mostra InfoWindow temporário
      mk.addListener('click', function(){
        if(window.rotSelecionados[o.id]){
          delete window.rotSelecionados[o.id];
          mk.setAnimation(null);
          mk.setIcon({path:'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',fillColor:getCorRota(o.rota||o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:1,scale:1.7,anchor:new google.maps.Point(12,22)});
        } else {
          window.rotSelecionados[o.id] = {order:o, marker:mk};
          mk.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);
          mk.setIcon({path:'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:1,scale:2.2,anchor:new google.maps.Point(12,22)});
        }
        // Fecha InfoWindow anterior temporário
        if(openIW && openIW !== fixedIW) openIW.close();
        iw.open(m, mk);
        openIW = iw;
        // Fecha automaticamente após 3s (a menos que seja fixo)
        setTimeout(function(){
          if(openIW === iw && fixedIW !== iw) { iw.close(); openIW = null; }
        }, 3000);
        atualizarSelecaoRot();
      });

      // 2 cliques: fixa o InfoWindow
      mk.addListener('dblclick', function(){
        if(fixedIW) fixedIW.close();
        iw.open(m, mk);
        fixedIW = iw;
        openIW = iw;
      });

      window._rotMapMarkers.push(mk);
      bounds.extend({lat:parseFloat(o.lat), lng:parseFloat(o.lng)});
    });

    if(filtrados.length > 0 && !bounds.isEmpty()) m.fitBounds(bounds);
  }, 200);
}
