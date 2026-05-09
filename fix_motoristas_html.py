path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a tela de motoristas
old_page = '''    <!-- ══ MOTORISTAS ══ -->
    <div class="page" id="page-motoristas">
      <div class="page-header">
        <div>
          <div class="page-title">Motoristas e Ajudantes</div>
          <div class="page-sub">Gestão de equipes de entrega</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadDrivers()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="openModal('driver')">+ Novo Motorista</button>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <table>
            <thead><tr><th>Nome</th><th>CPF</th><th>CNH</th><th>Categoria</th><th>Telefone</th><th>Jornada</th><th>Status</th><th>Ações</th></tr></thead>
            <tbody id="drivers-tbody"><tr><td colspan="8" class="loading-state">Carregando...</td></tr></tbody>
          </table>
        </div>
      </div>
    </div>'''

new_page = '''    <!-- ══ MOTORISTAS ══ -->
    <div class="page" id="page-motoristas">
      <div class="page-header">
        <div>
          <div class="page-title">Motoristas e Equipe</div>
          <div class="page-sub">Gestão de motoristas e ajudantes</div>
        </div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-secondary" onclick="loadDrivers()">↺ Atualizar</button>
          <button class="btn btn-primary" onclick="abrirModalMotorista()">+ Novo Cadastro</button>
        </div>
      </div>

      <!-- Filtro por tipo -->
      <div class="filters-bar" style="margin-bottom:12px">
        <div class="filter-group">
          <span class="filter-label">Tipo</span>
          <select class="filter-input" id="f-driver-tipo" onchange="loadDrivers()">
            <option value="">Todos</option>
            <option value="motorista">Motoristas</option>
            <option value="ajudante">Ajudantes</option>
          </select>
        </div>
      </div>

      <div class="card">
        <div class="card-body" style="padding:0;overflow-x:auto">
          <table>
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Nome</th>
                <th>CPF</th>
                <th>CNH</th>
                <th>Categoria</th>
                <th>Telefone</th>
                <th>Custo/Dia</th>
                <th>Veículo Fixo</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody id="drivers-tbody">
              <tr><td colspan="10" class="loading-state">Carregando...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- MODAL MOTORISTA/AJUDANTE COMPLETO -->
      <div id="modal-motorista-completo" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2000;align-items:center;justify-content:center;padding:20px">
        <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-height:90vh;overflow-y:auto">
          <div style="padding:18px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0;z-index:1">
            <span style="font-size:16px;font-weight:700;color:#e8f0fe" id="modal-mot-titulo">Novo Cadastro</span>
            <button onclick="document.getElementById('modal-motorista-completo').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
          </div>
          <div style="padding:20px 24px">

            <!-- Tipo -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">👤 TIPO DE CADASTRO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:20px">
              <div id="btn-tipo-motorista" onclick="selecionarTipoDriver('motorista')"
                style="padding:14px;border:2px solid #e8521a;background:rgba(232,82,26,.15);border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:20px">🚛</div>
                <div style="font-size:13px;font-weight:700;color:#e8521a;margin-top:4px">Motorista</div>
                <div style="font-size:10px;color:#90afd4">Dirige o veículo</div>
              </div>
              <div id="btn-tipo-ajudante" onclick="selecionarTipoDriver('ajudante')"
                style="padding:14px;border:2px solid #1e3a5c;background:transparent;border-radius:8px;text-align:center;cursor:pointer">
                <div style="font-size:20px">👷</div>
                <div style="font-size:13px;font-weight:700;color:#90afd4;margin-top:4px">Ajudante</div>
                <div style="font-size:10px;color:#90afd4">Auxilia nas entregas</div>
              </div>
            </div>
            <input type="hidden" id="d-tipo" value="motorista">

            <!-- Dados pessoais -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">👤 DADOS PESSOAIS</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
              <div style="grid-column:1/-1">
                <label class="form-label">Nome Completo *</label>
                <input class="form-control" id="d-name" placeholder="João da Silva Santos" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">CPF</label>
                <input class="form-control" id="d-cpf" placeholder="000.000.000-00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Telefone</label>
                <input class="form-control" id="d-phone" placeholder="(92) 99999-9999" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Data de Admissão</label>
                <input class="form-control" type="date" id="d-admissao" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
            </div>

            <!-- CNH (só para motorista) -->
            <div id="d-cnh-section">
              <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🪪 HABILITAÇÃO</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
                <div>
                  <label class="form-label">Número CNH</label>
                  <input class="form-control" id="d-cnh" placeholder="00000000000" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                </div>
                <div>
                  <label class="form-label">Categoria CNH</label>
                  <select class="form-control" id="d-cat" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Financeiro -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">💰 CUSTO OPERACIONAL</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">Custo Diário (R$) *</label>
                <input class="form-control" type="number" step="0.01" id="d-daily-cost" placeholder="310.00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                <div style="font-size:10px;color:#90afd4;margin-top:4px">Usado no cálculo da margem operacional</div>
              </div>
              <div>
                <label class="form-label">Veículo Fixo</label>
                <select class="form-control" id="d-veiculo-fixo" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="">— Sem veículo fixo —</option>
                </select>
              </div>
            </div>

            <!-- Observações -->
            <div style="margin-bottom:20px">
              <label class="form-label">Observações</label>
              <textarea class="form-control" id="d-obs" rows="2" placeholder="Informações adicionais..." style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c;resize:vertical"></textarea>
            </div>

            <div style="display:flex;gap:10px;justify-content:flex-end;padding-top:12px;border-top:1px solid #1e3a5c">
              <button onclick="document.getElementById('modal-motorista-completo').style.display='none'" class="btn btn-secondary">Cancelar</button>
              <button onclick="salvarMotoristaCompleto()" class="btn btn-primary">💾 Salvar</button>
            </div>
          </div>
        </div>
      </div>
    </div>'''

if old_page in content:
    content = content.replace(old_page, new_page)
    print('Tela de motoristas atualizada!')
else:
    print('ERRO: padrão não encontrado!')

# Atualiza loadDrivers
idx = content.find('async function loadDrivers(')
if idx != -1:
    depth = 0; started = False; i = idx
    for i in range(idx, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break

    new_load = '''async function loadDrivers() {
  document.getElementById('drivers-tbody').innerHTML = '<tr><td colspan="10" class="loading-state">Carregando...</td></tr>';
  const tipo = document.getElementById('f-driver-tipo')?.value || '';
  try {
    let drivers = await api('GET', '/drivers');
    if (tipo) drivers = drivers.filter(d => d.tipo === tipo);
    document.getElementById('drivers-tbody').innerHTML = drivers.length
      ? drivers.map(x => `<tr>
          <td><span class="badge ${x.tipo==='motorista'?'active':'routed'}">${x.tipo==='motorista'?'🚛 Motorista':'👷 Ajudante'}</span></td>
          <td><b>${x.name}</b></td>
          <td style="font-family:monospace;font-size:11px">${x.cpf||'—'}</td>
          <td style="font-family:monospace;font-size:11px">${x.cnh||'—'}</td>
          <td>${x.cnh_category||'—'}</td>
          <td>${x.phone||'—'}</td>
          <td style="color:#f59e0b;font-weight:600">R$ ${x.daily_cost||'—'}</td>
          <td style="font-size:11px;color:#90afd4">${x.veiculo_fixo||'—'}</td>
          <td><span class="badge ${x.status}">${statusLabel(x.status)}</span></td>
          <td style="display:flex;gap:4px">
            <button class="btn btn-sm btn-secondary" onclick="editarMotorista('${x.id}')">✏️ Editar</button>
            <button class="btn btn-sm btn-secondary" style="color:#f87171;border-color:#f87171" onclick="removerMotorista('${x.id}')">✕</button>
          </td>
        </tr>`).join('')
      : '<tr><td colspan="10" class="loading-state">Nenhum cadastro encontrado</td></tr>';
  } catch(e) { toast(e.message, 'error'); }
}'''
    content = content[:idx] + new_load + content[i+1:]
    print('loadDrivers atualizado!')

# Adiciona funções JS de motoristas
new_js = '''
// ── MOTORISTAS E EQUIPE ───────────────────────────────────────────
function selecionarTipoDriver(tipo) {
  document.getElementById('d-tipo').value = tipo;
  const btnMot = document.getElementById('btn-tipo-motorista');
  const btnAju = document.getElementById('btn-tipo-ajudante');
  const cnhSec = document.getElementById('d-cnh-section');
  if (tipo === 'motorista') {
    btnMot.style.border = '2px solid #e8521a';
    btnMot.style.background = 'rgba(232,82,26,.15)';
    btnMot.querySelector('div:nth-child(2)').style.color = '#e8521a';
    btnAju.style.border = '2px solid #1e3a5c';
    btnAju.style.background = 'transparent';
    btnAju.querySelector('div:nth-child(2)').style.color = '#90afd4';
    if (cnhSec) cnhSec.style.display = 'block';
  } else {
    btnAju.style.border = '2px solid #64B4FF';
    btnAju.style.background = 'rgba(100,180,255,.15)';
    btnAju.querySelector('div:nth-child(2)').style.color = '#64B4FF';
    btnMot.style.border = '2px solid #1e3a5c';
    btnMot.style.background = 'transparent';
    btnMot.querySelector('div:nth-child(2)').style.color = '#90afd4';
    if (cnhSec) cnhSec.style.display = 'none';
  }
}

async function abrirModalMotorista(driver) {
  document.getElementById('modal-mot-titulo').textContent = driver ? 'Editar Cadastro' : 'Novo Cadastro';

  // Limpa campos
  ['d-name','d-cpf','d-phone','d-cnh','d-daily-cost','d-obs','d-admissao'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = driver ? (driver[id.replace('d-','').replace('-','_')] || '') : '';
  });

  // Preenche veículos no select
  const selVeic = document.getElementById('d-veiculo-fixo');
  selVeic.innerHTML = '<option value="">— Sem veículo fixo —</option>';
  try {
    const veics = await api('GET', '/vehicles');
    veics.filter(v=>v.status==='active').forEach(v => {
      selVeic.innerHTML += `<option value="${v.vda||v.plate}">${v.vda||''} — ${v.plate}</option>`;
    });
  } catch(e) {}

  if (driver) {
    document.getElementById('d-name').value        = driver.name          || '';
    document.getElementById('d-cpf').value         = driver.cpf           || '';
    document.getElementById('d-phone').value       = driver.phone         || '';
    document.getElementById('d-cnh').value         = driver.cnh           || '';
    document.getElementById('d-cat').value         = driver.cnh_category  || 'C';
    document.getElementById('d-daily-cost').value  = driver.daily_cost    || '';
    document.getElementById('d-admissao').value    = driver.data_admissao || '';
    document.getElementById('d-obs').value         = driver.observacoes   || '';
    document.getElementById('d-veiculo-fixo').value= driver.veiculo_fixo  || '';
    selecionarTipoDriver(driver.tipo || 'motorista');
    document.getElementById('modal-motorista-completo').dataset.editId = driver.id;
  } else {
    selecionarTipoDriver('motorista');
    delete document.getElementById('modal-motorista-completo').dataset.editId;
  }

  document.getElementById('modal-motorista-completo').style.display = 'flex';
}

async function editarMotorista(id) {
  try {
    const drivers = await api('GET', '/drivers');
    const d = drivers.find(x => x.id === id);
    if (d) abrirModalMotorista(d);
  } catch(e) { toast(e.message, 'error'); }
}

async function salvarMotoristaCompleto() {
  const editId = document.getElementById('modal-motorista-completo').dataset.editId;
  const body = {
    name:          document.getElementById('d-name').value,
    tipo:          document.getElementById('d-tipo').value,
    cpf:           document.getElementById('d-cpf').value || null,
    cnh:           document.getElementById('d-cnh').value || null,
    cnh_category:  document.getElementById('d-cat').value || null,
    phone:         document.getElementById('d-phone').value || null,
    daily_cost:    parseFloat(document.getElementById('d-daily-cost').value) || 0,
    veiculo_fixo:  document.getElementById('d-veiculo-fixo').value || null,
    data_admissao: document.getElementById('d-admissao').value || null,
    observacoes:   document.getElementById('d-obs').value || null,
  };
  if (!body.name) { toast('Nome é obrigatório!', 'error'); return; }
  try {
    if (editId) {
      await api('PATCH', `/drivers/${editId}`, body);
      toast('Cadastro atualizado!', 'success');
    } else {
      await api('POST', '/drivers', body);
      toast('Cadastro realizado!', 'success');
    }
    document.getElementById('modal-motorista-completo').style.display = 'none';
    loadDrivers();
  } catch(e) { toast(e.message, 'error'); }
}

'''

if 'function selecionarTipoDriver' not in content:
    content = content.replace('// ── VEÍCULOS COMPLETO ──', new_js + '// ── VEÍCULOS COMPLETO ──')
    print('Funções de motoristas adicionadas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nHTML atualizado! Faca Ctrl+Shift+R.')
