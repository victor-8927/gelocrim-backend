path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('<div class="page" id="page-monitoramento">')
end   = content.find('<div class="page" id="page-ocorrencias">')

if start == -1 or end == -1:
    print(f'Secao nao encontrada: start={start}, end={end}')
    exit(1)

new_section = '''<div class="page" id="page-monitoramento">
  <div class="page-header" style="margin-bottom:12px">
    <div>
      <div class="page-title">&#x1F5FC; Torre de Controle</div>
      <div class="page-sub">Monitoramento em tempo real das rotas e entregas</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <input type="date" id="mon-date" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px">
      <div id="mon-auto-badge" style="display:flex;align-items:center;gap:6px;background:#f0fdf4;border:1px solid #bbf7d0;padding:6px 12px;border-radius:6px;font-size:12px;color:#16a34a">
        <span style="width:8px;height:8px;background:#16a34a;border-radius:50%;animation:pulse 2s infinite"></span>
        Auto-atualizar 30s
      </div>
      <button class="btn btn-secondary" onclick="loadTorreControle()">&#8635; Atualizar</button>
    </div>
  </div>

  <!-- KPIs -->
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px">
    <div class="card" style="border-left:4px solid #2563eb">
      <div class="card-body" style="padding:14px">
        <div style="font-size:11px;color:var(--muted);font-weight:600;margin-bottom:4px">ROTAS ATIVAS</div>
        <div id="tc-rotas-ativas" style="font-size:28px;font-weight:700;color:#2563eb">—</div>
      </div>
    </div>
    <div class="card" style="border-left:4px solid #d97706">
      <div class="card-body" style="padding:14px">
        <div style="font-size:11px;color:var(--muted);font-weight:600;margin-bottom:4px">EM ENTREGA</div>
        <div id="tc-em-entrega" style="font-size:28px;font-weight:700;color:#d97706">—</div>
      </div>
    </div>
    <div class="card" style="border-left:4px solid #16a34a">
      <div class="card-body" style="padding:14px">
        <div style="font-size:11px;color:var(--muted);font-weight:600;margin-bottom:4px">ENTREGUES</div>
        <div id="tc-entregues" style="font-size:28px;font-weight:700;color:#16a34a">—</div>
      </div>
    </div>
    <div class="card" style="border-left:4px solid #dc2626">
      <div class="card-body" style="padding:14px">
        <div style="font-size:11px;color:var(--muted);font-weight:600;margin-bottom:4px">COM FALHA</div>
        <div id="tc-falhas" style="font-size:28px;font-weight:700;color:#dc2626">—</div>
      </div>
    </div>
    <div class="card" style="border-left:4px solid #7c3aed">
      <div class="card-body" style="padding:14px">
        <div style="font-size:11px;color:var(--muted);font-weight:600;margin-bottom:4px">TAXA SUCESSO</div>
        <div id="tc-taxa" style="font-size:28px;font-weight:700;color:#7c3aed">—</div>
      </div>
    </div>
    <div class="card" style="border-left:4px solid #e8521a">
      <div class="card-body" style="padding:14px">
        <div style="font-size:11px;color:var(--muted);font-weight:600;margin-bottom:4px">KM TOTAL</div>
        <div id="tc-km" style="font-size:28px;font-weight:700;color:#e8521a">—</div>
      </div>
    </div>
  </div>

  <!-- LAYOUT: MAPA + SIDEBAR -->
  <div style="display:grid;grid-template-columns:1fr 340px;gap:12px;min-height:500px">

    <!-- MAPA -->
    <div style="display:flex;flex-direction:column;gap:8px">
      <!-- Legenda -->
      <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;font-size:12px;padding:8px 12px;background:#f8fafc;border-radius:8px;border:1px solid var(--border)">
        <span style="font-weight:600;color:var(--muted)">LEGENDA:</span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#16a34a;border-radius:50%;display:inline-block"></span>Entregue
        </span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#d97706;border-radius:50%;display:inline-block"></span>Em Rota
        </span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#dc2626;border-radius:50%;display:inline-block"></span>Atrasado
        </span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:12px;height:12px;background:#2563eb;border-radius:50%;display:inline-block"></span>Pendente
        </span>
        <span style="display:flex;align-items:center;gap:4px">
          <span style="width:14px;height:14px;background:#1a1d23;border-radius:3px;display:inline-block"></span>Deposito
        </span>
        <span id="tc-ultima-att" style="margin-left:auto;color:var(--muted);font-size:11px">—</span>
      </div>
      <div id="mon-map" style="flex:1;border-radius:10px;overflow:hidden;border:1px solid var(--border);min-height:450px"></div>
    </div>

    <!-- SIDEBAR: STATUS DAS ROTAS -->
    <div style="display:flex;flex-direction:column;gap:8px;overflow-y:auto;max-height:600px">

      <!-- Alertas -->
      <div id="tc-alertas" style="display:none" class="card">
        <div class="card-header" style="background:#fef2f2;padding:10px 12px">
          <span class="card-title" style="color:#dc2626;font-size:12px">&#x26A0;&#xFE0F; ALERTAS</span>
        </div>
        <div id="tc-alertas-lista" class="card-body" style="padding:8px"></div>
      </div>

      <!-- Rotas do dia -->
      <div class="card" style="flex:1">
        <div class="card-header" style="padding:10px 12px">
          <span class="card-title" style="font-size:12px">&#x1F69B; ROTAS DO DIA</span>
          <span id="tc-rotas-count" style="font-size:11px;color:var(--muted)">0 rotas</span>
        </div>
        <div id="tc-rotas-lista" class="card-body" style="padding:8px;overflow-y:auto">
          <div style="color:var(--muted);font-size:12px;text-align:center;padding:20px">
            Clique em Atualizar para carregar as rotas do dia.
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

'''

content = content[:start] + new_section + content[end:]

# JavaScript da Torre de Controle
new_js = '''
// ── TORRE DE CONTROLE ─────────────────────────────────────────────
let tcMap = null;
let tcMarkers = [];
let tcPolylines = [];
let tcAutoInterval = null;

async function loadTorreControle() {
  const today = new Date().toISOString().slice(0,10);
  const dateEl = document.getElementById('mon-date');
  if (!dateEl.value) dateEl.value = today;
  const date = dateEl.value;

  try {
    // Busca rotas e dashboard
    const [dash, routes] = await Promise.all([
      api('GET', '/reports/dashboard'),
      api('GET', `/routes?date=${date}`)
    ]);

    // Atualiza KPIs
    const total = (dash.orders?.delivered||0) + (dash.orders?.failed||0);
    const taxa = total > 0 ? Math.round((dash.orders?.delivered||0) / total * 100) : 0;

    document.getElementById('tc-rotas-ativas').textContent = routes.length || 0;
    document.getElementById('tc-em-entrega').textContent = dash.orders?.routed || 0;
    document.getElementById('tc-entregues').textContent = dash.orders?.delivered || 0;
    document.getElementById('tc-falhas').textContent = dash.orders?.failed || 0;
    document.getElementById('tc-taxa').textContent = taxa + '%';
    document.getElementById('tc-km').textContent = routes.reduce((s,r) => s+(r.total_distance_km||0),0).toFixed(0) + ' km';
    document.getElementById('tc-ultima-att').textContent = 'Atualizado: ' + new Date().toLocaleTimeString('pt-BR');
    document.getElementById('tc-rotas-count').textContent = routes.length + ' rotas';

    // Inicializa mapa
    if (!tcMap && typeof google !== 'undefined') {
      tcMap = new google.maps.Map(document.getElementById('mon-map'), {
        center: {lat: -3.1019, lng: -60.0250},
        zoom: 12,
        mapTypeId: 'roadmap',
      });
      // Deposito
      new google.maps.Marker({
        position: {lat: -3.1019, lng: -60.0250},
        map: tcMap,
        title: 'Deposito Gelocrim',
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          scale: 8,
          fillColor: '#1a1d23',
          fillOpacity: 1,
          strokeColor: '#fff',
          strokeWeight: 2
        }
      });
    }

    // Limpa marcadores e rotas anteriores
    tcMarkers.forEach(m => m.setMap(null));
    tcPolylines.forEach(p => p.setMap(null));
    tcMarkers = [];
    tcPolylines = [];

    const cores = ['#e8521a','#2563eb','#16a34a','#d97706','#7c3aed','#db2777'];
    const alertas = [];

    // Renderiza lista de rotas
    const lista = document.getElementById('tc-rotas-lista');
    if (!routes.length) {
      lista.innerHTML = '<div style="color:var(--muted);font-size:12px;text-align:center;padding:20px">Nenhuma rota para esta data.</div>';
      return;
    }

    lista.innerHTML = '';

    for (let i = 0; i < routes.length; i++) {
      const r = routes[i];
      const cor = cores[i % cores.length];
      const stops = await api('GET', `/routes/${r.route_id}/stops`);

      // Hora atual em minutos
      const agora = new Date();
      const agoraMins = agora.getHours() * 60 + agora.getMinutes();

      let completadas = 0, pendentes = 0, atrasadas = 0;
      const stopsLatLng = [{lat: -3.1019, lng: -60.0250}]; // começa no deposito

      stops.forEach(s => {
        const lat = parseFloat(s.lat), lng = parseFloat(s.lng);
        if (!lat || !lng) return;

        stopsLatLng.push({lat, lng});

        // Determina status e cor do pin
        let corPin = '#2563eb'; // pendente
        let iconeSize = 9;

        if (s.status === 'completed') {
          corPin = '#16a34a';
          completadas++;
          iconeSize = 8;
        } else if (s.status === 'failed') {
          corPin = '#dc2626';
          atrasadas++;
          iconeSize = 10;
        } else {
          // Verifica se está atrasado
          if (s.eta) {
            const [h, m] = s.eta.split(':').map(Number);
            const etaMins = h * 60 + m;
            if (agoraMins > etaMins + 30) {
              corPin = '#dc2626';
              atrasadas++;
              alertas.push(`${r.vehicle_plate}: ${s.recipient_name} atrasado (ETA ${s.eta})`);
            } else {
              corPin = '#d97706';
              pendentes++;
            }
          } else {
            pendentes++;
          }
        }

        if (tcMap) {
          const marker = new google.maps.Marker({
            position: {lat, lng},
            map: tcMap,
            title: s.recipient_name,
            icon: {
              path: google.maps.SymbolPath.CIRCLE,
              scale: iconeSize,
              fillColor: corPin,
              fillOpacity: 1,
              strokeColor: '#fff',
              strokeWeight: 2
            }
          });

          const iw = new google.maps.InfoWindow({
            content: `<div style="font-family:Arial;font-size:12px;min-width:180px">
              <b style="color:${cor}">${r.vehicle_plate}</b> — Parada ${s.sequence+1}<br>
              <b>${s.recipient_name}</b><br>
              ${s.address||''}<br>
              ETA: <b>${s.eta||'—'}</b> | Status: <b>${s.status||'pendente'}</b><br>
              Peso: ${(s.weight_kg||0).toFixed(0)} kg
            </div>`
          });
          marker.addListener('click', () => iw.open(tcMap, marker));
          tcMarkers.push(marker);
        }
      });

      stopsLatLng.push({lat: -3.1019, lng: -60.0250}); // volta ao deposito

      // Desenha linha da rota
      if (tcMap && stopsLatLng.length > 2) {
        const poly = new google.maps.Polyline({
          path: stopsLatLng,
          geodesic: true,
          strokeColor: cor,
          strokeOpacity: 0.7,
          strokeWeight: 3,
          map: tcMap
        });
        tcPolylines.push(poly);
      }

      // Status da rota
      const statusRota = r.status === 'executing' ? '🟡 Em Execução' :
                         r.status === 'done' ? '🟢 Concluída' :
                         r.status === 'optimized' ? '🔵 Otimizada' :
                         r.status === 'released' ? '🟠 Liberada' : '⚪ ' + r.status;

      const pctConcluido = stops.length > 0 ? Math.round(completadas/stops.length*100) : 0;

      // Card da rota
      const card = document.createElement('div');
      card.style.cssText = `border:2px solid ${cor}30;border-radius:8px;padding:10px;margin-bottom:8px;cursor:pointer`;
      card.onclick = () => tcFocarRota(r, stopsLatLng);
      card.innerHTML = `
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
          <span style="background:${cor};color:#fff;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>
          <span style="font-size:11px;color:var(--muted)">${statusRota}</span>
        </div>
        <div style="display:flex;gap:8px;font-size:11px;margin-bottom:8px;flex-wrap:wrap">
          <span>&#x1F4CD; ${stops.length} paradas</span>
          <span>&#x1F6E3;&#xFE0F; ${r.total_distance_km||0} km</span>
          <span>&#x1F550; ${r.planned_start||'07:30'}</span>
        </div>
        <!-- Barra de progresso -->
        <div style="margin-bottom:4px">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-bottom:3px">
            <span>Progresso</span>
            <span>${completadas}/${stops.length} (${pctConcluido}%)</span>
          </div>
          <div style="background:#e5e7eb;border-radius:4px;height:6px;overflow:hidden">
            <div style="width:${pctConcluido}%;height:100%;background:${pctConcluido===100?'#16a34a':cor};border-radius:4px;transition:width .3s"></div>
          </div>
        </div>
        <div style="display:flex;gap:6px;font-size:10px;margin-top:6px">
          <span style="background:#f0fdf4;color:#16a34a;padding:2px 6px;border-radius:3px">&#x2705; ${completadas}</span>
          <span style="background:#fff7ed;color:#d97706;padding:2px 6px;border-radius:3px">&#x1F550; ${pendentes}</span>
          ${atrasadas > 0 ? `<span style="background:#fef2f2;color:#dc2626;padding:2px 6px;border-radius:3px">&#x26A0; ${atrasadas}</span>` : ''}
        </div>`;
      lista.appendChild(card);
    }

    // Exibe alertas
    const alertasDiv = document.getElementById('tc-alertas');
    const alertasLista = document.getElementById('tc-alertas-lista');
    if (alertas.length > 0) {
      alertasDiv.style.display = 'block';
      alertasLista.innerHTML = alertas.map(a =>
        `<div style="font-size:11px;color:#dc2626;padding:4px 0;border-bottom:1px solid #fee2e2">&#x26A0;&#xFE0F; ${a}</div>`
      ).join('');
    } else {
      alertasDiv.style.display = 'none';
    }

  } catch(e) {
    toast(e.message, 'error');
  }
}

function tcFocarRota(rota, pontos) {
  if (!tcMap || !pontos.length) return;
  const bounds = new google.maps.LatLngBounds();
  pontos.forEach(p => bounds.extend(p));
  tcMap.fitBounds(bounds);
}

function tcIniciarAutoUpdate() {
  if (tcAutoInterval) clearInterval(tcAutoInterval);
  tcAutoInterval = setInterval(() => {
    const page = document.querySelector('.page.active');
    if (page && page.id === 'page-monitoramento') {
      loadTorreControle();
    }
  }, 30000);
}

// Inicia auto-update quando pagina carrega
tcIniciarAutoUpdate();
'''

# Injeta JS
inject_marker = '</script>'
last_script = content.rfind(inject_marker)
if last_script != -1:
    content = content[:last_script] + new_js + '\n' + content[last_script:]
    print('JavaScript injetado!')

# Atualiza o navegador para chamar loadTorreControle ao abrir a pagina
content = content.replace(
    "if(page==='monitoramento')",
    "if(page==='monitoramento') { const today=new Date().toISOString().slice(0,10); document.getElementById('mon-date').value=today; loadTorreControle(); } if(page==='monitoramento_unused')"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Torre de Controle criada com sucesso!')
print('Faca Ctrl+Shift+R no navegador e va em Monitoramento.')
