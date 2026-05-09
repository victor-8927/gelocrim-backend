"""
update_selecao_pedidos.py
Atualiza a tela de Roteirização com seleção manual de pedidos por veículo.
"""

html_path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Nova seção de roteirização com seleção manual
new_roteirizacao_html = '''
<!-- TELA ROTEIRIZAÇÃO -->
<div id="page-roteirizacao" class="page" style="display:none">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:12px">
    <div>
      <h2 style="margin:0;font-size:20px;font-weight:700">⚡ Roteirização</h2>
      <p style="margin:4px 0 0;color:var(--muted);font-size:13px">Selecione o veículo e os pedidos para roteirizar</p>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <input type="date" id="opt-date" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px">
      <button class="btn btn-secondary" onclick="loadPreSummary()">↺ Atualizar</button>
    </div>
  </div>

  <!-- PASSO 1: SELECIONAR VEÍCULO -->
  <div class="card" style="margin-bottom:16px">
    <div class="card-header">
      <span class="card-title">🚛 Passo 1 — Selecione o Veículo</span>
    </div>
    <div class="card-body" style="padding:16px">
      <div id="lista-veiculos-rot" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px">
        <div style="color:var(--muted);font-size:13px">Carregando veículos...</div>
      </div>
    </div>
  </div>

  <!-- BARRA DE CAPACIDADE -->
  <div id="barra-capacidade" class="card" style="margin-bottom:16px;display:none">
    <div class="card-body" style="padding:16px">
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:12px">
        <span id="veiculo-selecionado-nome" style="font-weight:700;font-size:15px"></span>
        <span id="contador-pedidos-sel" style="background:var(--primary);color:#fff;padding:2px 10px;border-radius:10px;font-size:12px;font-weight:600">0 pedidos</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px">
            <span>⚖️ Peso</span>
            <span id="peso-usado-txt">0 / 0 kg</span>
          </div>
          <div style="background:#e5e7eb;border-radius:6px;height:12px;overflow:hidden">
            <div id="barra-peso" style="height:100%;background:#e8521a;border-radius:6px;transition:width .3s;width:0%"></div>
          </div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px">
            <span>📦 Volume</span>
            <span id="vol-usado-txt">0 / 0 m³</span>
          </div>
          <div style="background:#e5e7eb;border-radius:6px;height:12px;overflow:hidden">
            <div id="barra-vol" style="height:100%;background:#2563eb;border-radius:6px;transition:width .3s;width:0%"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- PASSO 2: SELECIONAR PEDIDOS -->
  <div id="card-pedidos-rot" class="card" style="margin-bottom:16px;display:none">
    <div class="card-header">
      <span class="card-title">📦 Passo 2 — Selecione os Pedidos</span>
      <div style="display:flex;gap:8px">
        <button class="btn btn-secondary btn-sm" onclick="selecionarTodosPedidos()">Selecionar Todos</button>
        <button class="btn btn-secondary btn-sm" onclick="limparSelecao()">Limpar</button>
        <input type="text" id="busca-pedidos-rot" placeholder="Buscar cliente..." onkeyup="filtrarPedidosRot()" 
          style="padding:4px 10px;border:1px solid var(--border);border-radius:6px;font-size:12px;width:160px">
      </div>
    </div>
    <div class="card-body" style="padding:0;max-height:420px;overflow-y:auto">
      <table style="width:100%;border-collapse:collapse;font-size:12px">
        <thead style="position:sticky;top:0;z-index:1">
          <tr style="background:#f8fafc;border-bottom:2px solid var(--border)">
            <th style="padding:10px 12px;text-align:center;width:40px">
              <input type="checkbox" id="chk-todos" onchange="toggleTodos(this)">
            </th>
            <th style="padding:10px 12px;text-align:left">Pedido</th>
            <th style="padding:10px 12px;text-align:left">Cliente</th>
            <th style="padding:10px 12px;text-align:left">Endereço</th>
            <th style="padding:10px 12px;text-align:right">Peso (kg)</th>
            <th style="padding:10px 12px;text-align:right">Vol (m³)</th>
            <th style="padding:10px 12px;text-align:center">Janela</th>
          </tr>
        </thead>
        <tbody id="tbody-pedidos-rot"></tbody>
      </table>
    </div>
  </div>

  <!-- PASSO 3: ROTEIRIZAR -->
  <div id="card-roteirizar" style="display:none;margin-bottom:16px">
    <button id="btn-optimize" onclick="optimizeRoutes()"
      style="width:100%;padding:16px;background:#e8521a;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px">
      ⚡ Roteirizar Pedidos Selecionados
    </button>
  </div>

  <div id="optimize-result"></div>
</div>
'''

# JavaScript da nova tela
new_js = '''
// ── ROTEIRIZAÇÃO COM SELEÇÃO MANUAL ──────────────────────────────
let veiculoSelecionado = null;
let pedidosDisponiveis = [];
let pedidosSelecionados = new Set();

async function loadPreSummary() {
  const today = new Date().toISOString().slice(0,10);
  if (!document.getElementById('opt-date').value)
    document.getElementById('opt-date').value = today;

  await carregarVeiculosRot();
  await carregarPedidosRot();
}

async function carregarVeiculosRot() {
  try {
    const veiculos = await api('GET', '/vehicles');
    const ativos = veiculos.filter(v => v.status === 'active');
    const container = document.getElementById('lista-veiculos-rot');
    if (!ativos.length) {
      container.innerHTML = '<div class="alert warn">Nenhum veículo ativo.</div>';
      return;
    }
    container.innerHTML = ativos.map(v => `
      <div id="vcard-${v.id}" onclick="selecionarVeiculo('${v.id}','${v.plate}','${v.model}',${v.capacity_kg},${v.capacity_m3})"
        style="border:2px solid var(--border);border-radius:8px;padding:12px;cursor:pointer;transition:all .2s">
        <div style="font-weight:700;font-size:13px;margin-bottom:4px">🚛 ${v.plate}</div>
        <div style="font-size:11px;color:var(--muted)">${v.model}</div>
        <div style="display:flex;gap:8px;margin-top:8px;font-size:11px">
          <span style="background:#fff7ed;color:#d97706;padding:2px 8px;border-radius:4px">⚖️ ${v.capacity_kg} kg</span>
          <span style="background:#eff6ff;color:#2563eb;padding:2px 8px;border-radius:4px">📦 ${v.capacity_m3} m³</span>
        </div>
      </div>`).join('');
  } catch(e) { toast(e.message,'error'); }
}

function selecionarVeiculo(id, plate, model, capKg, capM3) {
  veiculoSelecionado = {id, plate, model, capKg, capM3};
  pedidosSelecionados.clear();

  // Destaca veículo selecionado
  document.querySelectorAll('[id^="vcard-"]').forEach(el => {
    el.style.border = '2px solid var(--border)';
    el.style.background = '';
  });
  const card = document.getElementById(`vcard-${id}`);
  if (card) {
    card.style.border = '2px solid #e8521a';
    card.style.background = '#fff7ed';
  }

  // Mostra barra de capacidade
  document.getElementById('barra-capacidade').style.display = 'block';
  document.getElementById('card-pedidos-rot').style.display = 'block';
  document.getElementById('veiculo-selecionado-nome').textContent = `${plate} — ${model}`;
  atualizarBarraCapacidade();
  renderizarPedidosRot();
}

async function carregarPedidosRot() {
  try {
    const orders = await api('GET', '/orders?status=pending&limit=500');
    pedidosDisponiveis = orders;
    if (veiculoSelecionado) renderizarPedidosRot();
  } catch(e) { toast(e.message,'error'); }
}

function renderizarPedidosRot() {
  const tbody = document.getElementById('tbody-pedidos-rot');
  const busca = document.getElementById('busca-pedidos-rot')?.value.toLowerCase() || '';
  const filtrados = pedidosDisponiveis.filter(o =>
    !busca || o.recipient_name.toLowerCase().includes(busca) ||
    (o.external_id||'').toLowerCase().includes(busca)
  );

  tbody.innerHTML = filtrados.map(o => {
    const sel = pedidosSelecionados.has(o.id);
    const peso = (o.weight_kg||0).toFixed(0);
    const vol = (o.volume_m3||0).toFixed(2);
    return `
    <tr id="row-${o.id}" style="${sel?'background:#fff7ed':''}" onclick="togglePedido('${o.id}',${o.weight_kg||0},${o.volume_m3||0})">
      <td style="padding:8px 12px;text-align:center">
        <input type="checkbox" ${sel?'checked':''} onchange="togglePedido('${o.id}',${o.weight_kg||0},${o.volume_m3||0})" onclick="event.stopPropagation()">
      </td>
      <td style="padding:8px 12px;font-family:monospace;font-size:11px;color:var(--muted)">${o.external_id||o.id.slice(0,8)}</td>
      <td style="padding:8px 12px;font-weight:600;font-size:12px">${o.recipient_name}</td>
      <td style="padding:8px 12px;font-size:11px;color:var(--muted)">${o.address||''}</td>
      <td style="padding:8px 12px;text-align:right;font-weight:600;color:#d97706">${peso}</td>
      <td style="padding:8px 12px;text-align:right;color:#2563eb">${vol}</td>
      <td style="padding:8px 12px;text-align:center;font-size:11px">${o.tw_start||'07:30'}–${o.tw_end||'18:00'}</td>
    </tr>`;
  }).join('');
}

function togglePedido(id, peso, vol) {
  if (!veiculoSelecionado) { toast('Selecione um veículo primeiro!','warn'); return; }

  if (pedidosSelecionados.has(id)) {
    pedidosSelecionados.delete(id);
  } else {
    // Verifica capacidade
    const totPeso = getPesoSelecionado() + peso;
    const totVol = getVolSelecionado() + vol;
    if (totPeso > veiculoSelecionado.capKg) {
      toast(`⚖️ Peso excede capacidade! (${totPeso.toFixed(0)} / ${veiculoSelecionado.capKg} kg)`,'warn');
      return;
    }
    if (veiculoSelecionado.capM3 > 0 && totVol > veiculoSelecionado.capM3) {
      toast(`📦 Volume excede capacidade! (${totVol.toFixed(2)} / ${veiculoSelecionado.capM3} m³)`,'warn');
      return;
    }
    pedidosSelecionados.add(id);
  }

  atualizarBarraCapacidade();
  renderizarPedidosRot();
  document.getElementById('card-roteirizar').style.display =
    pedidosSelecionados.size > 0 ? 'block' : 'none';
}

function getPesoSelecionado() {
  return pedidosDisponiveis
    .filter(o => pedidosSelecionados.has(o.id))
    .reduce((s,o) => s + (o.weight_kg||0), 0);
}

function getVolSelecionado() {
  return pedidosDisponiveis
    .filter(o => pedidosSelecionados.has(o.id))
    .reduce((s,o) => s + (o.volume_m3||0), 0);
}

function atualizarBarraCapacidade() {
  if (!veiculoSelecionado) return;
  const peso = getPesoSelecionado();
  const vol = getVolSelecionado();
  const pct_peso = Math.min(100, (peso / veiculoSelecionado.capKg) * 100);
  const pct_vol = veiculoSelecionado.capM3 > 0 ?
    Math.min(100, (vol / veiculoSelecionado.capM3) * 100) : 0;

  document.getElementById('barra-peso').style.width = pct_peso + '%';
  document.getElementById('barra-peso').style.background = pct_peso > 90 ? '#dc2626' : '#e8521a';
  document.getElementById('peso-usado-txt').textContent = `${peso.toFixed(0)} / ${veiculoSelecionado.capKg} kg`;

  document.getElementById('barra-vol').style.width = pct_vol + '%';
  document.getElementById('vol-usado-txt').textContent = `${vol.toFixed(2)} / ${veiculoSelecionado.capM3} m³`;

  document.getElementById('contador-pedidos-sel').textContent = `${pedidosSelecionados.size} pedidos selecionados`;
}

function selecionarTodosPedidos() {
  if (!veiculoSelecionado) { toast('Selecione um veículo primeiro!','warn'); return; }
  let totPeso = 0, totVol = 0;
  pedidosSelecionados.clear();
  for (const o of pedidosDisponiveis) {
    if (totPeso + (o.weight_kg||0) <= veiculoSelecionado.capKg) {
      pedidosSelecionados.add(o.id);
      totPeso += o.weight_kg||0;
      totVol += o.volume_m3||0;
    }
  }
  atualizarBarraCapacidade();
  renderizarPedidosRot();
  document.getElementById('card-roteirizar').style.display = 'block';
  toast(`${pedidosSelecionados.size} pedidos selecionados automaticamente!`);
}

function limparSelecao() {
  pedidosSelecionados.clear();
  atualizarBarraCapacidade();
  renderizarPedidosRot();
  document.getElementById('card-roteirizar').style.display = 'none';
}

function toggleTodos(chk) {
  if (chk.checked) selecionarTodosPedidos();
  else limparSelecao();
}

function filtrarPedidosRot() {
  renderizarPedidosRot();
}

async function optimizeRoutes() {
  if (!veiculoSelecionado) { toast('Selecione um veículo!','warn'); return; }
  if (pedidosSelecionados.size === 0) { toast('Selecione pelo menos um pedido!','warn'); return; }

  const btn = document.getElementById('btn-optimize');
  const result = document.getElementById('optimize-result');
  btn.disabled = true;
  btn.innerHTML = '⏳ Roteirizando...';

  result.innerHTML = `<div class="alert info" style="margin-top:16px">
    ⏳ Motor V2 calculando rota para ${veiculoSelecionado.plate} com ${pedidosSelecionados.size} pedidos...
  </div>`;

  try {
    const d = await api('POST', '/routes/optimize', {
      route_date: document.getElementById('opt-date').value,
      vehicle_ids: [veiculoSelecionado.id],
      order_ids: Array.from(pedidosSelecionados),
      time_limit_sec: 30,
      reoptimize: false,
    });

    const routeColors = ['#e8521a','#2563eb','#16a34a','#d97706','#7c3aed'];
    result.innerHTML = `
      <div class="card" style="margin-top:16px">
        <div class="card-header" style="background:#f0fdf4">
          <span class="card-title" style="color:#16a34a">✅ Rota Criada!</span>
          <span style="font-size:12px;color:var(--muted)">${(d.wall_time_ms/1000).toFixed(1)}s</span>
        </div>
        <div class="card-body" style="padding:16px">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:16px">
            <div style="background:#f0fdf4;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:24px;font-weight:700;color:#16a34a">${d.routes_created}</div>
              <div style="font-size:11px;color:#16a34a;font-weight:600">ROTAS</div>
            </div>
            <div style="background:#eff6ff;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:24px;font-weight:700;color:#2563eb">${d.total_stops}</div>
              <div style="font-size:11px;color:#2563eb;font-weight:600">PARADAS</div>
            </div>
            <div style="background:#fff7ed;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:24px;font-weight:700;color:#d97706">${d.routes.reduce((s,r)=>s+(r.total_distance_km||0),0).toFixed(1)} km</div>
              <div style="font-size:11px;color:#d97706;font-weight:600">DISTÂNCIA</div>
            </div>
            <div style="background:#fef9c3;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:24px;font-weight:700;color:#ca8a04">${d.unassigned_orders.length}</div>
              <div style="font-size:11px;color:#ca8a04;font-weight:600">NÃO ALOCADOS</div>
            </div>
          </div>

          ${d.routes.map((r,idx) => {
            const color = routeColors[idx % routeColors.length];
            return `
            <div style="border:2px solid ${color}30;border-radius:10px;overflow:hidden;margin-bottom:12px">
              <div style="background:${color}10;padding:12px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap">
                <span style="background:${color};color:#fff;padding:4px 14px;border-radius:6px;font-weight:700">${r.vehicle_plate}</span>
                <span style="font-size:12px">🕐 Saída: <b>07:30</b></span>
                <span style="font-size:12px">🏁 Chegada: <b>${r.planned_end}</b></span>
                <span style="font-size:12px">📍 <b>${r.total_stops}</b> paradas</span>
                <span style="font-size:12px">🛣️ <b>${r.total_distance_km}</b> km</span>
                ${r.score ? `<span style="font-size:12px;color:#16a34a">⭐ <b>${r.score}/10</b></span>` : ''}
              </div>
              <table style="width:100%;font-size:12px">
                <thead><tr style="background:#f8fafc">
                  <th style="padding:8px 12px;text-align:left;font-size:10px;color:var(--muted)">SEQ</th>
                  <th style="padding:8px 12px;text-align:left;font-size:10px;color:var(--muted)">ETA</th>
                  <th style="padding:8px 12px;text-align:left;font-size:10px;color:var(--muted)">CLIENTE</th>
                  <th style="padding:8px 12px;text-align:left;font-size:10px;color:var(--muted)">ENDEREÇO</th>
                  <th style="padding:8px 12px;text-align:right;font-size:10px;color:var(--muted)">PESO</th>
                </tr></thead>
                <tbody>${r.stops.map((s,si) => `
                  <tr style="background:${si%2===0?'#fff':'#fafafa'}">
                    <td style="padding:8px 12px">
                      <span style="background:${color};color:#fff;width:22px;height:22px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700">${s.sequence+1}</span>
                    </td>
                    <td style="padding:8px 12px;font-family:monospace;color:#2563eb;font-weight:600">${s.eta}</td>
                    <td style="padding:8px 12px;font-weight:600">${s.recipient_name}</td>
                    <td style="padding:8px 12px;font-size:11px;color:var(--muted)">${s.address}</td>
                    <td style="padding:8px 12px;text-align:right;font-size:11px">${s.weight_kg||0} kg</td>
                  </tr>`).join('')}
                </tbody>
              </table>
            </div>`;
          }).join('')}

          ${d.unassigned_orders.length ? `
          <div class="alert warn">⚠️ ${d.unassigned_orders.length} pedido(s) não alocado(s)</div>` : 
          '<div class="alert" style="background:#f0fdf4;border:1px solid #bbf7d0;color:#16a34a">✅ Todos os pedidos alocados!</div>'}
        </div>
      </div>`;

    toast(`✅ Rota criada para ${veiculoSelecionado.plate}!`);
    pedidosSelecionados.clear();
    atualizarBarraCapacidade();
    await carregarPedidosRot();
    loadRoutes();

  } catch(e) {
    result.innerHTML = `<div class="alert danger" style="margin-top:16px">❌ ${e.message}</div>`;
    toast(e.message,'error');
  }
  btn.disabled = false;
  btn.innerHTML = '⚡ Roteirizar Pedidos Selecionados';
}
'''

# Substitui a seção de roteirização no HTML
old_marker = 'id="page-roteirizacao"'
if old_marker in content:
    # Encontra o início e fim da div da página
    start = content.find('<div id="page-roteirizacao"')
    # Encontra o próximo page div para delimitar
    end = content.find('<div id="page-rotas"', start)
    if end == -1:
        end = content.find('<!-- ROTAS -->', start)
    if start != -1 and end != -1:
        content = content[:start] + new_roteirizacao_html + '\n\n' + content[end:]
        print('✅ Seção de roteirização substituída!')
    else:
        print('⚠️  Não encontrou o fim da seção. Adicionando JS apenas.')
else:
    print('⚠️  Seção de roteirização não encontrada no HTML')

# Adiciona o JavaScript antes do </script> final ou antes de </body>
if 'async function optimizeRoutes()' in content:
    # Remove a função antiga
    start_func = content.find('async function optimizeRoutes()')
    end_func = content.find('\nasync function ', start_func + 1)
    if end_func == -1:
        end_func = content.find('\nfunction ', start_func + 1)
    if end_func != -1:
        content = content[:start_func] + content[end_func:]
        print('✅ Função optimizeRoutes antiga removida!')

# Injeta o novo JS
inject_marker = '</script>'
last_script = content.rfind(inject_marker)
if last_script != -1:
    content = content[:last_script] + new_js + '\n' + content[last_script:]
    print('✅ Novo JavaScript injetado!')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n🎉 Tela de seleção de pedidos criada!')
print('Faça Ctrl+Shift+R no navegador para ver as mudanças.')
