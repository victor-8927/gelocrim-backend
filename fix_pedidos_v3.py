path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Atualiza cabeçalho da tabela de pedidos ─────────────────────
old_thead = '''            <thead>
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
            </thead>'''

new_thead = '''            <thead>
              <tr>
                <th style="width:30px"><input type="checkbox" id="chk-all" onchange="toggleTodosOrders(this.checked)" title="Selecionar todos"></th>
                <th>Nº Pedido</th>
                <th>Cliente</th>
                <th>Endereço / Zona</th>
                <th>Peso (kg)</th>
                <th>Valor (R$)</th>
                <th>TOP</th>
                <th>Janela / Prioridade</th>
                <th>GPS</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>'''

if old_thead in content:
    content = content.replace(old_thead, new_thead)
    print('Cabeçalho da tabela atualizado!')

# ── 2. Atualiza os KPIs rápidos para funcionar como filtros ────────
old_kpis = '''      <!-- KPIs RÁPIDOS DE PEDIDOS -->
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
      </div>'''

new_kpis = '''      <!-- KPIs RÁPIDOS — clicáveis como filtro rápido -->
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:16px" id="pedidos-kpis">
        <div class="card" onclick="filtroRapido('pending')" style="padding:12px;margin-bottom:0;border-left:3px solid #f59e0b;cursor:pointer" title="Filtrar pendentes">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">📦 Pendentes</div>
          <div style="font-size:24px;font-weight:800;color:#f59e0b" id="pk-pendentes">—</div>
          <div style="font-size:10px;color:#90afd4;margin-top:2px">clique para filtrar</div>
        </div>
        <div class="card" onclick="filtroRapido('routed')" style="padding:12px;margin-bottom:0;border-left:3px solid #64B4FF;cursor:pointer" title="Filtrar em rota">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">🚛 Em Rota</div>
          <div style="font-size:24px;font-weight:800;color:#64B4FF" id="pk-rota">—</div>
          <div style="font-size:10px;color:#90afd4;margin-top:2px">clique para filtrar</div>
        </div>
        <div class="card" onclick="filtroRapido('delivered')" style="padding:12px;margin-bottom:0;border-left:3px solid #10b981;cursor:pointer" title="Filtrar entregues">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">✅ Entregues</div>
          <div style="font-size:24px;font-weight:800;color:#10b981" id="pk-entregues">—</div>
          <div style="font-size:10px;color:#90afd4;margin-top:2px">clique para filtrar</div>
        </div>
        <div class="card" onclick="filtroRapido('failed')" style="padding:12px;margin-bottom:0;border-left:3px solid #f87171;cursor:pointer" title="Filtrar com falha">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">❌ Com Falha</div>
          <div style="font-size:24px;font-weight:800;color:#f87171" id="pk-falha">—</div>
          <div style="font-size:10px;color:#90afd4;margin-top:2px">clique para filtrar</div>
        </div>
        <div class="card" style="padding:12px;margin-bottom:0;border-left:3px solid #a78bfa">
          <div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px">⚖️ Peso Total</div>
          <div style="font-size:24px;font-weight:800;color:#a78bfa" id="pk-peso">—</div>
          <div style="font-size:10px;color:#90afd4;margin-top:2px" id="pk-ocupacao">— da frota</div>
        </div>
      </div>

      <!-- BARRA DE CAPACIDADE DA FROTA -->
      <div class="card" style="padding:12px 16px;margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
          <div style="font-size:12px;font-weight:700;color:#e8f0fe">🚛 Ocupação da Frota Disponível</div>
          <div style="font-size:12px;color:#64B4FF;font-weight:600" id="frota-ocupacao-pct">—</div>
        </div>
        <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
          <div id="frota-ocupacao-bar" style="height:100%;background:#64B4FF;border-radius:4px;width:0%;transition:width .4s"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:10px;color:#90afd4">
          <span id="frota-peso-info">Peso total: 0 kg</span>
          <span id="frota-cap-info">Capacidade frota: — kg</span>
        </div>
        <div style="margin-top:6px;font-size:11px;color:#90afd4" id="ultima-sync">Última sincronização: —</div>
      </div>'''

if old_kpis in content:
    content = content.replace(old_kpis, new_kpis)
    print('KPIs com filtro rápido e barra de capacidade adicionados!')

# ── 3. Atualiza renderOrders com todas as melhorias ────────────────
idx = content.find('function renderOrders(orders) {')
if idx != -1:
    depth = 0; started = False; i = idx
    for i in range(idx, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break

    new_render = '''function renderOrders(orders) {
  const prioLabel = {1:'Normal',2:'Alta',3:'Urgente'};
  const prioClass = {1:'draft',2:'pending',3:'failed'};

  // KPIs rápidos
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

  // Barra de capacidade da frota
  api('GET', '/vehicles').then(veics => {
    const capTotal = veics.filter(v=>v.status==='active').reduce((s,v)=>s+(v.capacity_kg||0),0);
    const pct = capTotal > 0 ? Math.min(100, Math.round(pesoTotal/capTotal*100)) : 0;
    const bar = document.getElementById('frota-ocupacao-bar');
    const pctEl = document.getElementById('frota-ocupacao-pct');
    const pesoEl = document.getElementById('frota-peso-info');
    const capEl  = document.getElementById('frota-cap-info');
    const ocupEl = document.getElementById('pk-ocupacao');
    if (bar)  { bar.style.width = pct+'%'; bar.style.background = pct>90?'#f87171':pct>70?'#f59e0b':'#64B4FF'; }
    if (pctEl) pctEl.textContent = pct+'% ocupado';
    if (pesoEl) pesoEl.textContent = `Peso total: ${pesoTotal.toFixed(0)} kg`;
    if (capEl)  capEl.textContent  = `Capacidade frota: ${capTotal.toFixed(0)} kg`;
    if (ocupEl) ocupEl.textContent = `${pct}% da frota`;
  }).catch(()=>{});

  // Última sincronização
  const syncEl = document.getElementById('ultima-sync');
  if (syncEl) syncEl.textContent = `Última sincronização: ${new Date().toLocaleTimeString('pt-BR')}`;

  // Detecta zona
  function detectaZona(addr) {
    if (!addr) return '—';
    addr = addr.toLowerCase();
    if (addr.includes('tarumã')||addr.includes('cidade nova')||addr.includes('colônia')) return 'Norte';
    if (addr.includes('flores')||addr.includes('aleixo')||addr.includes('adrianópolis')) return 'Leste';
    if (addr.includes('praça 14')||addr.includes('cachoeirinha')||addr.includes('petrópolis')) return 'Sul';
    if (addr.includes('compensa')||addr.includes('lírio')||addr.includes('redenção')) return 'Oeste';
    if (addr.includes('centro')||addr.includes('educandos')) return 'Centro';
    return '—';
  }

  // Detecta cliente crítico (grandes redes)
  function isClienteCritico(nome) {
    const redes = ['assai','assaí','db','nova era','atacadão','carrefour','wallmart','supermercado'];
    return redes.some(r => (nome||'').toLowerCase().includes(r));
  }

  // Ícone GPS
  function gpsIcon(lat, lng) {
    if (lat && lng && Math.abs(parseFloat(lat)) > 0.01)
      return '<span title="Geolocalizado" style="color:#10b981;font-size:14px">📍</span>';
    return '<span title="Sem GPS — não será roteirizado" style="color:#f87171;font-size:14px">📍</span>';
  }

  // TOP label
  function topLabel(top) {
    const tops = {'1000':'1000 Venda','1007':'1007 Bonif.','1008':'1008 Consig.','1009':'1009 Troca','1010':'1010 Pré-ped.'};
    return tops[top] || (top ? `TOP ${top}` : '—');
  }

  document.getElementById('orders-tbody').innerHTML = orders.length
    ? orders.map(x => {
        const critico = isClienteCritico(x.recipient_name);
        const rowStyle = critico ? 'background:rgba(232,82,26,.05);' : '';
        const tooltip = `title="Pedido: ${x.external_id||'—'}\nPeso: ${x.weight_kg||0}kg\nVolume: ${x.volume_m3||0}m³\nPrioridade: ${prioLabel[x.priority||1]}"`;
        return `<tr style="${rowStyle}">
          <td><input type="checkbox" class="order-chk" data-id="${x.id}" onchange="toggleOrderChk('${x.id}',this.checked)"></td>
          <td style="font-family:monospace;font-size:11px" ${tooltip}>
            <b style="cursor:help;border-bottom:1px dashed #1e3a5c">${x.external_id||'—'}</b>
            ${critico ? '<span title="Grande rede — prioridade especial" style="margin-left:4px;font-size:10px">⭐</span>' : ''}
          </td>
          <td>
            <b style="color:${critico?'#f59e0b':'#e8f0fe'}">${x.recipient_name}</b>
            ${critico ? '<div style="font-size:9px;color:#f59e0b">Grande Rede</div>' : ''}
          </td>
          <td style="font-size:12px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${x.address}">
            ${x.address||'—'}
            <span style="font-size:10px;background:#1e3a5c;color:#64B4FF;padding:1px 5px;border-radius:4px;margin-left:4px">${detectaZona(x.address)}</span>
          </td>
          <td>
            <b>${x.weight_kg||0} kg</b>
            <div style="font-size:10px;color:#90afd4">${x.volume_m3||0} m³</div>
          </td>
          <td style="color:#10b981;font-weight:600">
            ${x.total_value ? 'R$ '+parseFloat(x.total_value).toFixed(2) : '<span style="color:#90afd4">—</span>'}
          </td>
          <td>
            <span style="font-size:11px;background:#1e3a5c;color:#a78bfa;padding:2px 6px;border-radius:4px">${topLabel(x.top||x.order_type)}</span>
          </td>
          <td style="font-size:11px">
            <div style="color:#e8f0fe">${x.time_window_start||'—'} - ${x.time_window_end||'—'}</div>
            <span class="badge ${prioClass[x.priority||1]}" style="font-size:9px">${prioLabel[x.priority||1]}</span>
          </td>
          <td style="text-align:center">${gpsIcon(x.lat,x.lng)}</td>
          <td><span class="badge ${x.status}">${x.status}</span></td>
          <td style="display:flex;gap:4px">
            <button class="btn btn-sm btn-secondary" onclick="verDetalhePedido('${x.id}')" title="Ver detalhes">🔍</button>
          </td>
        </tr>`;
      }).join('')
    : '<tr><td colspan="11" class="loading-state">Nenhum pedido encontrado</td></tr>';
}

// Filtro rápido por status via card KPI
function filtroRapido(status) {
  const sel = document.getElementById('f-status');
  if (sel) { sel.value = status; loadOrders(); }
}'''

    content = content[:idx] + new_render + content[i+1:]
    print('renderOrders atualizado com todas as melhorias!')

# ── 4. Atualiza ações em lote ──────────────────────────────────────
old_lote = '''        <div id="orders-acoes-lote" style="display:none;padding:10px 16px;background:#0a1628;border-top:1px solid #1e3a5c;display:none;align-items:center;gap:10px">
          <span id="orders-selecionados" style="font-size:13px;color:#90afd4"></span>
          <button class="btn btn-sm btn-primary" onclick="adicionarSelecionadosRota()">➕ Adicionar à Rota</button>
          <button class="btn btn-sm btn-secondary" onclick="limparSelecaoOrders()">✕ Limpar seleção</button>
        </div>'''

new_lote = '''        <div id="orders-acoes-lote" style="display:none;padding:10px 16px;background:#0a1628;border-top:1px solid #1e3a5c;align-items:center;gap:10px;flex-wrap:wrap">
          <span id="orders-selecionados" style="font-size:13px;color:#90afd4"></span>
          <button class="btn btn-sm btn-primary" onclick="adicionarSelecionadosRota()">⚡ Roteirizar Selecionados</button>
          <button class="btn btn-sm btn-secondary" onclick="alterarPrioridadeLote(2)">🟡 Prioridade Alta</button>
          <button class="btn btn-sm btn-secondary" onclick="alterarPrioridadeLote(3)">🔴 Urgente</button>
          <button class="btn btn-sm btn-secondary" style="color:#f87171" onclick="cancelarAlocacaoLote()">✕ Cancelar Alocação</button>
          <button class="btn btn-sm btn-secondary" onclick="limparSelecaoOrders()">Limpar seleção</button>
        </div>'''

if old_lote in content:
    content = content.replace(old_lote, new_lote)
    print('Ações em lote atualizadas!')

# ── 5. Adiciona funções de ações em lote ──────────────────────────
new_funcs = '''
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

'''

if 'function alterarPrioridadeLote' not in content:
    content = content.replace('function limparSelecaoOrders()', new_funcs + 'function limparSelecaoOrders()')
    print('Funções de lote adicionadas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
