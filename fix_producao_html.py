path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Adiciona item no sidebar ────────────────────────────────────
old_sidebar = '''    <div class="sidebar-section">
      <div class="sidebar-section-title">Cadastros</div>
      <div class="sidebar-item" onclick="goTo('veiculos',this)" data-page="veiculos">'''

new_sidebar = '''    <div class="sidebar-section">
      <div class="sidebar-section-title">Cadastros</div>
      <div class="sidebar-item" onclick="goTo('veiculos',this)" data-page="veiculos">'''

# Adiciona Produção após Motoristas no sidebar
old_after_mot = '''      <div class="sidebar-item" onclick="goTo('motoristas',this)" data-page="motoristas">'''

# Encontra a linha completa de motoristas
idx_mot = content.find(old_after_mot)
if idx_mot != -1:
    # Encontra o fim do item de motoristas
    idx_end = content.find('</div>', idx_mot) + 6
    new_producao_item = content[idx_mot:idx_end] + '''
      <div class="sidebar-item" onclick="goTo('producao',this)" data-page="producao">
        <span class="icon">📦</span> Produção
      </div>'''
    content = content[:idx_mot] + new_producao_item + content[idx_end:]
    print('Item Produção adicionado no sidebar!')

# ── 2. Adiciona tela de Produção antes da seção de Integração ──────
old_integracao = '''    <!-- ══ INTEGRAÇÃO ══ -->'''

new_producao_page = '''    <!-- ══ PRODUÇÃO ══ -->
    <div class="page" id="page-producao">
      <div class="page-header">
        <div>
          <div class="page-title">Produção</div>
          <div class="page-sub">Cadastro de pallets e itens de gelo</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadProducao()">↺ Atualizar</button>
          <button class="btn btn-primary" id="btn-novo-producao" onclick="abrirModalPallet()">+ Novo Pallet</button>
        </div>
      </div>

      <!-- Filtro Pallet / Item -->
      <div class="filters-bar" style="margin-bottom:16px">
        <div class="filter-group">
          <span class="filter-label">Visualizar</span>
          <div style="display:flex;gap:6px">
            <button id="btn-tab-pallet" onclick="switchProducaoTab('pallet')"
              style="padding:8px 18px;border:2px solid #e8521a;background:rgba(232,82,26,.15);color:#e8521a;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              🪵 Pallets
            </button>
            <button id="btn-tab-item" onclick="switchProducaoTab('item')"
              style="padding:8px 18px;border:2px solid #1e3a5c;background:transparent;color:#90afd4;border-radius:6px;font-size:12px;font-weight:700;cursor:pointer">
              🧊 Itens de Gelo
            </button>
          </div>
        </div>
      </div>

      <!-- SEÇÃO PALLETS -->
      <div id="section-pallets">
        <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">🪵 PALLETS CADASTRADOS</div>
        <div class="card">
          <div class="card-body" style="padding:0;overflow-x:auto">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Comprimento (m)</th>
                  <th>Largura (m)</th>
                  <th>Altura (m)</th>
                  <th>Cubagem (m³)</th>
                  <th>Peso Máx. (kg)</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody id="pallets-tbody">
                <tr><td colspan="8" class="loading-state">Carregando...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- SEÇÃO ITENS -->
      <div id="section-itens" style="display:none">
        <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:10px">🧊 ITENS DE GELO</div>
        <div class="card">
          <div class="card-body" style="padding:0;overflow-x:auto">
            <table>
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Peso (kg)</th>
                  <th>Dimensões</th>
                  <th>Un./Pallet</th>
                  <th>TOP</th>
                  <th>Observação</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody id="itens-tbody">
                <tr><td colspan="7" class="loading-state">Carregando...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- MODAL PALLET -->
      <div id="modal-pallet" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:560px;max-height:90vh;overflow-y:auto">
          <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-pallet-titulo">Novo Pallet</span>
            <button onclick="document.getElementById('modal-pallet').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div style="padding:20px 24px">
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🪵 DIMENSÕES DO PALLET</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Nome *</label>
                <input class="form-control" id="p-nome" placeholder="Pallet Padrão" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Comprimento (m)</label>
                <input class="form-control" type="number" step="0.01" id="p-comp" placeholder="1.20" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcPalletCubagem()">
              </div>
              <div>
                <label class="form-label">Largura (m)</label>
                <input class="form-control" type="number" step="0.01" id="p-larg" placeholder="1.00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcPalletCubagem()">
              </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
              <div>
                <label class="form-label">Altura (m)</label>
                <input class="form-control" type="number" step="0.01" id="p-alt" placeholder="0.15" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c" oninput="calcPalletCubagem()">
              </div>
              <div>
                <label class="form-label">Peso Máximo (kg)</label>
                <input class="form-control" type="number" id="p-peso-max" placeholder="1000" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Cubagem (m³)</label>
                <input class="form-control" id="p-cubagem" readonly style="background:#061020;color:#64B4FF;border-color:#1e3a5c">
              </div>
            </div>
            <div style="margin-bottom:16px">
              <label class="form-label">Observações</label>
              <textarea class="form-control" id="p-obs" rows="2" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c;resize:vertical"></textarea>
            </div>
            <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
              <button onclick="document.getElementById('modal-pallet').style.display='none'" class="btn btn-secondary">Cancelar</button>
              <button onclick="salvarPallet()" class="btn btn-primary">💾 Salvar Pallet</button>
            </div>
          </div>
        </div>
      </div>

      <!-- MODAL ITEM -->
      <div id="modal-item" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:580px;max-height:90vh;overflow-y:auto">
          <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-item-titulo">Novo Item</span>
            <button onclick="document.getElementById('modal-item').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div style="padding:20px 24px">
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🧊 DADOS DO ITEM</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
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
            </div>
            <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
              <button onclick="document.getElementById('modal-item').style.display='none'" class="btn btn-secondary">Cancelar</button>
              <button onclick="salvarItem()" class="btn btn-primary">💾 Salvar Item</button>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ══ INTEGRAÇÃO ══ -->'''

if old_integracao in content:
    content = content.replace(old_integracao, new_producao_page)
    print('Tela de Produção criada!')
else:
    print('ERRO: marcador não encontrado!')

# ── 3. Adiciona JS de Produção ─────────────────────────────────────
new_js = '''
// ── PRODUÇÃO (PALLETS E ITENS) ────────────────────────────────────
let producaoTab = 'pallet';
let palletsData = [];
let itensData   = [];

function switchProducaoTab(tab) {
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
}

function calcPalletCubagem() {
  const c = parseFloat(document.getElementById('p-comp')?.value||0);
  const l = parseFloat(document.getElementById('p-larg')?.value||0);
  const a = parseFloat(document.getElementById('p-alt')?.value||0);
  const el = document.getElementById('p-cubagem');
  if (el && c && l && a) el.value = (c*l*a).toFixed(4) + ' m³';
}

async function loadProducao() {
  if (producaoTab === 'pallet') {
    document.getElementById('pallets-tbody').innerHTML = '<tr><td colspan="8" class="loading-state">Carregando...</td></tr>';
    try {
      palletsData = await api('GET', '/producao/pallets');
      document.getElementById('pallets-tbody').innerHTML = palletsData.length
        ? palletsData.map(p => `<tr>
            <td><b style="color:#64B4FF">${p.nome}</b></td>
            <td>${p.comprimento||'—'} m</td>
            <td>${p.largura||'—'} m</td>
            <td>${p.altura||'—'} m</td>
            <td style="color:#2dd4bf">${p.cubagem||'—'} m³</td>
            <td>${p.peso_max||'—'} kg</td>
            <td><span class="badge active">Ativo</span></td>
            <td style="display:flex;gap:4px">
              <button class="btn btn-sm btn-secondary" onclick="editarPallet('${p.id}')">✏️</button>
              <button class="btn btn-sm btn-secondary" style="color:#f87171" onclick="deletarPallet('${p.id}')">✕</button>
            </td>
          </tr>`).join('')
        : '<tr><td colspan="8" class="loading-state">Nenhum pallet cadastrado</td></tr>';
    } catch(e) { document.getElementById('pallets-tbody').innerHTML = `<tr><td colspan="8" class="loading-state">${e.message}</td></tr>`; }
  } else {
    document.getElementById('itens-tbody').innerHTML = '<tr><td colspan="7" class="loading-state">Carregando...</td></tr>';
    try {
      itensData = await api('GET', '/producao/itens');
      document.getElementById('itens-tbody').innerHTML = itensData.length
        ? itensData.map(i => `<tr>
            <td><b style="color:#64B4FF">🧊 ${i.nome}</b></td>
            <td><b>${i.peso} kg</b></td>
            <td style="font-size:11px;color:#90afd4">${i.comprimento||'—'}×${i.largura||'—'}×${i.altura||'—'} m</td>
            <td style="color:#f59e0b;font-weight:600">${i.un_pallet} un</td>
            <td><span class="badge routed">TOP ${i.top}</span></td>
            <td style="font-size:11px;color:#90afd4">${i.observacao||'—'}</td>
            <td style="display:flex;gap:4px">
              <button class="btn btn-sm btn-secondary" onclick="editarItem('${i.id}')">✏️</button>
              <button class="btn btn-sm btn-secondary" style="color:#f87171" onclick="deletarItem('${i.id}')">✕</button>
            </td>
          </tr>`).join('')
        : '<tr><td colspan="7" class="loading-state">Nenhum item cadastrado</td></tr>';
    } catch(e) { document.getElementById('itens-tbody').innerHTML = `<tr><td colspan="7" class="loading-state">${e.message}</td></tr>`; }
  }
}

function abrirModalPallet(pallet) {
  document.getElementById('modal-pallet-titulo').textContent = pallet ? 'Editar Pallet' : 'Novo Pallet';
  document.getElementById('p-nome').value      = pallet?.nome         || '';
  document.getElementById('p-comp').value      = pallet?.comprimento  || '';
  document.getElementById('p-larg').value      = pallet?.largura      || '';
  document.getElementById('p-alt').value       = pallet?.altura       || '';
  document.getElementById('p-peso-max').value  = pallet?.peso_max     || '';
  document.getElementById('p-cubagem').value   = pallet?.cubagem      || '';
  document.getElementById('p-obs').value       = pallet?.observacao   || '';
  document.getElementById('modal-pallet').dataset.editId = pallet?.id || '';
  document.getElementById('modal-pallet').style.display = 'flex';
}

function abrirModalItem(item) {
  document.getElementById('modal-item-titulo').textContent = item ? 'Editar Item' : 'Novo Item';
  document.getElementById('i-nome').value      = item?.nome       || '';
  document.getElementById('i-peso').value      = item?.peso       || '';
  document.getElementById('i-comp').value      = item?.comprimento|| '';
  document.getElementById('i-larg').value      = item?.largura    || '';
  document.getElementById('i-alt').value       = item?.altura     || '';
  document.getElementById('i-un-pallet').value = item?.un_pallet  || '';
  document.getElementById('i-top').value       = item?.top        || '1000';
  document.getElementById('i-obs').value       = item?.observacao || '';
  document.getElementById('modal-item').dataset.editId = item?.id || '';
  document.getElementById('modal-item').style.display = 'flex';
}

async function salvarPallet() {
  const editId = document.getElementById('modal-pallet').dataset.editId;
  const c = parseFloat(document.getElementById('p-comp').value)||0;
  const l = parseFloat(document.getElementById('p-larg').value)||0;
  const a = parseFloat(document.getElementById('p-alt').value)||0;
  const body = {
    nome:         document.getElementById('p-nome').value,
    comprimento:  c, largura: l, altura: a,
    cubagem:      c&&l&&a ? parseFloat((c*l*a).toFixed(4)) : 0,
    peso_max:     parseFloat(document.getElementById('p-peso-max').value)||0,
    observacao:   document.getElementById('p-obs').value||null,
  };
  if (!body.nome) { toast('Nome é obrigatório!', 'error'); return; }
  try {
    if (editId) await api('PATCH', `/producao/pallets/${editId}`, body);
    else await api('POST', '/producao/pallets', body);
    toast(editId ? 'Pallet atualizado!' : 'Pallet cadastrado!', 'success');
    document.getElementById('modal-pallet').style.display = 'none';
    loadProducao();
  } catch(e) { toast(e.message, 'error'); }
}

async function salvarItem() {
  const editId = document.getElementById('modal-item').dataset.editId;
  const body = {
    nome:         document.getElementById('i-nome').value,
    peso:         parseFloat(document.getElementById('i-peso').value)||0,
    comprimento:  parseFloat(document.getElementById('i-comp').value)||0,
    largura:      parseFloat(document.getElementById('i-larg').value)||0,
    altura:       parseFloat(document.getElementById('i-alt').value)||0,
    un_pallet:    parseInt(document.getElementById('i-un-pallet').value)||0,
    top:          document.getElementById('i-top').value,
    observacao:   document.getElementById('i-obs').value||null,
  };
  if (!body.nome || !body.peso) { toast('Nome e peso são obrigatórios!', 'error'); return; }
  try {
    if (editId) await api('PATCH', `/producao/itens/${editId}`, body);
    else await api('POST', '/producao/itens', body);
    toast(editId ? 'Item atualizado!' : 'Item cadastrado!', 'success');
    document.getElementById('modal-item').style.display = 'none';
    loadProducao();
  } catch(e) { toast(e.message, 'error'); }
}

async function editarPallet(id) {
  const p = palletsData.find(x=>x.id===id);
  if (p) abrirModalPallet(p);
}
async function editarItem(id) {
  const i = itensData.find(x=>x.id===id);
  if (i) abrirModalItem(i);
}
async function deletarPallet(id) {
  if (!confirm('Remover este pallet?')) return;
  try { await api('DELETE', `/producao/pallets/${id}`); toast('Removido!'); loadProducao(); } catch(e) { toast(e.message,'error'); }
}
async function deletarItem(id) {
  if (!confirm('Remover este item?')) return;
  try { await api('DELETE', `/producao/itens/${id}`); toast('Removido!'); loadProducao(); } catch(e) { toast(e.message,'error'); }
}

'''

if 'function switchProducaoTab' not in content:
    content = content.replace('// ── MOTORISTAS E EQUIPE ──', new_js + '// ── MOTORISTAS E EQUIPE ──')
    print('JS de Produção adicionado!')

# ── 4. Adiciona na função goTo o carregamento de produção ──────────
old_goto = "if(page==='motoristas') loadDrivers();"
new_goto = "if(page==='motoristas') loadDrivers();\n  if(page==='producao') { switchProducaoTab('pallet'); }"

if old_goto in content:
    content = content.replace(old_goto, new_goto)
    print('goTo atualizado para produção!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Agora precisamos criar a API de produção.')
print('Faca Ctrl+Shift+R para ver a tela!')
