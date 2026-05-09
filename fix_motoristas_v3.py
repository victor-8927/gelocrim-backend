path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Corrige horário padrão de almoço ───────────────────────────
content = content.replace(
    'placeholder="12:00 - 13:00"',
    'placeholder="12:00 - 13:12"'
)
content = content.replace(
    '"hora_almoco":  Optional[str]   = None',
    '"hora_almoco":  Optional[str]   = "12:00-13:12"'
)
print('Horário almoço corrigido para 12:00-13:12!')

# ── 2. Corrige CNH para aceitar PDF ───────────────────────────────
old_cnh_foto = '''                <div style="border:2px dashed #1e3a5c;border-radius:8px;padding:12px;text-align:center;cursor:pointer" onclick="document.getElementById(\'d-cnh-foto-input\').click()">
                  <img id="d-cnh-foto-preview" src="" style="display:none;width:80px;height:50px;border-radius:4px;object-fit:cover;margin:0 auto 8px">
                  <div id="d-cnh-foto-placeholder" style="color:#90afd4;font-size:12px">🪪 Clique para adicionar CNH</div>
                </div>
                <input type="file" id="d-cnh-foto-input" accept="image/*" style="display:none" onchange="previewFoto(\'d-cnh-foto-input\',\'d-cnh-foto-preview\',\'d-cnh-foto-placeholder\',\'d-cnh-foto-base64\')">
                <input type="hidden" id="d-cnh-foto-base64">'''

new_cnh_foto = '''                <div style="border:2px dashed #1e3a5c;border-radius:8px;padding:12px;text-align:center;cursor:pointer" onclick="document.getElementById(\'d-cnh-foto-input\').click()">
                  <div id="d-cnh-foto-preview" style="display:none;padding:8px;background:#0a1628;border-radius:4px;margin-bottom:8px">
                    <span style="font-size:24px">📄</span>
                    <div id="d-cnh-nome-arquivo" style="font-size:10px;color:#64B4FF;margin-top:4px"></div>
                  </div>
                  <div id="d-cnh-foto-placeholder" style="color:#90afd4;font-size:12px">🪪 Clique para adicionar CNH (PDF ou imagem)</div>
                </div>
                <input type="file" id="d-cnh-foto-input" accept="image/*,.pdf" style="display:none" onchange="uploadCNH()">
                <input type="hidden" id="d-cnh-foto-base64">'''

if old_cnh_foto in content:
    content = content.replace(old_cnh_foto, new_cnh_foto)
    print('Campo CNH atualizado para aceitar PDF!')

# ── 3. Corrige função previewFoto e adiciona uploadCNH ────────────
old_preview = '''function previewFoto(inputId, previewId, placeholderId, base64Id) {
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
}'''

new_preview = '''function previewFoto(inputId, previewId, placeholderId, base64Id) {
  const input = document.getElementById(inputId);
  const file  = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const preview     = document.getElementById(previewId);
    const placeholder = document.getElementById(placeholderId);
    const base64El    = document.getElementById(base64Id);
    preview.src       = e.target.result;
    preview.style.display    = 'block';
    placeholder.style.display = 'none';
    if (base64El) base64El.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

function uploadCNH() {
  const input = document.getElementById('d-cnh-foto-input');
  const file  = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    document.getElementById('d-cnh-foto-base64').value = e.target.result;
    document.getElementById('d-cnh-foto-preview').style.display = 'block';
    document.getElementById('d-cnh-foto-placeholder').style.display = 'none';
    document.getElementById('d-cnh-nome-arquivo').textContent = file.name + ' (' + (file.size/1024).toFixed(0) + ' KB)';
  };
  reader.readAsDataURL(file);
}'''

if old_preview in content:
    content = content.replace(old_preview, new_preview)
    print('previewFoto e uploadCNH corrigidos!')

# ── 4. Corrige salvarMotoristaCompleto com todos os campos ─────────
old_save_body = '''  const body = {
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
  };
  if (!body.name) { toast('Nome é obrigatório!', 'error'); return; }'''

new_save_body = '''  // Validação
  const nome = document.getElementById('d-name').value.trim();
  if (!nome) { toast('Nome é obrigatório!', 'error'); return; }
  const custoDia = parseFloat(document.getElementById('d-daily-cost').value);
  if (!custoDia || custoDia <= 0) { toast('Custo diário é obrigatório!', 'error'); return; }

  const body = {
    name:          nome,
    tipo:          document.getElementById('d-tipo').value,
    cpf:           document.getElementById('d-cpf').value   || null,
    cnh:           document.getElementById('d-cnh').value   || null,
    cnh_category:  document.getElementById('d-cat').value   || null,
    phone:         document.getElementById('d-phone').value || null,
    daily_cost:    custoDia,
    veiculo_fixo:  document.getElementById('d-veiculo-fixo').value  || null,
    data_admissao: document.getElementById('d-admissao').value      || null,
    observacoes:   document.getElementById('d-obs').value           || null,
    foto:          document.getElementById('d-foto-base64').value   || null,
    cnh_foto:      document.getElementById('d-cnh-foto-base64').value || null,
    dia_folga:     document.getElementById('d-dia-folga').value     || null,
    carga_horaria: document.getElementById('d-carga-horaria').value || null,
    hora_almoco:   document.getElementById('d-hora-almoco').value   || null,
  };
  if (!body.name) { toast('Nome é obrigatório!', 'error'); return; }'''

if old_save_body in content:
    content = content.replace(old_save_body, new_save_body)
    print('salvarMotoristaCompleto corrigido com validação!')

# ── 5. Corrige a tabela para mostrar foto e custo ─────────────────
old_td_foto = '''          <td style="display:flex;align-items:center;gap:8px">
            ${x.foto ? `<img src="${x.foto}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;border:2px solid #1e3a5c">` : '<div style="width:32px;height:32px;border-radius:50%;background:#1e3a5c;display:flex;align-items:center;justify-content:center;font-size:14px">👤</div>'}
            <b>${x.name}</b>
          </td>'''

new_td_foto = '''          <td style="display:flex;align-items:center;gap:8px;min-width:160px">
            ${x.foto
              ? `<img src="${x.foto}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid #64B4FF;flex-shrink:0">`
              : `<div style="width:36px;height:36px;border-radius:50%;background:#1e3a5c;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0">${x.tipo==='motorista'?'🚛':'👷'}</div>`}
            <div>
              <div style="font-weight:600;color:#e8f0fe">${x.name}</div>
              <div style="font-size:10px;color:#90afd4">${x.dia_folga ? 'Folga: '+x.dia_folga : ''}</div>
            </div>
          </td>'''

if old_td_foto in content:
    content = content.replace(old_td_foto, new_td_foto)
    print('Foto na tabela corrigida!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
