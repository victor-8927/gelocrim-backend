path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

missing_funcs = '''
// ── FUNÇÕES FALTANDO ─────────────────────────────────────────────

async function abrirModalVeiculo(veiculo) {
  document.getElementById('modal-veic-titulo').textContent = veiculo ? 'Editar Veículo' : 'Novo Veículo';
  const fields = ['v-vda','v-plate','v-model','v-kg','v-m3','v-pallets','v-comp','v-larg','v-alt',
    'v-kml','v-preco-comb','v-ipva','v-manut','v-custo-dia','v-ult-oleo','v-prox-oleo','v-custo-oleo'];
  fields.forEach(id => { const e=document.getElementById(id); if(e) e.value=''; });
  if (veiculo) {
    const s=(id,val)=>{const e=document.getElementById(id);if(e)e.value=val||'';};
    s('v-vda',veiculo.vda); s('v-plate',veiculo.plate); s('v-model',veiculo.model);
    s('v-kg',veiculo.capacity_kg); s('v-m3',veiculo.capacity_m3); s('v-pallets',veiculo.pallets);
    s('v-comp',veiculo.bau_comp); s('v-larg',veiculo.bau_larg); s('v-alt',veiculo.bau_alt);
    s('v-kml',veiculo.km_per_liter); s('v-preco-comb',veiculo.fuel_price);
    s('v-ipva',veiculo.ipva_anual); s('v-manut',veiculo.manut_mes); s('v-custo-dia',veiculo.daily_cost);
    s('v-ult-oleo',veiculo.oleo_ult_data); s('v-prox-oleo',veiculo.oleo_prox_data); s('v-custo-oleo',veiculo.oleo_custo);
    document.getElementById('v-type').value        = veiculo.type      || 'caminhao_truck';
    document.getElementById('v-status').value      = veiculo.status    || 'active';
    document.getElementById('v-combustivel').value = veiculo.fuel_type || 'diesel';
    document.getElementById('modal-veiculo-completo').dataset.editId = veiculo.id;
  } else {
    delete document.getElementById('modal-veiculo-completo').dataset.editId;
  }
  document.getElementById('modal-veiculo-completo').style.display = 'flex';
}

async function editarVeiculo(id) {
  try {
    const veics = await api('GET', '/vehicles');
    const v = veics.find(x => x.id === id);
    if (v) abrirModalVeiculo(v);
  } catch(e) { toast(e.message, 'error'); }
}

async function inativarVeiculo(id) {
  if (!confirm('Inativar este veículo?')) return;
  try {
    await api('PATCH', `/vehicles/${id}`, {status:'inactive'});
    toast('Veículo inativado!', 'success');
    loadVehicles();
  } catch(e) { toast(e.message, 'error'); }
}

async function loadProducao() {
  if (producaoTab === 'pallet') {
    document.getElementById('pallets-tbody').innerHTML = '<tr><td colspan="8" class="loading-state">Carregando...</td></tr>';
    try {
      palletsData = await api('GET', '/producao/pallets');
      document.getElementById('pallets-tbody').innerHTML = palletsData.length
        ? palletsData.map(p=>`<tr>
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
    } catch(e) { document.getElementById('pallets-tbody').innerHTML=`<tr><td colspan="8" class="loading-state">${e.message}</td></tr>`; }
  }

  if (producaoTab === 'item') {
    document.getElementById('itens-tbody').innerHTML = '<tr><td colspan="7" class="loading-state">Carregando...</td></tr>';
    try {
      itensData = await api('GET', '/producao/itens');
      document.getElementById('itens-tbody').innerHTML = itensData.length
        ? itensData.map(i=>`<tr>
            <td><b style="color:#64B4FF">🧊 ${i.nome}</b></td>
            <td><b>${i.peso} kg</b></td>
            <td style="font-size:11px;color:#90afd4">${i.comprimento||'—'}×${i.largura||'—'}×${i.altura||'—'} m</td>
            <td style="color:#f59e0b;font-weight:600">${i.un_pallet||0} un</td>
            <td><span class="badge routed">TOP ${i.top||'1000'}</span></td>
            <td style="font-size:11px;color:#90afd4">${i.observacao||'—'}</td>
            <td style="display:flex;gap:4px">
              <button class="btn btn-sm btn-secondary" onclick="editarItem('${i.id}')">✏️</button>
              <button class="btn btn-sm btn-secondary" style="color:#f87171" onclick="deletarItem('${i.id}')">✕</button>
            </td>
          </tr>`).join('')
        : '<tr><td colspan="7" class="loading-state">Nenhum item cadastrado</td></tr>';
    } catch(e) { document.getElementById('itens-tbody').innerHTML=`<tr><td colspan="7" class="loading-state">${e.message}</td></tr>`; }
  }

  if (producaoTab === 'carregado') {
    try {
      const pallets = await api('GET', '/producao/pallets');
      const carregados = pallets.filter(p => p.observacao && p.observacao.includes('unidades'));
      const grid = document.getElementById('pallets-carregados-grid');
      if (!grid) return;
      if (carregados.length === 0) {
        grid.innerHTML = '<div class="loading-state" style="grid-column:1/-1">Nenhum pallet carregado configurado. Clique em "+ Configurar Pallet"</div>';
        return;
      }
      grid.innerHTML = carregados.map(p=>`
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
}

async function loadDrivers() {
  document.getElementById('drivers-tbody').innerHTML = '<tr><td colspan="10" class="loading-state">Carregando...</td></tr>';
  const tipo = document.getElementById('f-driver-tipo')?.value || '';
  try {
    let drivers = await api('GET', '/drivers');
    if (tipo) drivers = drivers.filter(d => d.tipo === tipo);
    document.getElementById('drivers-tbody').innerHTML = drivers.length
      ? drivers.map(x=>`<tr>
          <td><span class="badge ${x.tipo==='motorista'?'active':'routed'}">${x.tipo==='motorista'?'🚛 Motorista':'👷 Ajudante'}</span></td>
          <td style="display:flex;align-items:center;gap:8px;min-width:160px">
            ${x.foto?`<img src="${x.foto}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid #64B4FF;flex-shrink:0">`
            :`<div style="width:36px;height:36px;border-radius:50%;background:#1e3a5c;display:flex;align-items:center;justify-content:center;font-size:16px">${x.tipo==='motorista'?'🚛':'👷'}</div>`}
            <div>
              <div style="font-weight:600;color:#e8f0fe">${x.name}</div>
              <div style="font-size:10px;color:#90afd4">${x.dia_folga?'Folga: '+x.dia_folga:''}</div>
            </div>
          </td>
          <td style="font-family:monospace;font-size:11px">${x.cpf||'—'}</td>
          <td style="font-family:monospace;font-size:11px">${x.cnh||'—'}</td>
          <td>${x.cnh_category||'—'}</td>
          <td>${x.phone||'—'}</td>
          <td style="color:#f59e0b;font-weight:600">R$ ${x.daily_cost||'—'}</td>
          <td style="font-size:11px;color:#90afd4">${x.dia_folga||'—'}</td>
          <td style="font-size:11px;color:#90afd4">${x.carga_horaria||'—'}</td>
          <td><span class="badge ${x.status}">${statusLabel(x.status)}</span></td>
          <td style="display:flex;gap:4px">
            <button class="btn btn-sm btn-secondary" onclick="editarMotorista('${x.id}')">✏️ Editar</button>
            <button class="btn btn-sm btn-secondary" style="color:#f87171;border-color:#f87171" onclick="removerMotorista('${x.id}')">✕</button>
          </td>
        </tr>`).join('')
      : '<tr><td colspan="10" class="loading-state">Nenhum cadastro encontrado</td></tr>';
  } catch(e) { toast(e.message,'error'); }
}

'''

# Injeta antes do fechamento do script
if 'function abrirModalVeiculo' not in content or 'function loadProducao' not in content:
    content = content.replace('</script>\n</body>', missing_funcs + '\n</script>\n</body>')
    print('Funções faltando adicionadas!')
else:
    print('Funções já existem!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
print('\nTambém reinicie o servidor para carregar o router de produção!')
