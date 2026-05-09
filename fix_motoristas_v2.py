path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui o modal completo de motoristas
old_modal_body = '''            <!-- Financeiro -->
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
            </div>'''

new_modal_body = '''            <!-- Fotos -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">📷 FOTOS</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">Foto do Funcionário</label>
                <div style="border:2px dashed #1e3a5c;border-radius:8px;padding:12px;text-align:center;cursor:pointer" onclick="document.getElementById('d-foto-input').click()">
                  <img id="d-foto-preview" src="" style="display:none;width:80px;height:80px;border-radius:50%;object-fit:cover;margin:0 auto 8px">
                  <div id="d-foto-placeholder" style="color:#90afd4;font-size:12px">👤 Clique para adicionar foto</div>
                </div>
                <input type="file" id="d-foto-input" accept="image/*" style="display:none" onchange="previewFoto('d-foto-input','d-foto-preview','d-foto-placeholder','d-foto-base64')">
                <input type="hidden" id="d-foto-base64">
              </div>
              <div id="d-cnh-foto-wrap">
                <label class="form-label">Foto da CNH</label>
                <div style="border:2px dashed #1e3a5c;border-radius:8px;padding:12px;text-align:center;cursor:pointer" onclick="document.getElementById('d-cnh-foto-input').click()">
                  <img id="d-cnh-foto-preview" src="" style="display:none;width:80px;height:50px;border-radius:4px;object-fit:cover;margin:0 auto 8px">
                  <div id="d-cnh-foto-placeholder" style="color:#90afd4;font-size:12px">🪪 Clique para adicionar CNH</div>
                </div>
                <input type="file" id="d-cnh-foto-input" accept="image/*" style="display:none" onchange="previewFoto('d-cnh-foto-input','d-cnh-foto-preview','d-cnh-foto-placeholder','d-cnh-foto-base64')">
                <input type="hidden" id="d-cnh-foto-base64">
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

            <!-- Horários e Folga -->
            <div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:12px">🕐 JORNADA DE TRABALHO</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px">
              <div>
                <label class="form-label">Carga Horária</label>
                <input class="form-control" id="d-carga-horaria" placeholder="07:00 - 17:00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Horário de Almoço</label>
                <input class="form-control" id="d-hora-almoco" placeholder="12:00 - 13:00" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
              </div>
              <div>
                <label class="form-label">Dia de Folga</label>
                <select class="form-control" id="d-dia-folga" style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c">
                  <option value="">— Sem folga fixa —</option>
                  <option value="domingo">Domingo</option>
                  <option value="segunda">Segunda-feira</option>
                  <option value="terca">Terça-feira</option>
                  <option value="quarta">Quarta-feira</option>
                  <option value="quinta">Quinta-feira</option>
                  <option value="sexta">Sexta-feira</option>
                  <option value="sabado">Sábado</option>
                </select>
              </div>
            </div>

            <!-- Observações -->
            <div style="margin-bottom:20px">
              <label class="form-label">Observações</label>
              <textarea class="form-control" id="d-obs" rows="2" placeholder="Informações adicionais..." style="background:#0a1628;color:#e8f0fe;border-color:#1e3a5c;resize:vertical"></textarea>
            </div>'''

if old_modal_body in content:
    content = content.replace(old_modal_body, new_modal_body)
    print('Modal de motoristas atualizado com foto, folga e horários!')
else:
    print('ERRO: padrão modal não encontrado!')

# Atualiza salvarMotoristaCompleto para incluir novos campos
old_save = '''  const body = {
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
  };'''

new_save = '''  const body = {
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
    foto:          document.getElementById('d-foto-base64').value || null,
    cnh_foto:      document.getElementById('d-cnh-foto-base64').value || null,
    dia_folga:     document.getElementById('d-dia-folga').value || null,
    carga_horaria: document.getElementById('d-carga-horaria').value || null,
    hora_almoco:   document.getElementById('d-hora-almoco').value || null,
  };'''

if old_save in content:
    content = content.replace(old_save, new_save)
    print('salvarMotoristaCompleto atualizado!')

# Atualiza abrirModalMotorista para preencher novos campos
old_edit_fields = '''    document.getElementById('d-veiculo-fixo').value= driver.veiculo_fixo  || '';
    selecionarTipoDriver(driver.tipo || 'motorista');'''

new_edit_fields = '''    document.getElementById('d-veiculo-fixo').value  = driver.veiculo_fixo   || '';
    document.getElementById('d-dia-folga').value      = driver.dia_folga      || '';
    document.getElementById('d-carga-horaria').value  = driver.carga_horaria  || '';
    document.getElementById('d-hora-almoco').value    = driver.hora_almoco    || '';
    // Foto preview
    if (driver.foto) {
      document.getElementById('d-foto-preview').src = driver.foto;
      document.getElementById('d-foto-preview').style.display = 'block';
      document.getElementById('d-foto-placeholder').style.display = 'none';
      document.getElementById('d-foto-base64').value = driver.foto;
    }
    selecionarTipoDriver(driver.tipo || 'motorista');'''

if old_edit_fields in content:
    content = content.replace(old_edit_fields, new_edit_fields)
    print('abrirModalMotorista atualizado com novos campos!')

# Adiciona função previewFoto
new_preview = '''
function previewFoto(inputId, previewId, placeholderId, base64Id) {
  const input = document.getElementById(inputId);
  const file  = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const preview     = document.getElementById(previewId);
    const placeholder = document.getElementById(placeholderId);
    const base64El    = document.getElementById(base64Id);
    preview.src       = e.target.result;
    preview.style.display   = 'block';
    placeholder.style.display= 'none';
    if (base64El) base64El.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

'''

if 'function previewFoto' not in content:
    content = content.replace('function selecionarTipoDriver(', new_preview + 'function selecionarTipoDriver(')
    print('previewFoto adicionada!')

# Atualiza tabela de motoristas para mostrar foto
old_row_mot = '''          <td><span class="badge ${x.tipo==='motorista'?'active':'routed'}">${x.tipo==='motorista'?'🚛 Motorista':'👷 Ajudante'}</span></td>
          <td><b>${x.name}</b></td>'''

new_row_mot = '''          <td><span class="badge ${x.tipo==='motorista'?'active':'routed'}">${x.tipo==='motorista'?'🚛 Motorista':'👷 Ajudante'}</span></td>
          <td style="display:flex;align-items:center;gap:8px">
            ${x.foto ? `<img src="${x.foto}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;border:2px solid #1e3a5c">` : '<div style="width:32px;height:32px;border-radius:50%;background:#1e3a5c;display:flex;align-items:center;justify-content:center;font-size:14px">👤</div>'}
            <b>${x.name}</b>
          </td>'''

if old_row_mot in content:
    content = content.replace(old_row_mot, new_row_mot)
    print('Tabela de motoristas atualizada com foto!')

# Adiciona coluna folga na tabela
old_th_mot = '''                <th>Custo/Dia</th>
                <th>Veículo Fixo</th>
                <th>Status</th>'''

new_th_mot = '''                <th>Custo/Dia</th>
                <th>Folga</th>
                <th>Jornada</th>
                <th>Status</th>'''

if old_th_mot in content:
    content = content.replace(old_th_mot, new_th_mot)

old_td_mot = '''          <td style="color:#f59e0b;font-weight:600">R$ ${x.daily_cost||'—'}</td>
          <td style="font-size:11px;color:#90afd4">${x.veiculo_fixo||'—'}</td>
          <td><span class="badge ${x.status}">${statusLabel(x.status)}</span></td>'''

new_td_mot = '''          <td style="color:#f59e0b;font-weight:600">R$ ${x.daily_cost||'—'}</td>
          <td style="font-size:11px;color:#90afd4">${x.dia_folga||'—'}</td>
          <td style="font-size:11px;color:#90afd4">${x.carga_horaria||'—'}</td>
          <td><span class="badge ${x.status}">${statusLabel(x.status)}</span></td>'''

if old_td_mot in content:
    content = content.replace(old_td_mot, new_td_mot)
    print('Colunas folga e jornada adicionadas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Execute fix_db_drivers_v2.py e reinicie o servidor.')
