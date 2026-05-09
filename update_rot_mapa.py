path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('<div class="page" id="page-roteirizacao">')
end   = content.find('<div class="page" id="page-rotas">')

if start == -1 or end == -1:
    print(f'Secao nao encontrada: start={start}, end={end}')
    exit(1)

new_section = '''<div class="page" id="page-roteirizacao">
  <div class="page-header" style="margin-bottom:12px">
    <div>
      <div class="page-title">&#x26A1; Roteirizacao Visual</div>
      <div class="page-sub">Selecione clientes no mapa e roteirize</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <input type="date" id="opt-date" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px">
      <select id="rot-veiculo-select" onchange="rotVeiculoChanged()"
        style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px;min-width:200px">
        <option value="">-- Selecione o Veiculo --</option>
      </select>
      <button class="btn btn-secondary" onclick="loadRotMapData()">&#8635; Atualizar</button>
    </div>
  </div>

  <!-- LAYOUT PRINCIPAL: SIDEBAR + MAPA -->
  <div style="display:flex;gap:12px;height:calc(100vh - 200px);min-height:500px">

    <!-- SIDEBAR ESQUERDA -->
    <div style="width:320px;flex-shrink:0;display:flex;flex-direction:column;gap:8px">

      <!-- Capacidade do veiculo -->
      <div class="card" style="flex-shrink:0">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:12px;margin-bottom:8px;color:var(--muted)">CAPACIDADE DO VEICULO</div>
          <div id="rot-cap-info" style="font-size:12px;color:var(--muted);text-align:center">Selecione um veiculo</div>
          <div id="rot-barras" style="display:none">
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span>&#x2696;&#xFE0F; Peso</span><span id="rot-peso-txt" style="font-weight:600">0 kg</span>
              </div>
              <div style="background:#e5e7eb;border-radius:4px;height:10px;overflow:hidden">
                <div id="rot-barra-peso" style="height:100%;background:#e8521a;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <div>
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span>&#x1F4E6; Volume</span><span id="rot-vol-txt" style="font-weight:600">0 m3</span>
              </div>
              <div style="background:#e5e7eb;border-radius:4px;height:10px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ferramentas de selecao -->
      <div class="card" style="flex-shrink:0">
        <div class="card-body" style="padding:12px">
          <div style="font-weight:700;font-size:12px;margin-bottom:8px;color:var(--muted)">MODO DE SELECAO</div>
          <div style="display:flex;gap:6px">
            <button id="btn-modo-click" onclick="setModoSelecao('click')"
              style="flex:1;padding:8px;border:2px solid #e8521a;background:#fff7ed;color:#e8521a;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">
              &#x1F4CC; Individual
            </button>
            <button id="btn-modo-area" onclick="setModoSelecao('area')"
              style="flex:1;padding:8px;border:2px solid var(--border);background:#fff;color:var(--muted);border-radius:6px;font-size:11px;font-weight:700;cursor:pointer">
              &#x270F;&#xFE0F; Desenhar Area
            </button>
          </div>
          <div id="dica-modo" style="font-size:10px;color:var(--muted);margin-top:6px;text-align:center">
            Clique nos pins para selecionar clientes
          </div>
        </div>
      </div>

      <!-- Lista de selecionados -->
      <div class="card" style="flex:1;overflow:hidden;display:flex;flex-direction:column">
        <div class="card-header" style="flex-shrink:0;padding:10px 12px">
          <span class="card-title" style="font-size:12px">SELECIONADOS (<span id="rot-count">0</span>)</span>
          <button onclick="rotLimparTudo()" style="font-size:10px;color:var(--danger);background:none;border:none;cursor:pointer">Limpar</button>
        </div>
        <div id="rot-lista-sel" style="flex:1;overflow-y:auto;padding:8px">
          <div style="color:var(--muted);font-size:12px;text-align:center;padding:20px">
            Nenhum cliente selecionado.<br>Clique nos pins do mapa.
          </div>
        </div>
      </div>

      <!-- Botao roteirizar -->
      <button id="btn-rot-map" onclick="roteirizarDoMapa()" disabled
        style="padding:14px;background:#e8521a;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;opacity:0.5;transition:opacity .2s">
        &#x26A1; Roteirizar Selecionados
      </button>
    </div>

    <!-- MAPA -->
    <div style="flex:1;display:flex;flex-direction:column;gap:8px">
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:12px">
        <span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:12px;background:#e8521a;border-radius:50%;display:inline-block"></span>Pendente</span>
        <span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:12px;background:#16a34a;border-radius:50%;display:inline-block"></span>Selecionado</span>
        <span style="display:flex;align-items:center;gap:4px"><span style="width:12px;height:12px;background:#2563eb;border-radius:50%;display:inline-block"></span>Roteirizado</span>
        <span id="rot-map-status" style="margin-left:auto;color:var(--muted)">Carregando...</span>
      </div>
      <div id="rot-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid var(--border);min-height:400px"></div>
    </div>
  </div>

  <!-- RESULTADO DA ROTEIRIZACAO -->
  <div id="optimize-result" style="margin-top:16px"></div>
</div>

'''

content = content[:start] + new_section + content[end:]

# Injeta o JavaScript
new_js = '''
// ── ROTEIRIZACAO VISUAL NO MAPA ──────────────────────────────────
let rotMap = null;
let rotMarkers = {};
let rotSelecionados = {};  // id -> {order, marker}
let rotVeiculo = null;
let rotModo = 'click';
let rotDrawingManager = null;
let rotPedidosTodos = [];

async function loadRotMapData() {
  const today = new Date().toISOString().slice(0,10);
  if (!document.getElementById('opt-date').value)
    document.getElementById('opt-date').value = today;

  await carregarVeiculosSelect();
  await carregarPedidosMapa();
}

async function carregarVeiculosSelect() {
  try {
    const veiculos = await api('GET', '/vehicles');
    const sel = document.getElementById('rot-veiculo-select');
    sel.innerHTML = '<option value="">-- Selecione o Veiculo --</option>';
    veiculos.filter(v => v.status === 'active').forEach(v => {
      sel.innerHTML += `<option value="${v.id}" data-kg="${v.capacity_kg}" data-m3="${v.capacity_m3}" data-plate="${v.plate}" data-model="${v.model}">
        ${v.plate} — ${v.model} (${v.capacity_kg}kg / ${v.capacity_m3}m3)
      </option>`;
    });
  } catch(e) { toast(e.message,'error'); }
}

function rotVeiculoChanged() {
  const sel = document.getElementById('rot-veiculo-select');
  const opt = sel.options[sel.selectedIndex];
  if (!opt.value) { rotVeiculo = null; return; }
  rotVeiculo = {
    id: opt.value,
    plate: opt.dataset.plate,
    model: opt.dataset.model,
    capKg: parseFloat(opt.dataset.kg),
    capM3: parseFloat(opt.dataset.m3),
  };
  document.getElementById('rot-barras').style.display = 'block';
  document.getElementById('rot-cap-info').style.display = 'none';
  rotAtualizarBarras();
}

async function carregarPedidosMapa() {
  try {
    document.getElementById('rot-map-status').textContent = 'Carregando pedidos...';
    const orders = await api('GET', '/orders?status=pending&limit=500');
    rotPedidosTodos = orders.filter(o => o.lat && o.lng && Math.abs(parseFloat(o.lat)) > 0.01);

    // Inicializa mapa
    if (!rotMap) {
      const el = document.getElementById('rot-map');
      if (typeof google !== 'undefined') {
        rotMap = new google.maps.Map(el, {
          center: {lat: -3.1019, lng: -60.0250},
          zoom: 12,
          mapTypeId: 'roadmap',
        });
        // Depósito
        new google.maps.Marker({
          position: {lat: -3.1019, lng: -60.0250},
          map: rotMap,
          title: 'Deposito Gelocrim',
          icon: {path: google.maps.SymbolPath.CIRCLE, scale:12, fillColor:'#1a1d23', fillOpacity:1, strokeColor:'#fff', strokeWeight:2}
        });
      } else {
        el.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--muted)">Google Maps nao disponivel</div>';
        return;
      }
    }

    // Limpa marcadores antigos
    Object.values(rotMarkers).forEach(m => m.setMap(null));
    rotMarkers = {};
    rotSelecionados = {};
    rotAtualizarSidebar();

    // Adiciona marcadores
    rotPedidosTodos.forEach(o => {
      const lat = parseFloat(o.lat), lng = parseFloat(o.lng);
      const marker = new google.maps.Marker({
        position: {lat, lng},
        map: rotMap,
        title: o.recipient_name,
        icon: rotIcone('#e8521a'),
      });
      marker.addListener('click', () => rotTogglePedido(o, marker));
      rotMarkers[o.id] = marker;
    });

    document.getElementById('rot-map-status').textContent = `${rotPedidosTodos.length} pedidos no mapa`;
    toast(`${rotPedidosTodos.length} pedidos carregados!`);
  } catch(e) {
    document.getElementById('rot-map-status').textContent = 'Erro ao carregar';
    toast(e.message,'error');
  }
}

function rotIcone(color, size=10) {
  return {path: google.maps.SymbolPath.CIRCLE, scale: size, fillColor: color, fillOpacity: 1, strokeColor: '#fff', strokeWeight: 2};
}

function rotTogglePedido(order, marker) {
  if (rotModo !== 'click') return;
  if (rotSelecionados[order.id]) {
    // Deselecionar
    delete rotSelecionados[order.id];
    marker.setIcon(rotIcone('#e8521a'));
  } else {
    // Verificar capacidade
    if (!rotVeiculo) { toast('Selecione um veiculo primeiro!','warn'); return; }
    const totPeso = rotGetPesoTotal() + (order.weight_kg||0);
    const totVol  = rotGetVolTotal() + (order.volume_m3||0);
    if (totPeso > rotVeiculo.capKg) {
      toast(`Peso excede capacidade! (${totPeso.toFixed(0)} / ${rotVeiculo.capKg} kg)`,'warn');
      return;
    }
    rotSelecionados[order.id] = {order, marker};
    marker.setIcon(rotIcone('#16a34a', 12));
  }
  rotAtualizarSidebar();
  rotAtualizarBarras();
}

function rotGetPesoTotal() {
  return Object.values(rotSelecionados).reduce((s,{order}) => s+(order.weight_kg||0), 0);
}
function rotGetVolTotal() {
  return Object.values(rotSelecionados).reduce((s,{order}) => s+(order.volume_m3||0), 0);
}

function rotAtualizarBarras() {
  if (!rotVeiculo) return;
  const peso = rotGetPesoTotal();
  const vol  = rotGetVolTotal();
  const pctP = Math.min(100, (peso/rotVeiculo.capKg)*100);
  const pctV = rotVeiculo.capM3 > 0 ? Math.min(100, (vol/rotVeiculo.capM3)*100) : 0;

  document.getElementById('rot-barra-peso').style.width = pctP+'%';
  document.getElementById('rot-barra-peso').style.background = pctP>90?'#dc2626':'#e8521a';
  document.getElementById('rot-peso-txt').textContent = `${peso.toFixed(0)} / ${rotVeiculo.capKg} kg`;
  document.getElementById('rot-barra-vol').style.width = pctV+'%';
  document.getElementById('rot-vol-txt').textContent = `${vol.toFixed(2)} / ${rotVeiculo.capM3} m3`;
}

function rotAtualizarSidebar() {
  const items = Object.values(rotSelecionados);
  document.getElementById('rot-count').textContent = items.length;

  const lista = document.getElementById('rot-lista-sel');
  if (!items.length) {
    lista.innerHTML = '<div style="color:var(--muted);font-size:12px;text-align:center;padding:20px">Nenhum cliente selecionado.<br>Clique nos pins do mapa.</div>';
    document.getElementById('btn-rot-map').disabled = true;
    document.getElementById('btn-rot-map').style.opacity = '0.5';
    return;
  }

  lista.innerHTML = items.map(({order}) => `
    <div style="display:flex;align-items:center;gap:8px;padding:6px 8px;margin-bottom:4px;background:#f8fafc;border-radius:6px;font-size:11px">
      <span style="width:8px;height:8px;background:#16a34a;border-radius:50%;flex-shrink:0"></span>
      <div style="flex:1;min-width:0">
        <div style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${order.recipient_name}</div>
        <div style="color:var(--muted)">${(order.weight_kg||0).toFixed(0)}kg</div>
      </div>
      <button onclick="rotRemoverItem('${order.id}')"
        style="background:none;border:none;cursor:pointer;color:var(--danger);font-size:14px;padding:0 4px">&#x2715;</button>
    </div>`).join('');

  document.getElementById('btn-rot-map').disabled = false;
  document.getElementById('btn-rot-map').style.opacity = '1';
}

function rotRemoverItem(id) {
  if (rotMarkers[id]) rotMarkers[id].setIcon(rotIcone('#e8521a'));
  delete rotSelecionados[id];
  rotAtualizarSidebar();
  rotAtualizarBarras();
}

function rotLimparTudo() {
  Object.values(rotSelecionados).forEach(({marker}) => marker.setIcon(rotIcone('#e8521a')));
  rotSelecionados = {};
  rotAtualizarSidebar();
  rotAtualizarBarras();
}

function setModoSelecao(modo) {
  rotModo = modo;
  const btnClick = document.getElementById('btn-modo-click');
  const btnArea  = document.getElementById('btn-modo-area');
  const dica     = document.getElementById('dica-modo');

  if (modo === 'click') {
    btnClick.style.border = '2px solid #e8521a';
    btnClick.style.background = '#fff7ed';
    btnClick.style.color = '#e8521a';
    btnArea.style.border = '2px solid var(--border)';
    btnArea.style.background = '#fff';
    btnArea.style.color = 'var(--muted)';
    dica.textContent = 'Clique nos pins para selecionar clientes';
    if (rotDrawingManager) rotDrawingManager.setDrawingMode(null);
  } else {
    btnArea.style.border = '2px solid #2563eb';
    btnArea.style.background = '#eff6ff';
    btnArea.style.color = '#2563eb';
    btnClick.style.border = '2px solid var(--border)';
    btnClick.style.background = '#fff';
    btnClick.style.color = 'var(--muted)';
    dica.textContent = 'Desenhe um poligono no mapa para selecionar a area';
    iniciarDesenhoArea();
  }
}

function iniciarDesenhoArea() {
  if (!rotMap || typeof google === 'undefined') return;
  if (!rotDrawingManager) {
    rotDrawingManager = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.POLYGON,
      drawingControl: false,
      polygonOptions: {fillColor:'#2563eb',fillOpacity:0.2,strokeColor:'#2563eb',strokeWeight:2,clickable:false,editable:false}
    });
    rotDrawingManager.setMap(rotMap);
    google.maps.event.addListener(rotDrawingManager, 'polygoncomplete', function(polygon) {
      rotSelecionarDentroDoPoligono(polygon);
      polygon.setMap(null);
      rotDrawingManager.setDrawingMode(null);
      setModoSelecao('click');
    });
  } else {
    rotDrawingManager.setDrawingMode(google.maps.drawing.OverlayType.POLYGON);
  }
}

function rotSelecionarDentroDoPoligono(polygon) {
  if (!rotVeiculo) { toast('Selecione um veiculo primeiro!','warn'); return; }
  let adicionados = 0;
  rotPedidosTodos.forEach(o => {
    if (rotSelecionados[o.id]) return;
    const lat = parseFloat(o.lat), lng = parseFloat(o.lng);
    const pt = new google.maps.LatLng(lat, lng);
    if (google.maps.geometry.poly.containsLocation(pt, polygon)) {
      const totPeso = rotGetPesoTotal() + (o.weight_kg||0);
      if (totPeso <= rotVeiculo.capKg) {
        rotSelecionados[o.id] = {order: o, marker: rotMarkers[o.id]};
        if (rotMarkers[o.id]) rotMarkers[o.id].setIcon(rotIcone('#16a34a', 12));
        adicionados++;
      }
    }
  });
  rotAtualizarSidebar();
  rotAtualizarBarras();
  toast(`${adicionados} clientes selecionados na area!`);
}

async function roteirizarDoMapa() {
  const items = Object.values(rotSelecionados);
  if (!items.length) { toast('Selecione clientes no mapa!','warn'); return; }
  if (!rotVeiculo) { toast('Selecione um veiculo!','warn'); return; }

  const btn = document.getElementById('btn-rot-map');
  btn.disabled = true;
  btn.innerHTML = '&#x23F3; Roteirizando...';

  const orderIds = items.map(({order}) => order.id);
  const result = document.getElementById('optimize-result');
  result.innerHTML = `<div class="alert info" style="margin-top:16px">&#x23F3; Calculando rota para ${rotVeiculo.plate} com ${orderIds.length} clientes...</div>`;

  try {
    const d = await api('POST', '/routes/optimize', {
      route_date: document.getElementById('opt-date').value,
      vehicle_ids: [rotVeiculo.id],
      order_ids: orderIds,
      time_limit_sec: 30,
      reoptimize: false,
    });

    const cores = ['#e8521a','#2563eb','#16a34a','#d97706','#7c3aed'];
    result.innerHTML = `
      <div class="card" style="margin-top:16px">
        <div class="card-header" style="background:#f0fdf4">
          <span class="card-title" style="color:#16a34a">&#x2705; Rota Criada!</span>
          <span style="font-size:12px;color:var(--muted)">${(d.wall_time_ms/1000).toFixed(1)}s</span>
        </div>
        <div class="card-body" style="padding:16px">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-bottom:16px">
            <div style="background:#f0fdf4;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:22px;font-weight:700;color:#16a34a">${d.routes_created}</div>
              <div style="font-size:10px;color:#16a34a;font-weight:600">ROTAS</div>
            </div>
            <div style="background:#eff6ff;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:22px;font-weight:700;color:#2563eb">${d.total_stops}</div>
              <div style="font-size:10px;color:#2563eb;font-weight:600">PARADAS</div>
            </div>
            <div style="background:#fff7ed;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:22px;font-weight:700;color:#d97706">${d.routes.reduce((s,r)=>s+(r.total_distance_km||0),0).toFixed(1)} km</div>
              <div style="font-size:10px;color:#d97706;font-weight:600">DISTANCIA</div>
            </div>
            <div style="background:#fef9c3;padding:12px;border-radius:8px;text-align:center">
              <div style="font-size:22px;font-weight:700;color:#ca8a04">${d.unassigned_orders.length}</div>
              <div style="font-size:10px;color:#ca8a04;font-weight:600">NAO ALOCADOS</div>
            </div>
          </div>
          ${d.routes.map((r,idx) => {
            const cor = cores[idx % cores.length];
            return `
            <div style="border:2px solid ${cor}30;border-radius:8px;overflow:hidden;margin-bottom:10px">
              <div style="background:${cor}10;padding:10px 14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap">
                <span style="background:${cor};color:#fff;padding:3px 12px;border-radius:6px;font-weight:700;font-size:12px">${r.vehicle_plate}</span>
                <span style="font-size:12px">&#x1F550; 07:30 &rarr; ${r.planned_end}</span>
                <span style="font-size:12px">&#x1F4CD; ${r.total_stops} paradas</span>
                <span style="font-size:12px">&#x1F6E3;&#xFE0F; ${r.total_distance_km} km</span>
                ${r.score?`<span style="font-size:12px;color:#16a34a">&#x2B50; ${r.score}/10</span>`:''}
              </div>
              <div style="padding:8px;overflow-x:auto">
                <table style="width:100%;font-size:11px;border-collapse:collapse">
                  ${r.stops.map((s,si) => `
                  <tr style="background:${si%2===0?'#fff':'#f8fafc'}">
                    <td style="padding:6px 10px"><span style="background:${cor};color:#fff;width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:700">${s.sequence+1}</span></td>
                    <td style="padding:6px 10px;font-family:monospace;color:#2563eb;font-weight:600">${s.eta}</td>
                    <td style="padding:6px 10px;font-weight:600">${s.recipient_name}</td>
                    <td style="padding:6px 10px;color:var(--muted)">${s.address||''}</td>
                    <td style="padding:6px 10px;text-align:right">${(s.weight_kg||0).toFixed(0)} kg</td>
                  </tr>`).join('')}
                </table>
              </div>
            </div>`;
          }).join('')}
          ${d.unassigned_orders.length ?
            `<div class="alert warn">&#x26A0;&#xFE0F; ${d.unassigned_orders.length} pedido(s) nao alocado(s)</div>` :
            `<div class="alert" style="background:#f0fdf4;border:1px solid #bbf7d0;color:#16a34a">&#x2705; Todos os pedidos alocados!</div>`}
        </div>
      </div>`;

    // Atualiza marcadores no mapa
    items.forEach(({order, marker}) => {
      if (marker) marker.setIcon(rotIcone('#2563eb'));
    });
    rotSelecionados = {};
    rotAtualizarSidebar();
    rotAtualizarBarras();
    toast(`Rota criada para ${rotVeiculo.plate}!`);
    loadRoutes();

  } catch(e) {
    result.innerHTML = `<div class="alert danger" style="margin-top:16px">&#x274C; ${e.message}</div>`;
    toast(e.message,'error');
  }
  btn.disabled = false;
  btn.innerHTML = '&#x26A1; Roteirizar Selecionados';
}
'''

# Adiciona drawing library ao Google Maps
if 'libraries=geometry,places' in content:
    content = content.replace(
        'libraries=geometry,places',
        'libraries=geometry,places,drawing'
    )
    print('Google Maps Drawing Library adicionada!')

# Injeta JS
inject_marker = '</script>'
last_script = content.rfind(inject_marker)
if last_script != -1:
    content = content[:last_script] + new_js + '\n' + content[last_script:]
    print('JavaScript injetado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('HTML atualizado com sucesso!')
print('Faca Ctrl+Shift+R no navegador.')
