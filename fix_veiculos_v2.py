path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui o modal completo de veículos
old_modal = '''          <div style="padding:20px 24px">

            <!-- Identificação -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🚛 IDENTIFICAÇÃO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">Placa *</label>
                <input class="form-control" id="v-plate" placeholder="ABC-1234" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Modelo *</label>
                <input class="form-control" id="v-model" placeholder="Mercedes Axor" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Tipo</label>
                <select class="form-control" id="v-type" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="truck">Caminhão</option>
                  <option value="van">Van</option>
                  <option value="moto">Moto</option>
                </select>
              </div>
            </div>'''

new_modal = '''          <div style="padding:20px 24px">

            <!-- Identificação -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🚛 IDENTIFICAÇÃO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">VDA (Nome do Veículo) *</label>
                <input class="form-control" id="v-vda" placeholder="VDA 01" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Placa *</label>
                <input class="form-control" id="v-plate" placeholder="ABC-1234" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Modelo *</label>
                <input class="form-control" id="v-model" placeholder="Mercedes Axor" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Tipo</label>
                <select class="form-control" id="v-type" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="caminhao_truck">Caminhão Truck</option>
                  <option value="caminhao_toco">Caminhão Toco</option>
                  <option value="cavalo">Cavalo</option>
                  <option value="muck">Muck</option>
                  <option value="accelo">Accelo</option>
                  <option value="hr">HR</option>
                  <option value="troller_20p">Troller 20P</option>
                  <option value="troller_40p">Troller 40P</option>
                  <option value="outros">Outros</option>
                </select>
              </div>
            </div>'''

if old_modal in content:
    content = content.replace(old_modal, new_modal)
    print('Identificação atualizada com VDA e tipos corretos!')
else:
    print('ERRO: padrão identificação não encontrado')

# Corrige campos de óleo para datas + custo
old_oleo = '''            <!-- Manutenção -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🔧 MANUTENÇÃO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">Última troca de óleo (km)</label>
                <input class="form-control" type="number" id="v-ult-oleo" placeholder="50000" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Próxima troca de óleo (km)</label>
                <input class="form-control" type="number" id="v-prox-oleo" placeholder="55000" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
            </div>'''

new_oleo = '''            <!-- Manutenção -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🔧 MANUTENÇÃO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">Data da última troca de óleo</label>
                <input class="form-control" type="date" id="v-ult-oleo" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Data da próxima troca de óleo</label>
                <input class="form-control" type="date" id="v-prox-oleo" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Custo da troca de óleo (R$)</label>
                <input class="form-control" type="number" step="0.01" id="v-custo-oleo" placeholder="450.00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
            </div>'''

if old_oleo in content:
    content = content.replace(old_oleo, new_oleo)
    print('Campos de óleo corrigidos para datas + custo!')
else:
    print('ERRO: padrão óleo não encontrado')

# Corrige a tabela de listagem para mostrar VDA
old_tabela_th = '''            <thead>
              <tr>
                <th>Placa</th>
                <th>Modelo</th>
                <th>Tipo</th>
                <th>Cap. Peso</th>
                <th>Cap. Volume</th>
                <th>Combustível</th>
                <th>KM/L</th>
                <th>Custo/Dia</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>'''

new_tabela_th = '''            <thead>
              <tr>
                <th>VDA</th>
                <th>Placa</th>
                <th>Modelo</th>
                <th>Tipo</th>
                <th>Cap. Peso</th>
                <th>Combustível</th>
                <th>KM/L</th>
                <th>Custo/Dia</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>'''

if old_tabela_th in content:
    content = content.replace(old_tabela_th, new_tabela_th)
    print('Cabeçalho da tabela atualizado com VDA!')

# Corrige loadVehicles para mostrar VDA e tipos corretos
old_row = '''          <td><b style="font-family:'DM Mono',monospace;color:#64B4FF">${x.plate}</b></td>
          <td>${x.model}</td>
          <td>${x.type}</td>
          <td>${x.capacity_kg||0} kg</td>
          <td>${x.capacity_m3||0} m³</td>
          <td style="color:#90afd4">${x.fuel_type||'—'}</td>
          <td style="color:#90afd4">${x.km_per_liter||'—'}</td>
          <td style="color:#f59e0b">R$ ${x.daily_cost||'—'}</td>
          <td><span class="badge ${x.status}">${statusLabel(x.status)}</span></td>
          <td style="display:flex;gap:4px">
            <button class="btn btn-sm btn-secondary" onclick="editarVeiculo('${x.id}')">✏️</button>
            <button class="btn btn-sm btn-secondary" style="color:#f87171" onclick="inativarVeiculo('${x.id}')">⏸</button>
          </td>'''

new_row = '''          <td><b style="color:#64B4FF">${x.vda||'—'}</b></td>
          <td><b style="font-family:'DM Mono',monospace">${x.plate}</b></td>
          <td>${x.model}</td>
          <td style="font-size:11px;color:#90afd4">${tipoVeiculoLabel(x.type)}</td>
          <td>${x.capacity_kg||0} kg</td>
          <td style="color:#90afd4">${x.fuel_type||'—'}</td>
          <td style="color:#90afd4">${x.km_per_liter||'—'} km/L</td>
          <td style="color:#f59e0b">R$ ${x.daily_cost||'—'}</td>
          <td><span class="badge ${x.status}">${statusLabel(x.status)}</span></td>
          <td style="display:flex;gap:4px">
            <button class="btn btn-sm btn-secondary" onclick="editarVeiculo('${x.id}')">✏️ Editar</button>
            <button class="btn btn-sm btn-secondary" style="color:#f87171;border-color:#f87171" onclick="inativarVeiculo('${x.id}')">⏸</button>
          </td>'''

if old_row in content:
    content = content.replace(old_row, new_row)
    print('Linha da tabela atualizada com VDA!')

# Corrige salvarVeiculoCompleto para incluir VDA e novos campos
old_body = '''  const body = {
    plate:        document.getElementById('v-plate').value,
    model:        document.getElementById('v-model').value,
    type:         document.getElementById('v-type').value,
    status:       document.getElementById('v-status').value,
    capacity_kg:  parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:  parseFloat(document.getElementById('v-m3').value)||0,
    pallets:      parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:     parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:     parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:      parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:    document.getElementById('v-combustivel').value,
    km_per_liter: parseFloat(document.getElementById('v-kml').value)||4,
    fuel_price:   parseFloat(document.getElementById('v-preco-comb').value)||6.50,
    ipva_anual:   ipva,
    manut_mes:    manut,
    daily_cost:   parseFloat(custoDia),
    oleo_ult_km:  parseInt(document.getElementById('v-ult-oleo').value)||0,
    oleo_prox_km: parseInt(document.getElementById('v-prox-oleo').value)||0,
  };

  if (!body.plate || !body.model) { toast('Placa e modelo são obrigatórios!', 'error'); return; }'''

new_body = '''  const body = {
    vda:          document.getElementById('v-vda').value,
    plate:        document.getElementById('v-plate').value,
    model:        document.getElementById('v-model').value,
    type:         document.getElementById('v-type').value,
    status:       document.getElementById('v-status').value,
    capacity_kg:  parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:  parseFloat(document.getElementById('v-m3').value)||0,
    pallets:      parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:     parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:     parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:      parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:    document.getElementById('v-combustivel').value,
    km_per_liter: parseFloat(document.getElementById('v-kml').value)||4,
    fuel_price:   parseFloat(document.getElementById('v-preco-comb').value)||6.50,
    ipva_anual:   ipva,
    manut_mes:    manut,
    daily_cost:   parseFloat(custoDia),
    oleo_ult_data:  document.getElementById('v-ult-oleo').value||null,
    oleo_prox_data: document.getElementById('v-prox-oleo').value||null,
    oleo_custo:     parseFloat(document.getElementById('v-custo-oleo').value)||0,
  };

  if (!body.vda)   { toast('VDA é obrigatório!', 'error'); return; }
  if (!body.plate) { toast('Placa é obrigatória!', 'error'); return; }
  if (!body.model) { toast('Modelo é obrigatório!', 'error'); return; }'''

if old_body in content:
    content = content.replace(old_body, new_body)
    print('Body do save atualizado com VDA e datas de óleo!')

# Adiciona função helper tipoVeiculoLabel
old_status_label = 'function statusLabel(s) {'
new_tipo_label = '''function tipoVeiculoLabel(tipo) {
  const labels = {
    'caminhao_truck':'Caminhão Truck', 'caminhao_toco':'Caminhão Toco',
    'cavalo':'Cavalo', 'muck':'Muck', 'accelo':'Accelo', 'hr':'HR',
    'troller_20p':'Troller 20P', 'troller_40p':'Troller 40P',
    'truck':'Caminhão', 'van':'Van', 'moto':'Moto', 'outros':'Outros'
  };
  return labels[tipo] || tipo || '—';
}
function statusLabel(s) {'''

if 'function tipoVeiculoLabel' not in content:
    content = content.replace(old_status_label, new_tipo_label)
    print('tipoVeiculoLabel adicionado!')

# Corrige abrirModalVeiculo para incluir VDA e novos campos
old_edit = '''    document.getElementById('v-plate').value       = veiculo.plate       || '';
    document.getElementById('v-model').value       = veiculo.model       || '';
    document.getElementById('v-type').value        = veiculo.type        || 'truck';
    document.getElementById('v-status').value      = veiculo.status      || 'active';
    document.getElementById('v-kg').value          = veiculo.capacity_kg || '';
    document.getElementById('v-m3').value          = veiculo.capacity_m3 || '';
    document.getElementById('v-pallets').value     = veiculo.pallets     || '';
    document.getElementById('v-comp').value        = veiculo.bau_comp    || '';
    document.getElementById('v-larg').value        = veiculo.bau_larg    || '';
    document.getElementById('v-alt').value         = veiculo.bau_alt     || '';
    document.getElementById('v-combustivel').value = veiculo.fuel_type   || 'diesel';
    document.getElementById('v-kml').value         = veiculo.km_per_liter|| '';
    document.getElementById('v-preco-comb').value  = veiculo.fuel_price  || '';
    document.getElementById('v-ipva').value        = veiculo.ipva_anual  || '';
    document.getElementById('v-manut').value       = veiculo.manut_mes   || '';
    document.getElementById('v-custo-dia').value   = veiculo.daily_cost  || '';
    document.getElementById('v-ult-oleo').value    = veiculo.oleo_ult_km || '';
    document.getElementById('v-prox-oleo').value   = veiculo.oleo_prox_km|| '';
    document.getElementById('modal-veiculo-completo').dataset.editId = veiculo.id;'''

new_edit = '''    document.getElementById('v-vda').value          = veiculo.vda         || '';
    document.getElementById('v-plate').value       = veiculo.plate       || '';
    document.getElementById('v-model').value       = veiculo.model       || '';
    document.getElementById('v-type').value        = veiculo.type        || 'caminhao_truck';
    document.getElementById('v-status').value      = veiculo.status      || 'active';
    document.getElementById('v-kg').value          = veiculo.capacity_kg || '';
    document.getElementById('v-m3').value          = veiculo.capacity_m3 || '';
    document.getElementById('v-pallets').value     = veiculo.pallets     || '';
    document.getElementById('v-comp').value        = veiculo.bau_comp    || '';
    document.getElementById('v-larg').value        = veiculo.bau_larg    || '';
    document.getElementById('v-alt').value         = veiculo.bau_alt     || '';
    document.getElementById('v-combustivel').value = veiculo.fuel_type   || 'diesel';
    document.getElementById('v-kml').value         = veiculo.km_per_liter|| '';
    document.getElementById('v-preco-comb').value  = veiculo.fuel_price  || '';
    document.getElementById('v-ipva').value        = veiculo.ipva_anual  || '';
    document.getElementById('v-manut').value       = veiculo.manut_mes   || '';
    document.getElementById('v-custo-dia').value   = veiculo.daily_cost  || '';
    document.getElementById('v-ult-oleo').value    = veiculo.oleo_ult_data  || '';
    document.getElementById('v-prox-oleo').value   = veiculo.oleo_prox_data || '';
    document.getElementById('v-custo-oleo').value  = veiculo.oleo_custo     || '';
    document.getElementById('modal-veiculo-completo').dataset.editId = veiculo.id;'''

if old_edit in content:
    content = content.replace(old_edit, new_edit)
    print('abrirModalVeiculo corrigido com VDA e datas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
