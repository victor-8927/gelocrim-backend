path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Substitui o painel direito de indicadores ──────────────────
old_panel = '''              <!-- COL 3: Indicadores -->
              <div style="border-left:1px solid #1e3a5c;overflow-y:auto;padding:14px;background:#061828">
                <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:14px">INDICADORES DA CARGA</div>

                <!-- Cronograma -->
                <div style="margin-bottom:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F4C5; CRONOGRAMA</div>
                  <div style="display:grid;gap:6px">
                    <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Data saída</span><input type="date" id="conf-data-saida" style="padding:3px 6px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:120px"></div>
                    <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Hora início</span><input type="time" id="conf-hora-inicio" value="07:30" style="padding:3px 6px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:80px"></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Previsão fim</span><span id="conf-hora-fim" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
                  </div>
                </div>

                <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F69B; LOGÍSTICA</div>
                  <div style="display:grid;gap:4px">
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Veículo</span><span id="conf-veiculo" style="font-size:11px;color:#e8f0fe;font-weight:600">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Motorista</span><span id="conf-motorista" style="font-size:11px;color:#e8f0fe">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Capacidade</span><span id="conf-capacidade" style="font-size:11px;color:#e8f0fe">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Peso carga</span><span id="conf-peso" style="font-size:11px;color:#f59e0b;font-weight:600">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Entregas</span><span id="conf-entregas" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Distância est.</span><span id="conf-distancia" style="font-size:11px;color:#64B4FF">—</span></div>
                  </div>
                </div>

                <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F4B0; POR TOP (SANKHYA)</div>
                  <div style="display:grid;gap:4px">
                    <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1000 Vendas</span><span id="conf-top1000" style="font-size:11px;color:#10b981">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1009 Trocas</span><span id="conf-top1009" style="font-size:11px;color:#64B4FF">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1007 Bonif.</span><span id="conf-top1007" style="font-size:11px;color:#a78bfa">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1010 Pré-ped.</span><span id="conf-top1010" style="font-size:11px;color:#f59e0b">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:10px;color:#90afd4">1008 Consig.</span><span id="conf-top1008" style="font-size:11px;color:#90afd4">—</span></div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid #1e3a5c;padding-top:5px;margin-top:4px"><span style="font-size:11px;color:#e8f0fe;font-weight:700">Total</span><span id="conf-total-pedidos" style="font-size:14px;color:#10b981;font-weight:800">—</span></div>
                  </div>
                </div>

                <div style="border-top:1px solid #1e3a5c;padding-top:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">&#x1F4CA; MARGEM OPERACIONAL</div>
                  <div style="display:grid;gap:4px;margin-bottom:12px">
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Custo equipe</span><span id="conf-custo-equipe" style="font-size:11px;color:#f87171">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Combustível</span><span id="conf-custo-diesel" style="font-size:11px;color:#f87171">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Manutenção/IPVA</span><span id="conf-custo-manut" style="font-size:11px;color:#f87171">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#e8f0fe;font-weight:600">Total custos</span><span id="conf-custo-total" style="font-size:12px;color:#f87171;font-weight:700">—</span></div>
                  </div>
                  <div id="conf-semaforo" style="padding:14px;border-radius:10px;text-align:center;background:#1e3a5c;border:1px solid #2563a8">
                    <div style="font-size:32px" id="conf-semaforo-emoji">&#x23F3;</div>
                    <div style="font-size:24px;font-weight:800;margin:4px 0;color:#e8f0fe" id="conf-margem-valor">—</div>
                    <div style="font-size:11px;color:#90afd4" id="conf-margem-label">Margem Operacional</div>
                  </div>
                </div>

              </div>'''

new_panel = '''              <!-- COL 3: Indicadores -->
              <div style="border-left:1px solid #1e3a5c;overflow-y:auto;padding:14px;background:#061828">
                <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:14px">INDICADORES DA CARGA</div>

                <!-- Cronograma -->
                <div style="margin-bottom:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">📅 CRONOGRAMA</div>
                  <div style="display:grid;gap:6px">
                    <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Data saída</span><input type="date" id="conf-data-saida" style="padding:3px 6px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:120px"></div>
                    <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#90afd4">Hora início</span><input type="time" id="conf-hora-inicio" value="07:30" style="padding:3px 6px;border:1px solid #1e3a5c;border-radius:4px;font-size:11px;background:#0a1628;color:#e8f0fe;width:80px"></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Previsão fim</span><span id="conf-hora-fim" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
                  </div>
                </div>

                <!-- Logística com barras -->
                <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">🚛 LOGÍSTICA</div>
                  <div style="display:grid;gap:4px;margin-bottom:10px">
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Veículo</span><span id="conf-veiculo" style="font-size:11px;color:#e8f0fe;font-weight:600">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Motorista</span><span id="conf-motorista" style="font-size:11px;color:#e8f0fe">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Entregas</span><span id="conf-entregas" style="font-size:11px;color:#64B4FF;font-weight:600">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Distância</span><span id="conf-distancia" style="font-size:11px;color:#64B4FF">—</span></div>
                  </div>
                  <!-- Barras de capacidade -->
                  <div style="display:grid;gap:8px">
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                        <span style="color:#90afd4">⚖️ Peso</span><span id="conf-peso" style="color:#f59e0b;font-weight:600">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:6px"><div id="conf-bar-peso" style="height:100%;background:#f59e0b;border-radius:3px;width:0%;transition:width .3s"></div></div>
                    </div>
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                        <span style="color:#90afd4">📦 Volume</span><span id="conf-volume" style="color:#2dd4bf;font-weight:600">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:6px"><div id="conf-bar-vol" style="height:100%;background:#2dd4bf;border-radius:3px;width:0%;transition:width .3s"></div></div>
                    </div>
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">
                        <span style="color:#90afd4">🪵 Pallets</span><span id="conf-pallets" style="color:#a78bfa;font-weight:600">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:6px"><div id="conf-bar-pallets" style="height:100%;background:#a78bfa;border-radius:3px;width:0%;transition:width .3s"></div></div>
                    </div>
                    <span id="conf-capacidade" style="display:none"></span>
                  </div>
                </div>

                <!-- Financeiro por TOP com mini barras -->
                <div style="border-top:1px solid #1e3a5c;padding-top:12px;margin-bottom:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">💰 MIX DE CARGA POR TOP</div>
                  <div style="display:grid;gap:6px">
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">
                        <span style="color:#90afd4">1000 Vendas</span><span id="conf-top1000" style="color:#10b981">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1000" style="height:100%;background:#10b981;border-radius:3px;width:0%"></div></div>
                    </div>
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">
                        <span style="color:#90afd4">1009 Trocas</span><span id="conf-top1009" style="color:#64B4FF">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1009" style="height:100%;background:#64B4FF;border-radius:3px;width:0%"></div></div>
                    </div>
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">
                        <span style="color:#90afd4">1007 Bonif.</span><span id="conf-top1007" style="color:#a78bfa">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1007" style="height:100%;background:#a78bfa;border-radius:3px;width:0%"></div></div>
                    </div>
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">
                        <span style="color:#90afd4">1010 Pré-ped.</span><span id="conf-top1010" style="color:#f59e0b">—</span>
                      </div>
                      <div style="background:#1e3a5c;border-radius:3px;height:4px"><div id="conf-bar-top1010" style="height:100%;background:#f59e0b;border-radius:3px;width:0%"></div></div>
                    </div>
                    <div>
                      <div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">
                        <span style="color:#90afd4">1008 Consig.</span><span id="conf-top1008" style="color:#90afd4">—</span>
                      </div>
                    </div>
                    <div style="display:flex;justify-content:space-between;border-top:1px solid #1e3a5c;padding-top:5px;margin-top:2px">
                      <span style="font-size:11px;color:#e8f0fe;font-weight:700">Total Pedidos</span>
                      <span id="conf-total-pedidos" style="font-size:14px;color:#10b981;font-weight:800">—</span>
                    </div>
                  </div>
                </div>

                <!-- Margem operacional -->
                <div style="border-top:1px solid #1e3a5c;padding-top:12px">
                  <div style="font-size:10px;color:#64B4FF;font-weight:700;margin-bottom:8px">📊 MARGEM OPERACIONAL</div>
                  <div style="display:grid;gap:4px;margin-bottom:10px">
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Custo equipe</span><span id="conf-custo-equipe" style="font-size:11px;color:#f87171">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Combustível</span><span id="conf-custo-diesel" style="font-size:11px;color:#f87171">—</span></div>
                    <div style="display:flex;justify-content:space-between"><span style="font-size:11px;color:#90afd4">Manutenção/IPVA</span><span id="conf-custo-manut" style="font-size:11px;color:#f87171">—</span></div>
                    <div style="display:flex;justify-content:space-between">
                      <span style="font-size:11px;color:#e8f0fe;font-weight:600">Total custos</span>
                      <span id="conf-custo-total" style="font-size:12px;color:#f87171;font-weight:700">—</span>
                    </div>
                  </div>
                  <div id="conf-semaforo" style="padding:14px;border-radius:10px;text-align:center;background:#1e3a5c;border:1px solid #2563a8">
                    <div style="font-size:32px" id="conf-semaforo-emoji">⏳</div>
                    <div style="font-size:24px;font-weight:800;margin:4px 0;color:#e8f0fe" id="conf-margem-valor">—</div>
                    <div style="font-size:11px;color:#90afd4" id="conf-margem-label">Margem Operacional</div>
                  </div>
                  <!-- Alerta margem negativa -->
                  <div id="conf-alerta-margem" style="display:none;margin-top:8px;padding:10px;background:rgba(248,113,113,.15);border:1px solid #f87171;border-radius:8px">
                    <div style="font-size:11px;color:#f87171;font-weight:700;margin-bottom:6px">⚠️ Margem Negativa — Justificativa Obrigatória</div>
                    <textarea id="conf-justificativa" rows="2" placeholder="Informe o motivo para gravar com margem negativa..." style="width:100%;background:#0a1628;border:1px solid #f87171;border-radius:4px;color:#e8f0fe;font-size:11px;padding:6px;resize:none"></textarea>
                  </div>
                  <!-- Botão Romaneio -->
                  <button onclick="gerarRomaneio()" style="margin-top:10px;width:100%;padding:8px;background:transparent;border:1px solid #1e3a5c;color:#90afd4;border-radius:6px;font-size:11px;cursor:pointer">
                    🖨️ Gerar Romaneio PDF
                  </button>
                </div>
              </div>'''

if old_panel in content:
    content = content.replace(old_panel, new_panel)
    print('Painel direito atualizado com barras e novas funcionalidades!')
else:
    print('ERRO: painel direito não encontrado')

# ── 2. Atualiza botão GRAVAR com bloqueio e camada de tráfego ─────
old_gravar_btn = '''              <button onclick="gravarCarga()" style="padding:7px 20px;background:#10b981;border:none;color:#fff;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer">&#x1F4BE; GRAVAR CARGA</button>'''

new_gravar_btn = '''              <button id="btn-gravar-carga" onclick="gravarCarga()" style="padding:7px 20px;background:#10b981;border:none;color:#fff;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer">💾 GRAVAR CARGA</button>
              <button onclick="toggleTrafegoMapa()" style="padding:7px 12px;background:transparent;border:1px solid #1e3a5c;color:#64B4FF;border-radius:6px;font-size:11px;cursor:pointer" title="Tráfego em tempo real">🚦 Tráfego</button>'''

if old_gravar_btn in content:
    content = content.replace(old_gravar_btn, new_gravar_btn)
    print('Botão GRAVAR e tráfego adicionados!')

# ── 3. Adiciona funções JS novas ───────────────────────────────────
new_funcs = '''
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
    </style></head><body>
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
    </body></html>`;

  const w = window.open('', '_blank');
  w.document.write(html);
  w.document.close();
  w.print();
  toast('Romaneio gerado!', 'success');
}

'''

if 'function toggleTrafegoMapa' not in content:
    content = content.replace('function renderizarListaConf()', new_funcs + 'function renderizarListaConf()')
    print('Novas funções da Conferência adicionadas!')

# ── 4. Atualiza abrirConferenciaMaster para chamar as novas funções ─
old_call = '''  // Semáforo de margem
  const emoji = fatTotal === 0 ? '⚠️' : margem >= 20 ? '🟢' : margem >= 10 ? '🟡' : '🔴';'''

new_call = '''  // Barras de capacidade
  atualizarBarrasCapacidade(pesoTotal, capKg, volTotal, capM3);
  atualizarBarrasTOP(fatTotal);
  verificarMargemNegativa(margem);
  verificarCamposObrigatorios();

  // Semáforo de margem
  const emoji = fatTotal === 0 ? '⚠️' : margem >= 20 ? '🟢' : margem >= 10 ? '🟡' : '🔴';'''

if old_call in content:
    content = content.replace(old_call, new_call)
    print('abrirConferenciaMaster atualizado!')

# ── 5. Atualiza gravarCarga para verificar justificativa ───────────
old_gravar_check = '''  if (!veiculo || !motorista) {
    toast('Selecione veículo e motorista!', 'error');
    return;
  }'''

new_gravar_check = '''  if (!veiculo || !motorista) {
    toast('Selecione veículo e motorista!', 'error');
    return;
  }
  // Verifica margem negativa
  const alertaMargem = document.getElementById('conf-alerta-margem');
  if (alertaMargem && alertaMargem.style.display !== 'none') {
    const justificativa = document.getElementById('conf-justificativa')?.value?.trim();
    if (!justificativa) {
      toast('Informe a justificativa para gravar com margem negativa!', 'error');
      return;
    }
  }'''

if old_gravar_check in content:
    content = content.replace(old_gravar_check, new_gravar_check)
    print('gravarCarga com verificação de justificativa!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
