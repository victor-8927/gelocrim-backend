path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_js = '''
// ── DASHBOARD MODAIS ──────────────────────────────────────────────
function fecharModalDash() {
  document.getElementById('modal-dash').style.display = 'none';
}

async function abrirModalDash(tipo, titulo) {
  document.getElementById('modal-dash-title').textContent = titulo;
  document.getElementById('modal-dash').style.display = 'flex';
  const body = document.getElementById('modal-dash-body');
  body.innerHTML = '<div class="loading-state">Carregando...</div>';
  const today = new Date().toISOString().slice(0,10);

  try {
    if (tipo === 'pedidos-pendentes') {
      const orders = await api('GET', '/orders?status=pending&limit=100');
      body.innerHTML = orders.length ? `
        <div style="margin-bottom:12px;font-size:13px;color:#90afd4">${orders.length} pedidos aguardando roteirização</div>
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Endereço</th><th>Peso</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td style="font-size:12px;color:#90afd4;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${o.address||'—'}</td>
            <td>${o.weight_kg||0}kg</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhum pedido pendente ✅</div>';
    }
    else if (tipo === 'pedidos-rota') {
      const orders = await api('GET', '/orders?status=routed&limit=100');
      body.innerHTML = orders.length ? `
        <div style="margin-bottom:12px;font-size:13px;color:#90afd4">${orders.length} pedidos em trânsito</div>
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Status</th><th>Peso</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td><span class="badge ${o.status}">${o.status}</span></td>
            <td>${o.weight_kg||0}kg</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhum pedido em rota</div>';
    }
    else if (tipo === 'pedidos-entregues') {
      const orders = await api('GET', '/orders?status=delivered&limit=100');
      body.innerHTML = orders.length ? `
        <div style="margin-bottom:12px;font-size:13px;color:#10b981">${orders.length} entregas concluídas hoje ✅</div>
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Peso</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td>${o.weight_kg||0}kg</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhuma entrega hoje</div>';
    }
    else if (tipo === 'pedidos-falha') {
      const orders = await api('GET', '/orders?status=failed&limit=100');
      body.innerHTML = orders.length ? `
        <div style="margin-bottom:12px;font-size:13px;color:#f87171">${orders.length} entregas com falha</div>
        <table>
          <thead><tr><th>Pedido</th><th>Cliente</th><th>Motivo</th></tr></thead>
          <tbody>${orders.map(o=>`<tr>
            <td style="font-family:monospace;font-size:11px">${o.external_id||'—'}</td>
            <td><b>${o.recipient_name}</b></td>
            <td style="color:#f87171">${o.failure_reason||'Não informado'}</td>
          </tr>`).join('')}</tbody>
        </table>` : '<div class="loading-state">Nenhuma falha hoje ✅</div>';
    }
    else if (tipo === 'rotas') {
      const routes = await api('GET', `/routes?date=${today}`);
      body.innerHTML = routes.length ? `
        <div style="margin-bottom:12px;font-size:13px;color:#90afd4">${routes.length} rotas hoje</div>
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
    }
    else if (tipo === 'frotas') {
      const veics = await api('GET', '/vehicles');
      const ativos = veics.filter(v => v.status === 'active');
      body.innerHTML = `
        <div style="margin-bottom:12px;font-size:13px;color:#90afd4">${ativos.length} veículos ativos</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
          ${ativos.map(v=>`<div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:14px">
            <div style="font-size:18px;font-weight:700;color:#64B4FF;font-family:monospace">${v.plate}</div>
            <div style="font-size:12px;color:#90afd4;margin-top:4px">${v.model||'—'} · ${v.capacity_kg||0}kg</div>
            <div style="margin-top:8px"><span class="badge active">Ativo</span></div>
          </div>`).join('')}
        </div>`;
    }
    else if (tipo === 'financeiro') {
      const routes = await api('GET', `/routes?date=${today}`);
      const km = routes.reduce((s,r)=>s+(r.total_distance_km||0),0);
      const diesel = (km/4)*6.50;
      const equipe = routes.length*310;
      body.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px">
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:16px">
            <div style="font-size:10px;color:#90afd4;margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;font-weight:700">Custos Operacionais</div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c">
              <span style="color:#90afd4">Diesel (${(km/4).toFixed(0)}L)</span>
              <span style="color:#f87171;font-weight:600">R$ ${diesel.toFixed(2)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c">
              <span style="color:#90afd4">Equipe (${routes.length} rotas)</span>
              <span style="color:#f87171;font-weight:600">R$ ${equipe.toFixed(2)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:10px 0">
              <span style="color:#e8f0fe;font-weight:700">Total Custos</span>
              <span style="color:#f87171;font-weight:800;font-size:16px">R$ ${(diesel+equipe).toFixed(2)}</span>
            </div>
          </div>
          <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:16px">
            <div style="font-size:10px;color:#90afd4;margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;font-weight:700">KM e Combustível</div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c">
              <span style="color:#90afd4">KM Total</span>
              <span style="color:#64B4FF;font-weight:600">${km.toFixed(1)} km</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1e3a5c">
              <span style="color:#90afd4">Consumo Médio</span>
              <span style="color:#64B4FF;font-weight:600">4 km/L</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:8px 0">
              <span style="color:#90afd4">Preço Diesel</span>
              <span style="color:#64B4FF;font-weight:600">R$ 6,50/L</span>
            </div>
          </div>
        </div>
        <div style="padding:10px;background:#061020;border-radius:8px;font-size:11px;color:#90afd4">
          * Faturamento e margem serão integrados com o Sankhya
        </div>`;
    }
    else if (tipo === 'retorno') {
      body.innerHTML = `
        <div style="margin-bottom:12px;font-size:13px;color:#90afd4">Retornos por TOP — hoje</div>
        <table>
          <thead><tr><th>TOP</th><th>Item</th><th>Qtd Saiu</th><th>Qtd Retornou</th><th>Motivo</th></tr></thead>
          <tbody>
            <tr><td>1000</td><td>Gelo 20kg</td><td>50</td><td>0</td><td style="color:#10b981">—</td></tr>
            <tr><td>1000</td><td>Gelo 10kg</td><td>80</td><td>0</td><td style="color:#10b981">—</td></tr>
            <tr><td>1007</td><td>Gelo 5kg (bonif.)</td><td>30</td><td>0</td><td style="color:#10b981">—</td></tr>
          </tbody>
        </table>
        <div style="margin-top:12px;padding:10px;background:#061020;border-radius:8px;font-size:11px;color:#90afd4">
          * Dados de retorno serão integrados com o Sankhya (TOPs 1000/1007)
        </div>`;
    }
    else {
      body.innerHTML = '<div class="loading-state">Em desenvolvimento — integração Sankhya pendente</div>';
    }
  } catch(e) {
    body.innerHTML = `<div class="loading-state">Erro: ${e.message}</div>`;
  }
}

'''

# Injeta antes da função kpiCard
if 'async function abrirModalDash' not in content:
    content = content.replace('function kpiCard(', new_js + 'function kpiCard(')
    print('Função abrirModalDash adicionada!')
else:
    print('Função já existe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
