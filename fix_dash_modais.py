path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona funções de modal e kpiCard antes de loadDashboard
new_js = '''
// ── DASHBOARD MODAIS ──────────────────────────────────────────────
function fecharModalDash() {
  document.getElementById('modal-dash').style.display = 'none';
}

function abrirModalDash(tipo, titulo) {
  document.getElementById('modal-dash-title').textContent = titulo;
  document.getElementById('modal-dash').style.display = 'flex';
  const body = document.getElementById('modal-dash-body');
  body.innerHTML = '<div class="loading-state">Carregando...</div>';

  const today = new Date().toISOString().slice(0,10);

  if (tipo === 'pedidos-pendentes') {
    api('GET', '/orders?status=pending&limit=50').then(orders => {
      body.innerHTML = orders.length ? `
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Endereço</th><th>Peso</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td style="font-size:12px;color:#90afd4">${o.address||'—'}</td>
            <td>${o.weight_kg||0}kg</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhum pedido pendente</div>';
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else if (tipo === 'pedidos-rota') {
    api('GET', '/orders?status=routed&limit=50').then(orders => {
      body.innerHTML = orders.length ? `
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Status</th><th>Peso</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td><span class="badge ${o.status}">${o.status}</span></td>
            <td>${o.weight_kg||0}kg</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhum pedido em rota</div>';
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else if (tipo === 'pedidos-entregues') {
    api('GET', '/orders?status=delivered&limit=50').then(orders => {
      body.innerHTML = orders.length ? `
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Peso</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td>${o.weight_kg||0}kg</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhuma entrega hoje</div>';
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else if (tipo === 'pedidos-falha') {
    api('GET', '/orders?status=failed&limit=50').then(orders => {
      body.innerHTML = orders.length ? `
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Motivo</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td style="color:#f87171">${o.failure_reason||'Não informado'}</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhuma falha hoje ✅</div>';
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else if (tipo === 'rotas') {
    api('GET', `/routes?date=${today}`).then(routes => {
      body.innerHTML = routes.length ? `
        <table>
          <thead><tr><th>Veículo</th><th>Motorista</th><th>Paradas</th><th>KM</th><th>Status</th></tr></thead>
          <tbody>${routes.map(r=>`<tr>
            <td><b style="font-family:monospace">${r.vehicle_plate}</b></td>
            <td>${r.driver_name||'—'}</td>
            <td style="text-align:center">${r.total_stops||0}</td>
            <td>${r.total_distance_km||0}km</td>
            <td><span class="badge ${r.status}">${r.status}</span></td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhuma rota hoje</div>';
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else if (tipo === 'frotas') {
    api('GET', '/vehicles').then(veics => {
      const ativos = veics.filter(v => v.status === 'active');
      body.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
          ${ativos.map(v=>`<div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:14px">
            <div style="font-size:16px;font-weight:700;color:#64B4FF;font-family:monospace">${v.plate}</div>
            <div style="font-size:12px;color:#90afd4;margin-top:4px">${v.model||'—'} · ${v.capacity_kg||0}kg</div>
            <div style="margin-top:8px"><span class="badge active">Ativo</span></div>
          </div>`).join('')}
        </div>`;
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else if (tipo === 'retorno') {
    body.innerHTML = `
      <div style="margin-bottom:16px;padding:12px;background:#0a1628;border-radius:8px;border:1px solid #1e3a5c">
        <div style="font-size:12px;color:#90afd4;margin-bottom:8px">Retornos por TOP (estimativa — integração Sankhya pendente)</div>
        <table>
          <thead><tr><th>TOP</th><th>Item</th><th>Qtd Saiu</th><th>Qtd Retornou</th><th>Motivo</th></tr></thead>
          <tbody>
            <tr><td>1000</td><td>Gelo 20kg</td><td>50</td><td>12</td><td style="color:#f87171">Cliente ausente</td></tr>
            <tr><td>1000</td><td>Gelo 10kg</td><td>80</td><td>8</td><td style="color:#f87171">End. não encontrado</td></tr>
            <tr><td>1007</td><td>Gelo 5kg</td><td>30</td><td>4</td><td style="color:#f87171">Recusou entrega</td></tr>
          </tbody>
        </table>
      </div>
      <div style="font-size:11px;color:#90afd4">* Dados serão integrados com o Sankhya futuramente</div>`;
  }
  else if (tipo === 'financeiro') {
    const today2 = new Date().toISOString().slice(0,10);
    api('GET', `/routes?date=${today2}`).then(routes => {
      const km = routes.reduce((s,r)=>s+(r.total_distance_km||0),0);
      const diesel = (km/4)*6.50;
      const equipe = routes.length*310;
      const fat = 0; // virá do Sankhya
      body.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:16px">
            <div style="font-size:11px;color:#90afd4;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px">Custos Operacionais</div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c"><span style="color:#90afd4">Diesel (${(km/4).toFixed(0)}L)</span><span style="color:#f87171;font-weight:600">R$ ${diesel.toFixed(2)}</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c"><span style="color:#90afd4">Equipe (${routes.length} rotas)</span><span style="color:#f87171;font-weight:600">R$ ${equipe.toFixed(2)}</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0"><span style="color:#90afd4;font-weight:700">Total Custos</span><span style="color:#f87171;font-weight:800">R$ ${(diesel+equipe).toFixed(2)}</span></div>
          </div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:16px">
            <div style="font-size:11px;color:#90afd4;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px">KM e Combustível</div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c"><span style="color:#90afd4">KM Total</span><span style="color:#64B4FF;font-weight:600">${km.toFixed(1)} km</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c"><span style="color:#90afd4">Consumo Médio</span><span style="color:#64B4FF;font-weight:600">4 km/L</span></div>
            <div style="display:flex;justify-content:space-between;padding:8px 0"><span style="color:#90afd4">Preço Diesel</span><span style="color:#64B4FF;font-weight:600">R$ 6,50/L</span></div>
          </div>
        </div>
        <div style="margin-top:12px;padding:10px;background:#061020;border-radius:8px;font-size:11px;color:#90afd4">
          * Faturamento e margem serão integrados com o Sankhya
        </div>`;
    }).catch(e => { body.innerHTML = `<div class="loading-state">${e.message}</div>`; });
  }
  else {
    body.innerHTML = `<div class="loading-state">Em desenvolvimento — integração Sankhya pendente</div>`;
  }
}

'''

# Injeta antes da função loadDashboard
if 'abrirModalDash' not in content:
    content = content.replace('// ── DASHBOARD ──\nasync function loadDashboard()', new_js + '// ── DASHBOARD ──\nasync function loadDashboard()')
    print('Funções de modal adicionadas!')

# Atualiza o kpiCard para usar abrirModalDash
old_kpi = '''function kpiCard(icon, label, value, sub, cor, onclick) {
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
}'''

new_kpi = '''function kpiCard(icon, label, value, sub, cor, modalTipo) {
  const colors = {orange:'#f59e0b',blue:'#64B4FF',green:'#10b981',red:'#f87171',purple:'#a78bfa',teal:'#2dd4bf',gray:'#94a3b8'};
  const c = colors[cor] || colors.blue;
  const clk = modalTipo ? `onclick="abrirModalDash('${modalTipo}','${icon} ${label}')"` : '';
  return `<div class="card" style="padding:14px;${modalTipo?'cursor:pointer':''}; border-left:3px solid ${c};margin-bottom:0;transition:all .15s" ${clk}
    onmouseover="if(this.style.borderColor)this.style.background='#142040'"
    onmouseout="this.style.background=''">
    <div style="font-size:18px;margin-bottom:6px">${icon}</div>
    <div style="font-size:10px;color:#90afd4;font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px">${label}</div>
    <div style="font-size:26px;font-weight:800;color:${c};line-height:1">${value}</div>
    <div style="font-size:11px;color:#90afd4;margin-top:6px">${sub}</div>
    ${modalTipo ? `<div style="font-size:10px;color:${c};margin-top:8px;opacity:.7">Clique para detalhar →</div>` : ''}
  </div>`;
}'''

if old_kpi in content:
    content = content.replace(old_kpi, new_kpi)
    print('kpiCard atualizado!')

# Atualiza os kpiCards com os tipos de modal corretos
old_kpis_pedidos = '''    document.getElementById('dash-kpis-pedidos').innerHTML =
      kpiCard('📦','Pendentes', d.orders.pending, 'aguardando roteirização','orange',"goTo('pedidos',null)") +
      kpiCard('🚛','Em Rota', d.orders.routed, 'em trânsito agora','blue',"goTo('monitoramento',null)") +
      kpiCard('✅','Entregues', d.orders.delivered, 'concluídos hoje','green',"abrirModalPedidos('delivered')") +
      kpiCard('⏰','Em Atraso', emAtraso, 'acima do prazo previsto','red',"abrirModalPedidos('atrasados')") +
      kpiCard('↩️','Devolvidos', devolvidos, 'retornaram à base','purple',"abrirModalRetorno()") +
      kpiCard('📅','Reprogramados', reprogramados, 'nova data de entrega','gray',"abrirModalPedidos('reprogramados')");'''

new_kpis_pedidos = '''    document.getElementById('dash-kpis-pedidos').innerHTML =
      kpiCard('📦','Pendentes', d.orders.pending, 'aguardando roteirização','orange','pedidos-pendentes') +
      kpiCard('🚛','Em Rota', d.orders.routed, 'em trânsito agora','blue','pedidos-rota') +
      kpiCard('✅','Entregues', d.orders.delivered, 'concluídos hoje','green','pedidos-entregues') +
      kpiCard('⏰','Em Atraso', emAtraso, 'acima do prazo previsto','red','pedidos-falha') +
      kpiCard('↩️','Devolvidos', devolvidos, 'retornaram à base','purple','retorno') +
      kpiCard('📅','Reprogramados', reprogramados, 'nova data de entrega','gray','');'''

if old_kpis_pedidos in content:
    content = content.replace(old_kpis_pedidos, new_kpis_pedidos)
    print('KPIs pedidos atualizados!')

old_kpis_op = '''    document.getElementById('dash-kpis-op').innerHTML =
      kpiCard('🗺️','Rotas de Hoje', d.routes_today.count, `${d.routes_today.total_stops||0} paradas · ${d.routes_today.total_km||0} km`,'blue',"goTo('rotas',null)") +
      kpiCard('🚐','Frotas Ativas', d.fleet.vehicles_active, `${d.fleet.drivers_active||0} motoristas em campo`,'orange',"goTo('veiculos',null)") +
      kpiCard('📍','KM Percorridos', totalKm.toFixed(0)+' km', 'total de todas as rotas hoje','teal',"goTo('monitoramento',null)");'''

new_kpis_op = '''    document.getElementById('dash-kpis-op').innerHTML =
      kpiCard('🗺️','Rotas de Hoje', d.routes_today.count, `${d.routes_today.total_stops||0} paradas · ${d.routes_today.total_km||0} km`,'blue','rotas') +
      kpiCard('🚐','Frotas Ativas', d.fleet.vehicles_active, `${d.fleet.drivers_active||0} motoristas em campo`,'orange','frotas') +
      kpiCard('📍','KM Percorridos', totalKm.toFixed(0)+' km', 'total de todas as rotas hoje','teal','financeiro');'''

if old_kpis_op in content:
    content = content.replace(old_kpis_op, new_kpis_op)
    print('KPIs operação atualizados!')

old_kpis_fin = '''    document.getElementById('dash-kpis-fin').innerHTML =
      kpiCard('💵','Faturamento', `R$ ${(faturamento/1000).toFixed(1)}k`, 'valor total processado hoje','green',"abrirModalFinanceiro('faturamento')") +
      kpiCard('📊','Margem Operacional', margem+'%', 'rentabilidade da operação',margemCor,"abrirModalFinanceiro('margem')") +
      kpiCard('⛽','Valor em Diesel', `R$ ${custoDiesel.toFixed(0)}`, `${(totalKm/4).toFixed(0)}L estimados hoje`,'orange',"abrirModalFinanceiro('diesel')") +
      kpiCard('🔧','Custo Equipe', `R$ ${custoEquipe.toFixed(0)}`, `${routes.length} rotas × R$ 310/equipe`,'purple',"abrirModalFinanceiro('equipe')");'''

new_kpis_fin = '''    document.getElementById('dash-kpis-fin').innerHTML =
      kpiCard('💵','Faturamento', `R$ ${(faturamento/1000).toFixed(1)}k`, 'valor total processado hoje','green','financeiro') +
      kpiCard('📊','Margem Operacional', margem+'%', 'rentabilidade da operação',margemCor,'financeiro') +
      kpiCard('⛽','Valor em Diesel', `R$ ${custoDiesel.toFixed(0)}`, `${(totalKm/4).toFixed(0)}L estimados hoje`,'orange','financeiro') +
      kpiCard('🔧','Custo Equipe', `R$ ${custoEquipe.toFixed(0)}`, `${routes.length} rotas × R$ 310/equipe`,'purple','financeiro');'''

if old_kpis_fin in content:
    content = content.replace(old_kpis_fin, new_kpis_fin)
    print('KPIs financeiro atualizados!')

# Remove funções antigas
content = content.replace('''
function abrirModalPedidos(tipo) {
  toast('Detalhe de pedidos ' + tipo + ' — Em desenvolvimento', 'info');
}

function abrirModalFinanceiro(tipo) {
  toast('Detalhe financeiro: ' + tipo + ' — Em desenvolvimento', 'info');
}''', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R no navegador.')
