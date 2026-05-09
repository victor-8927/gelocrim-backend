path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_pedidos = '''    <div class="page" id="page-pedidos">
      <div class="page-header">
        <div>
          <div class="page-title">Gestão de Pedidos</div>
          <div class="page-sub">Pedidos importados do Sankhya para roteirização</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadOrders()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="openModal('order')">+ Novo Pedido</button>
        </div>
      </div>
      <div class="filters-bar">
        <div class="filter-group">
          <span class="filter-label">Status</span>
          <select class="filter-input" id="f-status" onchange="loadOrders()">
            <option value="">Todos</option>
            <option value="pending">Pendente</option>
            <option value="routed">Roteirizado</option>
            <option value="delivered">Entregue</option>
            <option value="failed">Falhou</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Limite</span>
          <select class="filter-input" id="f-limit" onchange="loadOrders()">
            <option value="50">50</option>
            <option value="100" selected>100</option>
            <option value="200">200</option>
            <option value="500">500</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Buscar</span>
          <input class="filter-input" id="f-search" placeholder="Cliente, endereço..." onkeyup="filterOrdersLocal()">
        </div>
        <button class="btn btn-secondary btn-sm" style="align-self:flex-end" onclick="loadOrders()">Filtrar</button>
        <div style="margin-left:auto;align-self:flex-end">
          <span id="orders-count" style="font-size:12px;color:var(--muted);font-family:'DM Mono',monospace"></span>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <table>
            <thead>
              <tr>
                <th>Nº Pedido</th><th>Cliente</th><th>Endereço</th>
                <th>Peso</th><th>Volume</th><th>Janela</th>
                <th>Prioridade</th><th>Status</th><th>Ações</th>
              </tr>
            </thead>
            <tbody id="orders-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>'''

new_pedidos = '''    <div class="page" id="page-pedidos">
      <div class="page-header">
        <div>
          <div class="page-title">Gestão de Pedidos</div>
          <div class="page-sub" id="orders-sub">Pedidos importados do Sankhya para roteirização</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadOrders()">↺ Atualizar</button>
          <button class="btn btn-secondary" onclick="sincronizarSankhya()" style="border-color:#64B4FF;color:#64B4FF">
            🔄 Sincronizar Sankhya
          </button>
          <button class="btn btn-primary" onclick="openModal('order')">+ Novo Pedido</button>
        </div>
      </div>

      <!-- KPIs RÁPIDOS DE PEDIDOS -->
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:16px" id="pedidos-kpis">
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #f59e0b">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Pendentes</div>
          <div style="font-size:24px;font-weight:800;color:#f59e0b" id="pk-pendentes">—</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #64B4FF">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Em Rota</div>
          <div style="font-size:24px;font-weight:800;color:#64B4FF" id="pk-rota">—</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #10b981">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Entregues</div>
          <div style="font-size:24px;font-weight:800;color:#10b981" id="pk-entregues">—</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #f87171">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Com Falha</div>
          <div style="font-size:24px;font-weight:800;color:#f87171" id="pk-falha">—</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #a78bfa">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">Total Peso</div>
          <div style="font-size:24px;font-weight:800;color:#a78bfa" id="pk-peso">—</div>
        </div>
      </div>

      <!-- FILTROS -->
      <div class="filters-bar" style="flex-wrap:wrap;gap:10px">
        <div class="filter-group">
          <span class="filter-label">Status</span>
          <select class="filter-input" id="f-status" onchange="loadOrders()">
            <option value="">Todos</option>
            <option value="pending">Pendente</option>
            <option value="routed">Roteirizado</option>
            <option value="delivered">Entregue</option>
            <option value="failed">Falhou</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Zona</span>
          <select class="filter-input" id="f-zona" onchange="filterOrdersLocal()">
            <option value="">Todas</option>
            <option value="norte">Zona Norte</option>
            <option value="sul">Zona Sul</option>
            <option value="leste">Zona Leste</option>
            <option value="oeste">Zona Oeste</option>
            <option value="centro">Centro</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">TOP</span>
          <select class="filter-input" id="f-top" onchange="filterOrdersLocal()">
            <option value="">Todos</option>
            <option value="1000">TOP 1000 — Venda</option>
            <option value="1007">TOP 1007 — Bonificação</option>
            <option value="1008">TOP 1008 — Consignado</option>
            <option value="1009">TOP 1009 — Troca</option>
            <option value="1010">TOP 1010 — Pré-pedido</option>
          </select>
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Buscar</span>
          <input class="filter-input" id="f-search" placeholder="Cliente, pedido, endereço..." onkeyup="filterOrdersLocal()" style="width:220px">
        </div>
        <div class="filter-sep"></div>
        <div class="filter-group">
          <span class="filter-label">Limite</span>
          <select class="filter-input" id="f-limit" onchange="loadOrders()">
            <option value="50">50</option>
            <option value="100" selected>100</option>
            <option value="200">200</option>
            <option value="500">500</option>
          </select>
        </div>
        <div style="margin-left:auto;align-self:flex-end;display:flex;align-items:center;gap:12px">
          <span id="orders-count" style="font-size:12px;color:#90afd4;font-family:'DM Mono',monospace"></span>
          <span id="sankhya-status" style="font-size:11px;color:#10b981"></span>
        </div>
      </div>

      <!-- TABELA -->
      <div class="card">
        <div class="card-body" style="padding:0;overflow-x:auto">
          <table>
            <thead>
              <tr>
                <th style="width:30px"><input type="checkbox" id="chk-all" onchange="toggleTodosOrders(this.checked)" title="Selecionar todos"></th>
                <th>Nº Pedido</th>
                <th>Cliente</th>
                <th>Endereço / Zona</th>
                <th>Peso (kg)</th>
                <th>Valor (R$)</th>
                <th>TOP</th>
                <th>Janela</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody id="orders-tbody">
              <tr><td colspan="10" class="loading-state">Carregando pedidos...</td></tr>
            </tbody>
          </table>
        </div>
        <!-- Ações em lote -->
        <div id="orders-acoes-lote" style="display:none;padding:10px 16px;background:#0a1628;border-top:1px solid #1e3a5c;display:none;align-items:center;gap:10px">
          <span id="orders-selecionados" style="font-size:13px;color:#90afd4"></span>
          <button class="btn btn-sm btn-primary" onclick="adicionarSelecionadosRota()">➕ Adicionar à Rota</button>
          <button class="btn btn-sm btn-secondary" onclick="limparSelecaoOrders()">✕ Limpar seleção</button>
        </div>
      </div>

      <!-- MODAL DETALHE PEDIDO -->
      <div id="modal-pedido-detalhe" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:640px;max-height:85vh;overflow-y:auto">
          <div style="padding:20px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-ped-titulo">Detalhe do Pedido</span>
            <button onclick="document.getElementById('modal-pedido-detalhe').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div id="modal-ped-body" style="padding:20px 24px"></div>
        </div>
      </div>

    </div>'''

if old_pedidos in content:
    content = content.replace(old_pedidos, new_pedidos)
    print('HTML de pedidos atualizado!')
else:
    print('Padrao nao encontrado!')

# Adiciona funções JS para a nova tela de pedidos
new_js = '''
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

'''

if 'function sincronizarSankhya' not in content:
    content = content.replace('// ── ORDERS ──', new_js + '// ── ORDERS ──')
    print('Funções de pedidos adicionadas!')

# Atualiza o renderOrders para incluir checkbox e botão de detalhe
old_render = '''function renderOrders(orders) {
  const prioLabel = {1:'Normal',2:'Alta',3:'Urgente'};
  const prioClass = {1:'draft',2:'pending',3:'failed'};
  document.getElementById('orders-tbody').innerHTML = orders.length
    ? orders.map(x => `<tr>
        <td style="font-family:'DM Mono',monospace;font-size:12px"><b>${x.external_id||'—'}</b></td>
        <td><b>${x.recipient_name}</b></td>
        <td style="font-size:12px;color:var(--text2);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${x.address}</td>
        <td>${x.weight_kg} kg</td>'''

new_render = '''function renderOrders(orders) {
  const prioLabel = {1:'Normal',2:'Alta',3:'Urgente'};
  const prioClass = {1:'draft',2:'pending',3:'failed'};

  // Atualiza KPIs rápidos
  const pending   = orders.filter(o=>o.status==='pending').length;
  const routed    = orders.filter(o=>o.status==='routed').length;
  const delivered = orders.filter(o=>o.status==='delivered').length;
  const failed    = orders.filter(o=>o.status==='failed').length;
  const pesoTotal = orders.reduce((s,o)=>s+(o.weight_kg||0),0);
  const el = (id,val) => { const e=document.getElementById(id); if(e) e.textContent=val; };
  el('pk-pendentes', pending);
  el('pk-rota', routed);
  el('pk-entregues', delivered);
  el('pk-falha', failed);
  el('pk-peso', pesoTotal.toFixed(0)+'kg');
  document.getElementById('orders-sub').textContent = `${orders.length} pedidos · ${pesoTotal.toFixed(0)}kg total`;

  // Detecta zona pelo endereço (simplificado)
  function detectaZona(addr) {
    if (!addr) return '—';
    addr = addr.toLowerCase();
    if (addr.includes('tarumã') || addr.includes('cidade nova') || addr.includes('colônia')) return 'Norte';
    if (addr.includes('flores') || addr.includes('aleixo') || addr.includes('adrianópolis')) return 'Leste';
    if (addr.includes('praça 14') || addr.includes('cachoeirinha') || addr.includes('petrópolis')) return 'Sul';
    if (addr.includes('compensa') || addr.includes('lírio') || addr.includes('redenção')) return 'Oeste';
    if (addr.includes('centro') || addr.includes('educandos')) return 'Centro';
    return '—';
  }

  document.getElementById('orders-tbody').innerHTML = orders.length
    ? orders.map(x => `<tr>
        <td><input type="checkbox" class="order-chk" data-id="${x.id}" onchange="toggleOrderChk('${x.id}',this.checked)"></td>
        <td style="font-family:'DM Mono',monospace;font-size:12px"><b>${x.external_id||'—'}</b></td>
        <td><b>${x.recipient_name}</b></td>
        <td style="font-size:12px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${x.address}">${x.address} <span style="font-size:10px;background:#1e3a5c;color:#64B4FF;padding:1px 5px;border-radius:4px;margin-left:4px">${detectaZona(x.address)}</span></td>
        <td><b>${x.weight_kg} kg</b></td>'''

if old_render in content:
    content = content.replace(old_render, new_render)
    print('renderOrders atualizado!')

# Atualiza o final da linha da tabela para incluir botão de detalhe
old_acoes = '''<td>${x.priority||1}</td><td><span class="badge ${x.status}">${x.status}</span></td>
        <td>'''

new_acoes = '''<td style="font-size:11px;color:#90afd4">TOP 1000</td>
        <td style="font-size:11px;color:#90afd4">${x.time_window_start||'—'}</td>
        <td><span class="badge ${x.status}">${x.status}</span></td>
        <td>'''

content = content.replace(old_acoes, new_acoes, 1)

# Atualiza o botão de ação na tabela
old_btn = '''onclick="openModal('order')"'''
# Adiciona botão de detalhe
old_ver = '''<button class="btn btn-sm btn-secondary" onclick="verDetalhesOrder('${x.id}')">Ver</button>'''
new_ver = '''<button class="btn btn-sm btn-secondary" onclick="verDetalhePedido('${x.id}')" title="Ver detalhes">🔍</button>'''
content = content.replace(old_ver, new_ver)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R no navegador.')
