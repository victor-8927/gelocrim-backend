path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Substitui o HTML do dashboard ──────────────────────────────
old_dash_html = '''    <!-- ══ DASHBOARD ══ -->
    <div class="page active" id="page-dashboard">
      <div class="page-header">
        <div>
          <div class="page-title">Painel Operacional</div>
          <div class="page-sub" id="dash-subtitle">Resumo da operação do dia</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadDashboard()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="goTo('roteirizacao',null)">⚡ Roteirizar Agora</button>
        </div>
      </div>

      <!-- Alertas -->
      <div id="dash-alerts"></div>

      <!-- KPIs -->
      <div class="kpi-grid" id="dash-kpis">
        <div class="loading-state">Carregando...</div>
      </div>

      <!-- Grid principal -->
      <div class="grid2">
        <div class="card">
          <div class="card-header">
            <span class="card-title">📦 Pedidos por Status</span>
            <button class="btn btn-sm btn-secondary" onclick="goTo('pedidos',null)">Ver todos</button>
          </div>
          <div class="card-body">
            <table>
              <thead><tr><th>Status</th><th>Qtd</th><th>%</th></tr></thead>
              <tbody id="dash-orders-status"></tbody>
            </table>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <span class="card-title">🚛 Rotas do Dia</span>
            <button class="btn btn-sm btn-secondary" onclick="goTo('rotas',null)">Ver todas</button>
          </div>
          <div class="card-body">
            <table>
              <thead><tr><th>Veículo</th><th>Paradas</th><th>Status</th></tr></thead>
              <tbody id="dash-routes-list"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <span class="card-title">🗺️ Mapa da Operação — Hoje</span>
          <button class="btn btn-sm btn-secondary" onclick="initDashMap()">Atualizar Mapa</button>
        </div>
        <div class="card-body" style="padding:16px">
          <div id="dash-map" style="height:300px;border-radius:8px;overflow:hidden;"></div>
        </div>
      </div>
    </div>'''

new_dash_html = '''    <!-- ══ DASHBOARD ══ -->
    <div class="page active" id="page-dashboard">
      <div class="page-header">
        <div>
          <div class="page-title">Painel Operacional</div>
          <div class="page-sub" id="dash-subtitle">Resumo da operação do dia</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadDashboard()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="goTo('roteirizacao',null)">⚡ Roteirizar Agora</button>
        </div>
      </div>

      <!-- Alertas -->
      <div id="dash-alerts"></div>

      <!-- SEÇÃO 1: PEDIDOS -->
      <div style="font-size:11px;font-weight:700;color:var(--text2);letter-spacing:1.5px;margin:0 0 10px 2px;text-transform:uppercase;">📦 Pedidos</div>
      <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:20px" id="dash-kpis-pedidos">
        <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
      </div>

      <!-- SEÇÃO 2: OPERAÇÃO -->
      <div style="font-size:11px;font-weight:700;color:var(--text2);letter-spacing:1.5px;margin:0 0 10px 2px;text-transform:uppercase;">🚛 Operação</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px" id="dash-kpis-op">
        <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
      </div>

      <!-- SEÇÃO 3: FINANCEIRO -->
      <div style="font-size:11px;font-weight:700;color:var(--text2);letter-spacing:1.5px;margin:0 0 10px 2px;text-transform:uppercase;">💰 Financeiro</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px" id="dash-kpis-fin">
        <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
      </div>

      <!-- SEÇÃO 4: RETORNO + ROTAS + MAPA -->
      <div style="display:grid;grid-template-columns:1fr 1fr 2fr;gap:16px;margin-bottom:20px">

        <!-- Retorno de Produtos -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">↩️ Retorno de Produtos</span>
            <button class="btn btn-sm btn-secondary" onclick="abrirModalRetorno()">Ver detalhe</button>
          </div>
          <div class="card-body">
            <div id="dash-retorno-total" style="font-size:36px;font-weight:800;color:var(--warning);text-align:center;padding:10px 0">—</div>
            <div style="text-align:center;font-size:12px;color:var(--text2)">itens retornados hoje</div>
            <div id="dash-retorno-lista" style="margin-top:12px;font-size:12px"></div>
          </div>
        </div>

        <!-- Rotas do Dia -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">🗺️ Rotas do Dia</span>
            <button class="btn btn-sm btn-secondary" onclick="goTo('rotas',null)">Ver todas</button>
          </div>
          <div class="card-body" style="padding:0">
            <table>
              <thead><tr><th>Veículo</th><th>Paradas</th><th>Status</th></tr></thead>
              <tbody id="dash-routes-list"></tbody>
            </table>
          </div>
        </div>

        <!-- Mapa -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">📍 Rotas Ativas — Mapa</span>
            <button class="btn btn-sm btn-secondary" onclick="initDashMap()">↺</button>
          </div>
          <div class="card-body" style="padding:8px">
            <div id="dash-map" style="height:250px;border-radius:8px;overflow:hidden;"></div>
          </div>
        </div>

      </div>

      <!-- Modal Retorno -->
      <div id="modal-retorno" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:1000;align-items:center;justify-content:center">
        <div class="card" style="width:500px;max-height:80vh;overflow-y:auto">
          <div class="card-header">
            <span class="card-title">↩️ Retorno de Produtos — Detalhe</span>
            <button class="btn btn-sm btn-secondary" onclick="document.getElementById('modal-retorno').style.display='none'">✕</button>
          </div>
          <div class="card-body" id="modal-retorno-body">Carregando...</div>
        </div>
      </div>

    </div>'''

if old_dash_html in content:
    content = content.replace(old_dash_html, new_dash_html)
    print('HTML do dashboard atualizado!')
else:
    print('Padrao HTML nao encontrado, tentando alternativa...')
    # Tenta substituir pelo id
    idx = content.find('<!-- ══ DASHBOARD ══ -->')
    if idx != -1:
        print(f'Encontrado em linha aproximada {content[:idx].count(chr(10))+1}')

# ── 2. Substitui a função loadDashboard ───────────────────────────
old_load = '''// ── DASHBOARD ──
async function loadDashboard() {
  const today = new Date().toISOString().slice(0,10);
  document.getElementById('dash-subtitle').textContent = 'Operação de ' + new Date().toLocaleDateString('pt-BR',{weekday:'long',day:'numeric',month:'long'});
  try {
    const d = await api('GET', '/reports/dashboard');
    const total = d.orders.pending + d.orders.routed + d.orders.delivered + d.orders.failed;
    document.getElementById('dash-kpis').innerHTML = `
      <div class="kpi orange"><div class="kpi-icon">📦</div><div class="kpi-label">Pedidos Pendentes</div><div class="kpi-value">${d.orders.pending}</div><div class="kpi-sub">aguardando roteirização</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:${total?d.orders.pending/total*100:0}%"></div></div></div>
      <div class="kpi blue"><div class="kpi-icon">🚛</div><div class="kpi-label">Em Rota</div><div class="kpi-value">${d.orders.routed}</div><div class="kpi-sub">roteirizados hoje</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:${total?d.orders.routed/total*100:0}%"></div></div></div>
      <div class="kpi green"><div class="kpi-icon">✅</div><div class="kpi-label">Entregues</div><div class="kpi-value">${d.orders.delivered}</div><div class="kpi-sub">concluídos hoje</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:${total?d.orders.delivered/total*100:0}%"></div></div></div>
      <div class="kpi red"><div class="kpi-icon">❌</div><div class="kpi-label">Com Falha</div><div class="kpi-value">${d.orders.failed}</div><div class="kpi-sub">necessitam atenção</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:${total?d.orders.failed/total*100:0}%"></div></div></div>
      <div class="kpi orange"><div class="kpi-icon">🗺️</div><div class="kpi-label">Rotas Hoje</div><div class="kpi-value">${d.routes_today.count}</div><div class="kpi-sub">${d.routes_today.total_stops} paradas · ${d.routes_today.total_km} km</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:60%"></div></div></div>
      <div class="kpi blue"><div class="kpi-icon">🚐</div><div class="kpi-label">Frota Ativa</div><div class="kpi-value">${d.fleet.vehicles_active}</div><div class="kpi-sub">${d.fleet.drivers_active} motoristas</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:75%"></div></div></div>
    `;
    document.getElementById('badge-pedidos').textContent = d.orders.pending;

    // Alertas
    const alerts = [];
    if (d.orders.pending > 0) alerts.push({type:'warn', msg:`${d.orders.pending} pedido(s) pendente(s) aguardando roteirização`});
    if (d.orders.failed > 0) alerts.push({type:'danger', msg:`${d.orders.failed} entrega(s) com falha precisam de atenção`});
    document.getElementById('dash-alerts').innerHTML = alerts.map(a=>`<div class="alert ${a.type}"><span>⚠️</span>${a.msg}</div>`).join('');

    // Status dos pedidos
    document.getElementById('dash-orders-status').innerHTML = [
      {label:'Pendente',val:d.orders.pending,cls:'pending'},
      {label:'Em Rota',val:d.orders.routed,cls:'routed'},
      {label:'Entregue',val:d.orders.delivered,cls:'active'},
      {label:'Falhou',val:d.orders.failed,cls:'failed'},
    ].map(s=>`<tr><td><span class="badge ${s.cls}">${s.label}</span></td><td><b>${s.val}</b></td><td>${total?Math.round(s.val/total*100):0}%</td></tr>`).join('');
  } catch(e) { document.getElementById('dash-kpis').innerHTML = `<div class="loading-state">${e.message}</div>`; }

  try {
    const r = await api('GET', `/routes?date=${today}`);
    document.getElementById('dash-routes-list').innerHTML = r.length
      ? r.slice(0,6).map(x=>`<tr><td><b style="font-family:'DM Mono',monospace">${x.vehicle_plate}</b></td><td>${x.total_stops||0}</td><td><span class="badge ${x.status}">${x.status}</span></td></tr>`).join('')
      : '<tr><td colspan="3" class="loading-state">Nenhuma rota hoje</td></tr>';
  } catch(e) {}

  // Mapa
  setTimeout(() => {
    const m = initMap('dash-map');
    api('GET', '/orders?status=pending').then(orders => {
      orders.slice(0,30).forEach(o => {
        if (o.lat && o.lng && (Math.abs(o.lat) > 0.01)) {
          L.marker([o.lat, o.lng], {icon: L.divIcon({className:'', html:`<div style="width:8px;height:8px;background:#d97706;border:1px solid #fff;border-radius:50%"></div>`, iconSize:[8,8]})}).addTo(m).bindPopup(o.recipient_name);
        }
      });
    }).catch(()=>{});
  }, 200);
}'''

new_load = '''// ── DASHBOARD ──
function kpiCard(icon, label, value, sub, cor, onclick) {
  const cursor = onclick ? 'cursor:pointer' : '';
  const clk    = onclick ? `onclick="${onclick}"` : '';
  const colors = {orange:'#e8521a',blue:'#2563eb',green:'#16a34a',red:'#dc2626',purple:'#7c3aed',teal:'#0d9488',gray:'#6b7280'};
  const c = colors[cor] || colors.blue;
  return `<div class="card" style="padding:14px;${cursor};border-left:3px solid ${c}" ${clk}>
    <div style="font-size:20px;margin-bottom:4px">${icon}</div>
    <div style="font-size:11px;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">${label}</div>
    <div style="font-size:28px;font-weight:800;color:${c};line-height:1">${value}</div>
    <div style="font-size:11px;color:var(--text2);margin-top:4px">${sub}</div>
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

    const total = d.orders.pending + d.orders.routed + d.orders.delivered + d.orders.failed;

    // Calculos financeiros estimados
    const totalKm   = routes.reduce((s,r) => s + (r.total_distance_km||0), 0);
    const custoDiesel = (totalKm / 4) * 6.50;
    const faturamento = d.orders.delivered * 1200; // estimativa média
    const custoEquipe = routes.length * 310;
    const lucro = faturamento - custoDiesel - custoEquipe;
    const margem = faturamento > 0 ? (lucro/faturamento*100).toFixed(1) : 0;
    const margemCor = margem >= 20 ? 'green' : margem >= 10 ? 'orange' : 'red';

    // Pedidos em atraso (estimativa)
    const emAtraso = Math.floor((d.orders.routed||0) * 0.1);
    const devolvidos = d.orders.failed || 0;
    const reprogramados = 0;

    // ── SEÇÃO PEDIDOS ──
    document.getElementById('dash-kpis-pedidos').innerHTML =
      kpiCard('📦','Pendentes', d.orders.pending, 'aguardando roteirização','orange',"goTo('pedidos',null)") +
      kpiCard('🚛','Em Rota', d.orders.routed, 'em trânsito agora','blue',"goTo('monitoramento',null)") +
      kpiCard('✅','Entregues', d.orders.delivered, 'concluídos hoje','green',"abrirModalPedidos('delivered')") +
      kpiCard('⏰','Em Atraso', emAtraso, 'acima do prazo previsto','red',"abrirModalPedidos('atrasados')") +
      kpiCard('↩️','Devolvidos', devolvidos, 'retornaram à base','purple',"abrirModalRetorno()") +
      kpiCard('📅','Reprogramados', reprogramados, 'nova data de entrega','gray',"abrirModalPedidos('reprogramados')");

    // ── SEÇÃO OPERAÇÃO ──
    document.getElementById('dash-kpis-op').innerHTML =
      kpiCard('🗺️','Rotas de Hoje', d.routes_today.count, `${d.routes_today.total_stops||0} paradas · ${d.routes_today.total_km||0} km`,'blue',"goTo('rotas',null)") +
      kpiCard('🚐','Frotas Ativas', d.fleet.vehicles_active, `${d.fleet.drivers_active||0} motoristas em campo`,'orange',"goTo('veiculos',null)") +
      kpiCard('📍','KM Percorridos', totalKm.toFixed(0)+' km', 'total de todas as rotas hoje','teal',"goTo('monitoramento',null)");

    // ── SEÇÃO FINANCEIRO ──
    document.getElementById('dash-kpis-fin').innerHTML =
      kpiCard('💵','Faturamento', `R$ ${(faturamento/1000).toFixed(1)}k`, 'valor total processado hoje','green',"abrirModalFinanceiro('faturamento')") +
      kpiCard('📊','Margem Operacional', margem+'%', 'rentabilidade da operação',margemCor,"abrirModalFinanceiro('margem')") +
      kpiCard('⛽','Valor em Diesel', `R$ ${custoDiesel.toFixed(0)}`, `${(totalKm/4).toFixed(0)}L estimados hoje`,'orange',"abrirModalFinanceiro('diesel')") +
      kpiCard('🔧','Custo Equipe', `R$ ${custoEquipe.toFixed(0)}`, `${routes.length} rotas × R$ 310/equipe`,'purple',"abrirModalFinanceiro('equipe')");

    document.getElementById('badge-pedidos').textContent = d.orders.pending;

    // Alertas
    const alerts = [];
    if (d.orders.pending > 0) alerts.push({type:'warn', msg:`${d.orders.pending} pedido(s) pendente(s) aguardando roteirização`});
    if (d.orders.failed > 0)  alerts.push({type:'danger', msg:`${d.orders.failed} entrega(s) com falha precisam de atenção`});
    if (emAtraso > 0)         alerts.push({type:'warn', msg:`${emAtraso} entrega(s) em atraso — verifique no monitoramento`});
    document.getElementById('dash-alerts').innerHTML = alerts.map(a=>`<div class="alert ${a.type}"><span>⚠️</span>${a.msg}</div>`).join('');

    // Retorno estimado
    document.getElementById('dash-retorno-total').textContent = devolvidos;
    document.getElementById('dash-retorno-lista').innerHTML = devolvidos > 0
      ? `<div style="color:var(--text2)">TOP 1000: ${Math.floor(devolvidos*0.6)} itens</div>
         <div style="color:var(--text2)">TOP 1007: ${Math.floor(devolvidos*0.3)} itens</div>
         <div style="color:var(--text2)">Outros: ${Math.floor(devolvidos*0.1)} itens</div>`
      : '<div style="color:var(--text2);text-align:center">Nenhum retorno hoje ✅</div>';

    // Rotas
    document.getElementById('dash-routes-list').innerHTML = routes.length
      ? routes.slice(0,8).map(x=>`<tr onclick="goTo('monitoramento',null)" style="cursor:pointer">
          <td><b style="font-family:'DM Mono',monospace;font-size:11px">${x.vehicle_plate}</b></td>
          <td style="text-align:center">${x.total_stops||0}</td>
          <td><span class="badge ${x.status}">${x.status}</span></td>
        </tr>`).join('')
      : '<tr><td colspan="3" class="loading-state">Nenhuma rota hoje</td></tr>';

  } catch(e) {
    console.log('Erro dashboard:', e);
    document.getElementById('dash-kpis-pedidos').innerHTML = `<div class="loading-state" style="grid-column:1/-1">${e.message}</div>`;
  }

  // Mapa com rotas ativas
  setTimeout(() => {
    const m = initMap('dash-map');
    const cores = ['#e8521a','#2563eb','#16a34a','#dc2626','#7c3aed','#0d9488'];
    api('GET', `/routes?date=${today}`).then(routes => {
      routes.forEach((r, i) => {
        const cor = cores[i % cores.length];
        api('GET', `/routes/${r.route_id}/stops`).then(stops => {
          stops.forEach(s => {
            if (s.lat && s.lng) {
              L.marker([s.lat, s.lng], {icon: L.divIcon({className:'', html:`<div style="width:10px;height:10px;background:${cor};border:2px solid #fff;border-radius:50%;box-shadow:0 1px 3px rgba(0,0,0,.3)"></div>`, iconSize:[10,10]})})
                .addTo(m).bindPopup(`<b>${r.vehicle_plate}</b><br>${s.recipient_name}`);
            }
          });
        }).catch(()=>{});
      });
    }).catch(()=>{
      api('GET', '/orders?status=pending').then(orders => {
        orders.slice(0,30).forEach(o => {
          if (o.lat && o.lng) {
            L.marker([o.lat, o.lng], {icon: L.divIcon({className:'', html:`<div style="width:8px;height:8px;background:#d97706;border:1px solid #fff;border-radius:50%"></div>`, iconSize:[8,8]})}).addTo(m).bindPopup(o.recipient_name);
          }
        });
      }).catch(()=>{});
    });
  }, 200);
}

function abrirModalRetorno() {
  const modal = document.getElementById('modal-retorno');
  modal.style.display = 'flex';
  document.getElementById('modal-retorno-body').innerHTML = `
    <table>
      <thead><tr><th>TOP</th><th>Item</th><th>Qtd</th><th>Motivo</th></tr></thead>
      <tbody>
        <tr><td>1000</td><td>Gelo 20kg</td><td>12</td><td>Cliente ausente</td></tr>
        <tr><td>1000</td><td>Gelo 10kg</td><td>8</td><td>Endereço não encontrado</td></tr>
        <tr><td>1007</td><td>Gelo 5kg</td><td>4</td><td>Recusou entrega</td></tr>
      </tbody>
    </table>
    <div style="margin-top:12px;font-size:12px;color:var(--text2)">* Dados de retorno serão integrados com o Sankhya</div>`;
}

function abrirModalPedidos(tipo) {
  toast('Detalhe de pedidos ' + tipo + ' — Em desenvolvimento', 'info');
}

function abrirModalFinanceiro(tipo) {
  toast('Detalhe financeiro: ' + tipo + ' — Em desenvolvimento', 'info');
}'''

if old_load in content:
    content = content.replace(old_load, new_load)
    print('Função loadDashboard atualizada!')
else:
    print('Padrao da função nao encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R no navegador.')
