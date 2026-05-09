path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Adiciona clique na barra de progresso da tabela de rotas ────
old_barra = '''            <td style="min-width:140px">
              <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                <span style="color:#90afd4">${entregues}/${totalStops} entregas</span>
                <span style="color:${corBar};font-weight:600">${pct}%</span>
              </div>
              <div style="background:#1e3a5c;border-radius:3px;height:6px;overflow:hidden">
                <div style="height:100%;background:${corBar};border-radius:3px;width:${pct}%;transition:width .3s"></div>
              </div>
            </td>'''

new_barra = '''            <td style="min-width:160px;cursor:pointer" onclick="abrirDetalheProgresso('${r.route_id||r.id}','${r.vehicle_plate}')" title="Clique para ver detalhes">
              <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                <span style="color:#90afd4">${entregues}/${totalStops} entregas</span>
                <span style="color:${corBar};font-weight:600">${pct}%</span>
              </div>
              <div style="background:#1e3a5c;border-radius:3px;height:8px;overflow:hidden">
                <div style="height:100%;background:${corBar};border-radius:3px;width:${pct}%;transition:width .3s"></div>
              </div>
              <div style="font-size:9px;color:#90afd4;margin-top:2px">Clique para detalhes →</div>
            </td>'''

if old_barra in content:
    content = content.replace(old_barra, new_barra)
    print('Clique na barra adicionado!')
else:
    print('ERRO: padrão barra não encontrado')

# ── 2. Adiciona modal de detalhe de progresso ──────────────────────
old_fim_rotas = '''    </div>

    <!-- ══ MONITORAMENTO ══ -->'''

new_fim_rotas = '''
      <!-- MODAL DETALHE PROGRESSO -->
      <div id="modal-progresso" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:640px;max-height:85vh;overflow-y:auto">
          <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-prog-titulo">Progresso da Rota</span>
            <button onclick="document.getElementById('modal-progresso').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div id="modal-prog-body" style="padding:20px 24px">Carregando...</div>
        </div>
      </div>

    </div>

    <!-- ══ MONITORAMENTO ══ -->'''

if old_fim_rotas in content:
    content = content.replace(old_fim_rotas, new_fim_rotas)
    print('Modal de progresso adicionado!')

# ── 3. Adiciona função abrirDetalheProgresso ──────────────────────
new_func = '''
async function abrirDetalheProgresso(routeId, plate) {
  const modal = document.getElementById('modal-progresso');
  modal.style.display = 'flex';
  document.getElementById('modal-prog-titulo').textContent = `📊 Progresso — ${plate}`;
  const body = document.getElementById('modal-prog-body');
  body.innerHTML = '<div class="loading-state">Carregando entregas...</div>';

  try {
    const stops = await api('GET', `/routes/${routeId}/stops`);
    const entregues = stops.filter(s=>s.status==='delivered').length;
    const falhas    = stops.filter(s=>s.status==='failed').length;
    const pendentes = stops.filter(s=>s.status==='pending'||!s.status).length;
    const total     = stops.length;
    const pct       = total>0?Math.round(entregues/total*100):0;

    body.innerHTML = `
      <!-- Resumo -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px;text-align:center">
          <div style="font-size:20px;font-weight:800;color:#10b981">${entregues}</div>
          <div style="font-size:10px;color:#90afd4">Entregues</div>
        </div>
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px;text-align:center">
          <div style="font-size:20px;font-weight:800;color:#f87171">${falhas}</div>
          <div style="font-size:10px;color:#90afd4">Com Falha</div>
        </div>
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px;text-align:center">
          <div style="font-size:20px;font-weight:800;color:#f59e0b">${pendentes}</div>
          <div style="font-size:10px;color:#90afd4">Pendentes</div>
        </div>
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px;text-align:center">
          <div style="font-size:20px;font-weight:800;color:#64B4FF">${pct}%</div>
          <div style="font-size:10px;color:#90afd4">Progresso</div>
        </div>
      </div>

      <!-- Barra geral -->
      <div style="margin-bottom:16px">
        <div style="background:#1e3a5c;border-radius:6px;height:10px;overflow:hidden">
          <div style="height:100%;background:${pct>=100?'#10b981':pct>=50?'#64B4FF':'#f59e0b'};border-radius:6px;width:${pct}%"></div>
        </div>
      </div>

      <!-- Lista de paradas -->
      <table>
        <thead><tr><th>#</th><th>Cliente</th><th>Status</th><th>Hora</th><th>Observação</th></tr></thead>
        <tbody>
          ${stops.map((s,i)=>`<tr>
            <td style="text-align:center;font-weight:700;color:#64B4FF">${i+1}</td>
            <td>
              <div style="font-weight:600;font-size:12px">${s.recipient_name||'—'}</div>
              <div style="font-size:10px;color:#90afd4">${s.address||''}</div>
            </td>
            <td>
              <span class="badge ${s.status||'pending'}" style="font-size:10px">
                ${s.status==='delivered'?'✅ Entregue':s.status==='failed'?'❌ Falhou':'🔵 Pendente'}
              </span>
            </td>
            <td style="font-size:11px;color:#90afd4">
              ${s.arrived_at?new Date(s.arrived_at).toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'}):s.time_window_start||'—'}
            </td>
            <td style="font-size:11px;color:#f87171">${s.failure_reason||''}</td>
          </tr>`).join('')}
        </tbody>
      </table>`;
  } catch(e) {
    body.innerHTML = `<div class="loading-state">${e.message}</div>`;
  }
}

'''

if 'function abrirDetalheProgresso' not in content:
    content = content.replace('function toggleTodasRotas', new_func + 'function toggleTodasRotas')
    print('Função abrirDetalheProgresso adicionada!')

# ── 4. Corrige o botão de tráfego do monitoramento ────────────────
# O problema é que o monMap pode não estar inicializado quando clica
old_toggle_trafego = '''function toggleTrafegoMon() {
  if (!monMap) return;
  if (monTrafegoLayer) {
    monTrafegoLayer.setMap(null);
    monTrafegoLayer = null;
    toast('Tráfego removido', 'info');
  } else {
    monTrafegoLayer = new google.maps.TrafficLayer();
    monTrafegoLayer.setMap(monMap);
    toast('Tráfego ativado!', 'success');
  }
}'''

new_toggle_trafego = '''function toggleTrafegoMon() {
  if (!monMap) {
    toast('Carregue o mapa primeiro!', 'error');
    loadMonitoring();
    return;
  }
  if (monTrafegoLayer) {
    monTrafegoLayer.setMap(null);
    monTrafegoLayer = null;
    toast('Tráfego removido', 'info');
  } else {
    monTrafegoLayer = new google.maps.TrafficLayer();
    monTrafegoLayer.setMap(monMap);
    toast('Tráfego em tempo real ativado!', 'success');
  }
}'''

if old_toggle_trafego in content:
    content = content.replace(old_toggle_trafego, new_toggle_trafego)
    print('toggleTrafegoMon corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
