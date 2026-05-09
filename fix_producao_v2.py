path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Atualiza botões de aba para incluir Pallet Carregado ────────
old_tabs = '''          <div style="display:flex;gap:6px">
            <button id="btn-tab-pallet" onclick="switchProducaoTab('pallet')"
              style="padding:8px 18px;border:2px solid #e8521a;background:rgba(232,82,26,.15);color:#e8521a;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              🪵 Pallets
            </button>
            <button id="btn-tab-item" onclick="switchProducaoTab('item')"
              style="padding:8px 18px;border:2px solid #1e3a5c;background:transparent;color:#90afd4;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              🧊 Itens de Gelo
            </button>
          </div>'''

new_tabs = '''          <div style="display:flex;gap:6px">
            <button id="btn-tab-pallet" onclick="switchProducaoTab('pallet')"
              style="padding:8px 18px;border:2px solid #e8521a;background:rgba(232,82,26,.15);color:#e8521a;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              🪵 Pallets
            </button>
            <button id="btn-tab-item" onclick="switchProducaoTab('item')"
              style="padding:8px 18px;border:2px solid #1e3a5c;background:transparent;color:#90afd4;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              🧊 Itens de Gelo
            </button>
            <button id="btn-tab-carregado" onclick="switchProducaoTab('carregado')"
              style="padding:8px 18px;border:2px solid #1e3a5c;background:transparent;color:#90afd4;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              📦 Pallet Carregado
            </button>
          </div>'''

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    print('Abas atualizadas com Pallet Carregado!')

# ── 2. Adiciona seção Pallet Carregado após seção Itens ────────────
old_modal_pallet_section = '''      <!-- MODAL PALLET -->'''

new_carregado_section = '''      <!-- SEÇÃO PALLET CARREGADO -->
      <div id="section-carregado" style="display:none">
        <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">📦 PALLETS CARREGADOS</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px" id="pallets-carregados-grid">
          <div class="loading-state" style="grid-column:1/-1">Carregando...</div>
        </div>
      </div>

      <!-- MODAL PALLET CARREGADO -->
      <div id="modal-pallet-carregado" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:640px;max-height:90vh;overflow-y:auto">
          <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-pc-titulo">Pallet Carregado</span>
            <button onclick="document.getElementById('modal-pallet-carregado').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div style="padding:20px 24px">

            <!-- Tipo do item -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🧊 TIPO DE GELO</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:20px" id="pc-tipo-grid">
              <div onclick="selecionarTipoPallet(5)" id="pc-tipo-5"
                style="padding:12px;border:2px solid #1e3a5c;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:22px">🧊</div>
                <div style="font-size:14px;font-weight:700;color:#64B4FF;margin-top:4px">5 kg</div>
                <div style="font-size:10px;color:#90afd4">180 un/pallet</div>
              </div>
              <div onclick="selecionarTipoPallet(10)" id="pc-tipo-10"
                style="padding:12px;border:2px solid #1e3a5c;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:22px">🧊</div>
                <div style="font-size:14px;font-weight:700;color:#64B4FF;margin-top:4px">10 kg</div>
                <div style="font-size:10px;color:#90afd4">110 un/pallet</div>
              </div>
              <div onclick="selecionarTipoPallet(20)" id="pc-tipo-20"
                style="padding:12px;border:2px solid #1e3a5c;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:22px">🧊</div>
                <div style="font-size:14px;font-weight:700;color:#64B4FF;margin-top:4px">20 kg</div>
                <div style="font-size:10px;color:#90afd4">50 un/pallet</div>
              </div>
              <div onclick="selecionarTipoPallet(40)" id="pc-tipo-40"
                style="padding:12px;border:2px solid #1e3a5c;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:22px">🧊</div>
                <div style="font-size:14px;font-weight:700;color:#64B4FF;margin-top:4px">40 kg</div>
                <div style="font-size:10px;color:#90afd4">27 un/pallet</div>
              </div>
            </div>
            <input type="hidden" id="pc-tipo-kg" value="5">

            <!-- Dimensões do pallet carregado -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">📐 DIMENSÕES DO PALLET CARREGADO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Comprimento (m)</label>
                <input class="form-control" type="number" step="0.01" id="pc-comp" placeholder="1.20" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcPalletCarregado()">
              </div>
              <div>
                <label class="form-label">Largura (m)</label>
                <input class="form-control" type="number" step="0.01" id="pc-larg" placeholder="1.00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcPalletCarregado()">
              </div>
              <div>
                <label class="form-label">Altura total (m)</label>
                <div style="font-size:10px;color:#90afd4;margin-bottom:3px">Base do pallet + camadas de sacos</div>
                <input class="form-control" type="number" step="0.01" id="pc-alt" placeholder="1.50" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcPalletCarregado()">
              </div>
            </div>

            <!-- Resultados calculados -->
            <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:16px;margin-bottom:16px">
              <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">📊 CÁLCULOS AUTOMÁTICOS</div>
              <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px">
                <div style="text-align:center">
                  <div style="font-size:22px;font-weight:800;color:#f59e0b" id="pc-res-un">—</div>
                  <div style="font-size:10px;color:#90afd4">Unidades/Pallet</div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:22px;font-weight:800;color:#f87171" id="pc-res-peso">—</div>
                  <div style="font-size:10px;color:#90afd4">Peso Total (kg)</div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:22px;font-weight:800;color:#2dd4bf" id="pc-res-cub">—</div>
                  <div style="font-size:10px;color:#90afd4">Cubagem (m³)</div>
                </div>
                <div style="text-align:center">
                  <div style="font-size:22px;font-weight:800;color:#a78bfa" id="pc-res-pallets-truck">—</div>
                  <div style="font-size:10px;color:#90afd4">Pallets/Truck</div>
                </div>
              </div>
            </div>

            <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
              <button onclick="document.getElementById('modal-pallet-carregado').style.display='none'" class="btn btn-secondary">Fechar</button>
              <button onclick="salvarPalletCarregado()" class="btn btn-primary">💾 Salvar Configuração</button>
            </div>
          </div>
        </div>
      </div>

      <!-- MODAL PALLET -->'''

if old_modal_pallet_section in content:
    content = content.replace(old_modal_pallet_section, new_carregado_section)
    print('Seção Pallet Carregado adicionada!')

# ── 3. Atualiza Modal Item — remove Un./Pallet e TOP, adiciona cubagem ──
old_modal_item_body = '''            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Nome do Item *</label>
                <input class="form-control" id="i-nome" placeholder="Gelo 5kg" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Peso (kg) *</label>
                <input class="form-control" type="number" step="0.1" id="i-peso" placeholder="5" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Comprimento (m)</label>
                <input class="form-control" type="number" step="0.01" id="i-comp" placeholder="0.30" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Largura (m)</label>
                <input class="form-control" type="number" step="0.01" id="i-larg" placeholder="0.20" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Altura (m)</label>
                <input class="form-control" type="number" step="0.01" id="i-alt" placeholder="0.15" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Un. por Pallet *</label>
                <input class="form-control" type="number" id="i-un-pallet" placeholder="180" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                <div style="font-size:10px;color:#90afd4;margin-top:3px">Ex: 5kg=180 · 10kg=110 · 20kg=50 · 40kg=27</div>
              </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">TOP</label>
                <select class="form-control" id="i-top" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="1000">TOP 1000 — Venda</option>
                  <option value="1007">TOP 1007 — Bonificação</option>
                  <option value="1008">TOP 1008 — Consignado</option>
                  <option value="1009">TOP 1009 — Troca</option>
                  <option value="1010">TOP 1010 — Pré-pedido</option>
                </select>
              </div>
              <div>
                <label class="form-label">Observação</label>
                <input class="form-control" id="i-obs" placeholder="Saco plástico, caixinha..." style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
            </div>'''

new_modal_item_body = '''            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Nome do Item *</label>
                <input class="form-control" id="i-nome" placeholder="Gelo 5kg" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Peso (kg) *</label>
                <input class="form-control" type="number" step="0.1" id="i-peso" placeholder="5" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Comprimento (m)</label>
                <input class="form-control" type="number" step="0.01" id="i-comp" placeholder="0.30" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcItemCubagem()">
              </div>
              <div>
                <label class="form-label">Largura (m)</label>
                <input class="form-control" type="number" step="0.01" id="i-larg" placeholder="0.20" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcItemCubagem()">
              </div>
              <div>
                <label class="form-label">Altura (m)</label>
                <input class="form-control" type="number" step="0.01" id="i-alt" placeholder="0.15" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcItemCubagem()">
              </div>
              <div>
                <label class="form-label">Cubagem (m³)</label>
                <input class="form-control" id="i-cubagem" readonly placeholder="calculado automaticamente" style="background:#061020;color:#64B4FF;border-color:#1e3a5c">
              </div>
            </div>
            <div style="margin-bottom:16px">
              <label class="form-label">Observação</label>
              <input class="form-control" id="i-obs" placeholder="Saco plástico, caixinha..." style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
            </div>
            <input type="hidden" id="i-un-pallet" value="0">
            <input type="hidden" id="i-top" value="1000">'''

if old_modal_item_body in content:
    content = content.replace(old_modal_item_body, new_modal_item_body)
    print('Modal Item atualizado - removido TOP e Un./Pallet, adicionado cubagem!')

# ── 4. Atualiza funções JS ─────────────────────────────────────────
old_switchTab = '''function switchProducaoTab(tab) {
  producaoTab = tab;
  const btnP = document.getElementById('btn-tab-pallet');
  const btnI = document.getElementById('btn-tab-item');
  const secP = document.getElementById('section-pallets');
  const secI = document.getElementById('section-itens');
  const btnNovo = document.getElementById('btn-novo-producao');

  if (tab === 'pallet') {
    btnP.style.border = '2px solid #e8521a'; btnP.style.background = 'rgba(232,82,26,.15)'; btnP.style.color = '#e8521a';
    btnI.style.border = '2px solid #1e3a5c'; btnI.style.background = 'transparent'; btnI.style.color = '#90afd4';
    secP.style.display = 'block'; secI.style.display = 'none';
    if (btnNovo) { btnNovo.textContent = '+ Novo Pallet'; btnNovo.onclick = abrirModalPallet; }
  } else {
    btnI.style.border = '2px solid #64B4FF'; btnI.style.background = 'rgba(100,180,255,.15)'; btnI.style.color = '#64B4FF';
    btnP.style.border = '2px solid #1e3a5c'; btnP.style.background = 'transparent'; btnP.style.color = '#90afd4';
    secI.style.display = 'block'; secP.style.display = 'none';
    if (btnNovo) { btnNovo.textContent = '+ Novo Item'; btnNovo.onclick = abrirModalItem; }
  }
  loadProducao();
}'''

new_switchTab = '''function switchProducaoTab(tab) {
  producaoTab = tab;
  const tabs = ['pallet','item','carregado'];
  const cores = {pallet:'#e8521a', item:'#64B4FF', carregado:'#a78bfa'};
  tabs.forEach(t => {
    const btn = document.getElementById(`btn-tab-${t}`);
    if (!btn) return;
    if (t === tab) {
      btn.style.border = `2px solid ${cores[t]}`;
      btn.style.background = `rgba(${t==='pallet'?'232,82,26':t==='item'?'100,180,255':'167,139,250'},.15)`;
      btn.style.color = cores[t];
    } else {
      btn.style.border = '2px solid #1e3a5c';
      btn.style.background = 'transparent';
      btn.style.color = '#90afd4';
    }
  });
  document.getElementById('section-pallets').style.display    = tab==='pallet'    ? 'block' : 'none';
  document.getElementById('section-itens').style.display      = tab==='item'      ? 'block' : 'none';
  document.getElementById('section-carregado').style.display  = tab==='carregado' ? 'block' : 'none';
  const btnNovo = document.getElementById('btn-novo-producao');
  if (tab === 'pallet')    { btnNovo.textContent = '+ Novo Pallet';           btnNovo.onclick = () => abrirModalPallet(); }
  if (tab === 'item')      { btnNovo.textContent = '+ Novo Item';             btnNovo.onclick = () => abrirModalItem(); }
  if (tab === 'carregado') { btnNovo.textContent = '+ Configurar Pallet';     btnNovo.onclick = () => abrirModalPalletCarregado(); }
  loadProducao();
}

function calcItemCubagem() {
  const c = parseFloat(document.getElementById('i-comp')?.value||0);
  const l = parseFloat(document.getElementById('i-larg')?.value||0);
  const a = parseFloat(document.getElementById('i-alt')?.value||0);
  const el = document.getElementById('i-cubagem');
  if (el && c && l && a) el.value = (c*l*a).toFixed(6) + ' m³';
}

// Tabela un/pallet por tipo
const unPorPallet = {5:180, 10:110, 20:50, 40:27};
let pcTipoSelecionado = 5;

function selecionarTipoPallet(kg) {
  pcTipoSelecionado = kg;
  [5,10,20,40].forEach(k => {
    const el = document.getElementById(`pc-tipo-${k}`);
    if (!el) return;
    if (k === kg) {
      el.style.border = '2px solid #64B4FF';
      el.style.background = 'rgba(100,180,255,.15)';
    } else {
      el.style.border = '2px solid #1e3a5c';
      el.style.background = 'transparent';
    }
  });
  document.getElementById('pc-tipo-kg').value = kg;
  calcPalletCarregado();
}

function calcPalletCarregado() {
  const c   = parseFloat(document.getElementById('pc-comp')?.value||0);
  const l   = parseFloat(document.getElementById('pc-larg')?.value||0);
  const a   = parseFloat(document.getElementById('pc-alt')?.value||0);
  const kg  = parseInt(document.getElementById('pc-tipo-kg')?.value||5);
  const un  = unPorPallet[kg] || 0;
  const pesTotal = un * kg;
  const cub = c && l && a ? (c*l*a).toFixed(3) : '—';
  // Estima pallets por truck (baú 6x2.4x2.2 = 31.68m³ aprox)
  const cubNum = c && l && a ? c*l*a : 0;
  const palletsNoTruck = cubNum > 0 ? Math.floor(31.68 / cubNum) : '—';
  const el = (id,val) => { const e=document.getElementById(id); if(e) e.textContent=val; };
  el('pc-res-un',            un + ' un');
  el('pc-res-peso',          pesTotal + ' kg');
  el('pc-res-cub',           cub + ' m³');
  el('pc-res-pallets-truck', palletsNoTruck);
}

function abrirModalPalletCarregado() {
  selecionarTipoPallet(5);
  document.getElementById('pc-comp').value = '1.20';
  document.getElementById('pc-larg').value = '1.00';
  document.getElementById('pc-alt').value  = '1.50';
  calcPalletCarregado();
  document.getElementById('modal-pallet-carregado').style.display = 'flex';
}

async function salvarPalletCarregado() {
  const kg  = parseInt(document.getElementById('pc-tipo-kg').value||5);
  const c   = parseFloat(document.getElementById('pc-comp').value||0);
  const l   = parseFloat(document.getElementById('pc-larg').value||0);
  const a   = parseFloat(document.getElementById('pc-alt').value||0);
  const un  = unPorPallet[kg] || 0;
  const body = {
    nome: `Pallet ${kg}kg carregado`,
    comprimento: c, largura: l, altura: a,
    cubagem: parseFloat((c*l*a).toFixed(4)),
    peso_max: un * kg,
    observacao: `${un} unidades de ${kg}kg | Cubagem: ${(c*l*a).toFixed(3)}m³`
  };
  try {
    await api('POST', '/producao/pallets', body);
    toast(`Pallet ${kg}kg configurado!`, 'success');
    document.getElementById('modal-pallet-carregado').style.display = 'none';
    loadProducao();
  } catch(e) { toast(e.message, 'error'); }
}'''

if old_switchTab in content:
    content = content.replace(old_switchTab, new_switchTab)
    print('switchProducaoTab e funções de pallet carregado atualizadas!')

# ── 5. Atualiza loadProducao para mostrar pallet carregado ─────────
old_load_producao_end = '''async function editarPallet(id) {
  const p = palletsData.find(x=>x.id===id);
  if (p) abrirModalPallet(p);
}'''

new_load_producao_carregado = '''  if (producaoTab === 'carregado') {
    try {
      const pallets = await api('GET', '/producao/pallets');
      const carregados = pallets.filter(p => p.observacao && p.observacao.includes('unidades'));
      const grid = document.getElementById('pallets-carregados-grid');
      if (!grid) return;
      if (carregados.length === 0) {
        grid.innerHTML = '<div class="loading-state" style="grid-column:1/-1">Nenhum pallet carregado configurado. Clique em "+ Configurar Pallet"</div>';
        return;
      }
      grid.innerHTML = carregados.map(p => `
        <div class="card" style="margin-bottom:0;padding:16px;border-left:3px solid #64B4FF">
          <div style="font-size:14px;font-weight:700;color:#64B4FF;margin-bottom:12px">📦 ${p.nome}</div>
          <div style="display:grid;gap:6px;font-size:12px">
            <div style="display:flex;justify-content:space-between"><span style="color:#90afd4">Dimensões</span><span>${p.comprimento}×${p.largura}×${p.altura} m</span></div>
            <div style="display:flex;justify-content:space-between"><span style="color:#90afd4">Cubagem</span><span style="color:#2dd4bf">${p.cubagem} m³</span></div>
            <div style="display:flex;justify-content:space-between"><span style="color:#90afd4">Peso total</span><span style="color:#f87171">${p.peso_max} kg</span></div>
            <div style="font-size:10px;color:#90afd4;margin-top:4px">${p.observacao||''}</div>
          </div>
          <button onclick="deletarPallet('${p.id}')" style="margin-top:10px;width:100%;padding:6px;background:transparent;border:1px solid #f87171;color:#f87171;border-radius:6px;font-size:11px;cursor:pointer">Remover</button>
        </div>`).join('');
    } catch(e) { console.log(e); }
    return;
  }

async function editarPallet(id) {
  const p = palletsData.find(x=>x.id===id);
  if (p) abrirModalPallet(p);
}'''

if old_load_producao_end in content:
    content = content.replace(old_load_producao_end, new_load_producao_carregado)
    print('loadProducao atualizado com aba carregado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
