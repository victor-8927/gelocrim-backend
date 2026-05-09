path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── Funções de Veículos ────────────────────────────────────────────
veiculos_js = '''
function calcularCubagem() {
  const c = parseFloat(document.getElementById('v-comp')?.value||0);
  const l = parseFloat(document.getElementById('v-larg')?.value||0);
  const a = parseFloat(document.getElementById('v-alt')?.value||0);
  const el = document.getElementById('v-cubagem-calc');
  if (!el) return;
  if (c && l && a) {
    const cub = (c * l * a).toFixed(2);
    el.textContent = `Cubagem calculada: ${cub} m³`;
    const vm3 = document.getElementById('v-m3');
    if (vm3 && !vm3.value) vm3.value = cub;
    calcularCustoDia();
  } else {
    el.textContent = 'Cubagem calculada: — m³ (preencha as dimensões)';
  }
}
function calcularCustoDia() {
  const ipva  = parseFloat(document.getElementById('v-ipva')?.value||0);
  const manut = parseFloat(document.getElementById('v-manut')?.value||0);
  const el = document.getElementById('v-custo-dia');
  if (el) el.value = ((ipva/365) + (manut/30)).toFixed(2);
}
function toggleMotivoParada() {
  const status = document.getElementById('v-status')?.value;
  const wrap   = document.getElementById('v-motivo-wrap');
  if (wrap) wrap.style.display = (status==='maintenance'||status==='inactive') ? 'block' : 'none';
}
function tipoVeiculoLabel(tipo) {
  const labels = {
    'caminhao_truck':'Caminhão Truck','caminhao_toco':'Caminhão Toco',
    'cavalo':'Cavalo','muck':'Muck','accelo':'Accelo','hr':'HR',
    'troller_20p':'Troller 20P','troller_40p':'Troller 40P',
    'truck':'Caminhão','van':'Van','moto':'Moto','outros':'Outros'
  };
  return labels[tipo] || tipo || '—';
}
function abrirModalVeiculo(veiculo) {
  document.getElementById('modal-veic-titulo').textContent = veiculo ? 'Editar Veículo' : 'Novo Veículo';
  ['v-vda','v-plate','v-model','v-kg','v-m3','v-pallets','v-comp','v-larg','v-alt',
   'v-kml','v-preco-comb','v-ipva','v-manut','v-custo-dia','v-ult-oleo','v-prox-oleo','v-custo-oleo'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  if (veiculo) {
    const s = (id,val) => { const e=document.getElementById(id); if(e) e.value=val||''; };
    s('v-vda',veiculo.vda); s('v-plate',veiculo.plate); s('v-model',veiculo.model);
    s('v-kg',veiculo.capacity_kg); s('v-m3',veiculo.capacity_m3); s('v-pallets',veiculo.pallets);
    s('v-comp',veiculo.bau_comp); s('v-larg',veiculo.bau_larg); s('v-alt',veiculo.bau_alt);
    s('v-kml',veiculo.km_per_liter); s('v-preco-comb',veiculo.fuel_price);
    s('v-ipva',veiculo.ipva_anual); s('v-manut',veiculo.manut_mes); s('v-custo-dia',veiculo.daily_cost);
    s('v-ult-oleo',veiculo.oleo_ult_data); s('v-prox-oleo',veiculo.oleo_prox_data); s('v-custo-oleo',veiculo.oleo_custo);
    document.getElementById('v-type').value        = veiculo.type || 'caminhao_truck';
    document.getElementById('v-status').value      = veiculo.status || 'active';
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
async function salvarVeiculoCompleto() {
  const editId = document.getElementById('modal-veiculo-completo').dataset.editId;
  const ipva   = parseFloat(document.getElementById('v-ipva').value||0);
  const manut  = parseFloat(document.getElementById('v-manut').value||0);
  const body = {
    vda: document.getElementById('v-vda').value,
    plate: document.getElementById('v-plate').value,
    model: document.getElementById('v-model').value,
    type: document.getElementById('v-type').value,
    status: document.getElementById('v-status').value,
    capacity_kg: parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3: parseFloat(document.getElementById('v-m3').value)||0,
    pallets: parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp: parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg: parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt: parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type: document.getElementById('v-combustivel').value,
    km_per_liter: parseFloat(document.getElementById('v-kml').value)||4,
    fuel_price: parseFloat(document.getElementById('v-preco-comb').value)||6.50,
    ipva_anual: ipva, manut_mes: manut,
    daily_cost: parseFloat(((ipva/365)+(manut/30)).toFixed(2)),
    oleo_ult_data: document.getElementById('v-ult-oleo').value||null,
    oleo_prox_data: document.getElementById('v-prox-oleo').value||null,
    oleo_custo: parseFloat(document.getElementById('v-custo-oleo').value)||0,
  };
  if (!body.vda)   { toast('VDA é obrigatório!', 'error'); return; }
  if (!body.plate) { toast('Placa é obrigatória!', 'error'); return; }
  if (!body.model) { toast('Modelo é obrigatório!', 'error'); return; }
  try {
    if (editId) await api('PATCH', `/vehicles/${editId}`, body);
    else await api('POST', '/vehicles', body);
    toast(editId ? 'Veículo atualizado!' : 'Veículo cadastrado!', 'success');
    document.getElementById('modal-veiculo-completo').style.display = 'none';
    loadVehicles();
  } catch(e) { toast(e.message, 'error'); }
}
async function loadVehicles() {
  document.getElementById('vehicles-tbody').innerHTML = '<tr><td colspan="10" class="loading-state">Carregando...</td></tr>';
  try {
    const v = await api('GET', '/vehicles');
    document.getElementById('vehicles-tbody').innerHTML = v.length
      ? v.map(x=>`<tr>
          <td><b style="color:#64B4FF">${x.vda||'—'}</b></td>
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
          </td>
        </tr>`).join('')
      : '<tr><td colspan="10" class="loading-state">Nenhum veículo cadastrado</td></tr>';
  } catch(e) { toast(e.message,'error'); }
}
'''

# ── Funções de Motoristas ─────────────────────────────────────────
motoristas_js = '''
function previewFoto(inputId, previewId, placeholderId, base64Id) {
  const input = document.getElementById(inputId);
  const file  = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const preview     = document.getElementById(previewId);
    const placeholder = document.getElementById(placeholderId);
    const base64El    = document.getElementById(base64Id);
    if (preview) { preview.src = e.target.result; preview.style.display = 'block'; }
    if (placeholder) placeholder.style.display = 'none';
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
}
function selecionarTipoDriver(tipo) {
  document.getElementById('d-tipo').value = tipo;
  const btnMot = document.getElementById('btn-tipo-motorista');
  const btnAju = document.getElementById('btn-tipo-ajudante');
  const cnhSec = document.getElementById('d-cnh-section');
  if (tipo === 'motorista') {
    if(btnMot){btnMot.style.border='2px solid #e8521a';btnMot.style.background='rgba(232,82,26,.15)';btnMot.querySelector('div:nth-child(2)').style.color='#e8521a';}
    if(btnAju){btnAju.style.border='2px solid #1e3a5c';btnAju.style.background='transparent';btnAju.querySelector('div:nth-child(2)').style.color='#90afd4';}
    if(cnhSec) cnhSec.style.display='block';
  } else {
    if(btnAju){btnAju.style.border='2px solid #64B4FF';btnAju.style.background='rgba(100,180,255,.15)';btnAju.querySelector('div:nth-child(2)').style.color='#64B4FF';}
    if(btnMot){btnMot.style.border='2px solid #1e3a5c';btnMot.style.background='transparent';btnMot.querySelector('div:nth-child(2)').style.color='#90afd4';}
    if(cnhSec) cnhSec.style.display='none';
  }
}
async function abrirModalMotorista(driver) {
  document.getElementById('modal-mot-titulo').textContent = driver ? 'Editar Cadastro' : 'Novo Cadastro';
  ['d-name','d-cpf','d-phone','d-cnh','d-daily-cost','d-obs','d-admissao','d-carga-horaria','d-hora-almoco'].forEach(id => {
    const el = document.getElementById(id); if(el) el.value = '';
  });
  const selVeic = document.getElementById('d-veiculo-fixo');
  selVeic.innerHTML = '<option value="">— Sem veículo fixo —</option>';
  try {
    const veics = await api('GET', '/vehicles');
    veics.filter(v=>v.status==='active').forEach(v => {
      selVeic.innerHTML += `<option value="${v.vda||v.plate}">${v.vda||''} — ${v.plate}</option>`;
    });
  } catch(e) {}
  if (driver) {
    const s = (id,val) => { const e=document.getElementById(id); if(e) e.value=val||''; };
    s('d-name',driver.name); s('d-cpf',driver.cpf); s('d-phone',driver.phone);
    s('d-cnh',driver.cnh); s('d-daily-cost',driver.daily_cost); s('d-admissao',driver.data_admissao);
    s('d-obs',driver.observacoes); s('d-carga-horaria',driver.carga_horaria); s('d-hora-almoco',driver.hora_almoco);
    document.getElementById('d-cat').value = driver.cnh_category || 'C';
    document.getElementById('d-veiculo-fixo').value = driver.veiculo_fixo || '';
    document.getElementById('d-dia-folga').value    = driver.dia_folga || '';
    if (driver.foto) {
      document.getElementById('d-foto-preview').src = driver.foto;
      document.getElementById('d-foto-preview').style.display = 'block';
      document.getElementById('d-foto-placeholder').style.display = 'none';
      document.getElementById('d-foto-base64').value = driver.foto;
    }
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
  const nome = document.getElementById('d-name').value.trim();
  if (!nome) { toast('Nome é obrigatório!', 'error'); return; }
  const custoDia = parseFloat(document.getElementById('d-daily-cost').value);
  if (!custoDia || custoDia <= 0) { toast('Custo diário é obrigatório!', 'error'); return; }
  const body = {
    name: nome, tipo: document.getElementById('d-tipo').value,
    cpf: document.getElementById('d-cpf').value||null,
    cnh: document.getElementById('d-cnh').value||null,
    cnh_category: document.getElementById('d-cat').value||null,
    phone: document.getElementById('d-phone').value||null,
    daily_cost: custoDia,
    veiculo_fixo: document.getElementById('d-veiculo-fixo').value||null,
    data_admissao: document.getElementById('d-admissao').value||null,
    observacoes: document.getElementById('d-obs').value||null,
    foto: document.getElementById('d-foto-base64').value||null,
    cnh_foto: document.getElementById('d-cnh-foto-base64').value||null,
    dia_folga: document.getElementById('d-dia-folga').value||null,
    carga_horaria: document.getElementById('d-carga-horaria').value||null,
    hora_almoco: document.getElementById('d-hora-almoco').value||null,
  };
  try {
    if (editId) await api('PATCH', `/drivers/${editId}`, body);
    else await api('POST', '/drivers', body);
    toast(editId ? 'Cadastro atualizado!' : 'Cadastro realizado!', 'success');
    document.getElementById('modal-motorista-completo').style.display = 'none';
    loadDrivers();
  } catch(e) { toast(e.message, 'error'); }
}
async function removerMotorista(id) {
  if (!confirm('Remover este cadastro?')) return;
  try { await api('DELETE', `/drivers/${id}`); toast('Removido!'); loadDrivers(); } catch(e) { toast(e.message,'error'); }
}
'''

# ── Funções de Produção ───────────────────────────────────────────
producao_js = '''
let producaoTab = 'pallet';
let palletsData = [];
let itensData   = [];
const unPorPallet = {5:180, 10:110, 20:50, 40:27};
let pcTipoSelecionado = 5;

function switchProducaoTab(tab) {
  producaoTab = tab;
  const cores = {pallet:'#e8521a', item:'#64B4FF', carregado:'#a78bfa'};
  ['pallet','item','carregado'].forEach(t => {
    const btn = document.getElementById(`btn-tab-${t}`);
    if (!btn) return;
    if (t === tab) {
      btn.style.border = `2px solid ${cores[t]}`;
      btn.style.background = `rgba(${t==='pallet'?'232,82,26':t==='item'?'100,180,255':'167,139,250'},.15)`;
      btn.style.color = cores[t];
    } else {
      btn.style.border = '2px solid #1e3a5c'; btn.style.background = 'transparent'; btn.style.color = '#90afd4';
    }
  });
  document.getElementById('section-pallets').style.display    = tab==='pallet'    ? 'block' : 'none';
  document.getElementById('section-itens').style.display      = tab==='item'      ? 'block' : 'none';
  document.getElementById('section-carregado').style.display  = tab==='carregado' ? 'block' : 'none';
  const btnNovo = document.getElementById('btn-novo-producao');
  if (tab==='pallet')    { btnNovo.textContent='+ Novo Pallet';       btnNovo.onclick=()=>abrirModalPallet(); }
  if (tab==='item')      { btnNovo.textContent='+ Novo Item';         btnNovo.onclick=()=>abrirModalItem(); }
  if (tab==='carregado') { btnNovo.textContent='+ Configurar Pallet'; btnNovo.onclick=()=>abrirModalPalletCarregado(); }
  loadProducao();
}
function calcPalletCubagem() {
  const c=parseFloat(document.getElementById('p-comp')?.value||0);
  const l=parseFloat(document.getElementById('p-larg')?.value||0);
  const a=parseFloat(document.getElementById('p-alt')?.value||0);
  const el=document.getElementById('p-cubagem');
  if(el&&c&&l&&a) el.value=(c*l*a).toFixed(4)+' m³';
}
function calcItemCubagem() {
  const c=parseFloat(document.getElementById('i-comp')?.value||0);
  const l=parseFloat(document.getElementById('i-larg')?.value||0);
  const a=parseFloat(document.getElementById('i-alt')?.value||0);
  const el=document.getElementById('i-cubagem');
  if(el&&c&&l&&a) el.value=(c*l*a).toFixed(6)+' m³';
}
function selecionarTipoPallet(kg) {
  pcTipoSelecionado = kg;
  [5,10,20,40].forEach(k => {
    const el = document.getElementById(`pc-tipo-${k}`);
    if (!el) return;
    el.style.border = k===kg ? '2px solid #64B4FF' : '2px solid #1e3a5c';
    el.style.background = k===kg ? 'rgba(100,180,255,.15)' : 'transparent';
  });
  document.getElementById('pc-tipo-kg').value = kg;
  calcPalletCarregado();
}
function calcPalletCarregado() {
  const kg  = parseInt(document.getElementById('pc-tipo-kg')?.value||5);
  const un  = unPorPallet[kg] || 0;
  const selP = document.getElementById('pc-pallet-sel');
  const pOpt = selP?.options[selP?.selectedIndex];
  const pPeso = parseFloat(pOpt?.dataset?.peso||0);
  const pCub  = parseFloat(pOpt?.dataset?.cub||0);
  const selI = document.getElementById('pc-item-sel');
  const iOpt = selI?.options[selI?.selectedIndex];
  const iPeso = parseFloat(iOpt?.dataset?.peso||kg);
  const iCub  = parseFloat(iOpt?.dataset?.cub||0);
  const pesoTotal = pPeso + (un * iPeso);
  const cubTotal  = pCub  + (un * iCub);
  const capPct = Math.min(100, Math.round(pesoTotal / Math.max(pPeso||1000,1) * 100));
  const el = (id,val) => { const e=document.getElementById(id); if(e) e.textContent=val; };
  el('pc-res-un',      un+' un');
  el('pc-res-peso',    pesoTotal.toFixed(1)+' kg');
  el('pc-res-peso-det',`base: ${pPeso}kg + itens: ${(un*iPeso).toFixed(0)}kg`);
  el('pc-res-cub',     cubTotal.toFixed(4)+' m³');
  el('pc-res-cub-det', `base: ${pCub}m³ + itens: ${(un*iCub).toFixed(4)}m³`);
  el('pc-res-cap-pct', capPct+'%');
  const bar = document.getElementById('pc-res-cap-bar');
  if (bar) { bar.style.width=capPct+'%'; bar.style.background=capPct>=90?'#f87171':capPct>=70?'#f59e0b':'#64B4FF'; }
}
async function abrirModalPalletCarregado() {
  selecionarTipoPallet(5);
  document.getElementById('pc-comp').value='1.20';
  document.getElementById('pc-larg').value='1.00';
  document.getElementById('pc-alt').value='1.50';
  try {
    const [pallets,itens] = await Promise.all([api('GET','/producao/pallets'),api('GET','/producao/itens')]);
    const selP = document.getElementById('pc-pallet-sel');
    const selI = document.getElementById('pc-item-sel');
    selP.innerHTML = '<option value="">— Selecione o pallet —</option>';
    selI.innerHTML = '<option value="">— Selecione o item —</option>';
    pallets.filter(p=>!p.observacao?.includes('unidades')).forEach(p => {
      selP.innerHTML += `<option value="${p.id}" data-peso="${p.peso_max||0}" data-cub="${p.cubagem||0}">${p.nome}</option>`;
    });
    itens.forEach(i => {
      selI.innerHTML += `<option value="${i.id}" data-peso="${i.peso||0}" data-cub="${(i.comprimento||0)*(i.largura||0)*(i.altura||0)}" data-nome="${i.nome}">${i.nome} — ${i.peso}kg</option>`;
    });
  } catch(e) {}
  calcPalletCarregado();
  document.getElementById('modal-pallet-carregado').style.display='flex';
}
async function salvarPalletCarregado() {
  const kg   = parseInt(document.getElementById('pc-tipo-kg').value||5);
  const un   = unPorPallet[kg]||0;
  const selP = document.getElementById('pc-pallet-sel');
  const selI = document.getElementById('pc-item-sel');
  const pOpt = selP?.options[selP?.selectedIndex];
  const iOpt = selI?.options[selI?.selectedIndex];
  const c=parseFloat(document.getElementById('pc-comp').value||1.20);
  const l=parseFloat(document.getElementById('pc-larg').value||1.00);
  const a=parseFloat(document.getElementById('pc-alt').value||1.50);
  const pPeso=parseFloat(pOpt?.dataset?.peso||0);
  const pCub=parseFloat(pOpt?.dataset?.cub||0);
  const iPeso=parseFloat(iOpt?.dataset?.peso||kg);
  const iNome=iOpt?.dataset?.nome||`${kg}kg`;
  const iCub=parseFloat(iOpt?.dataset?.cub||0);
  const body = {
    nome:`Pallet ${iNome} carregado`, comprimento:c, largura:l, altura:a,
    cubagem:parseFloat((pCub+(un*iCub)).toFixed(4)),
    peso_max:pPeso+(un*iPeso),
    observacao:`${un} unidades de ${iNome} | Peso: ${(pPeso+(un*iPeso)).toFixed(0)}kg`
  };
  try {
    await api('POST','/producao/pallets',body);
    toast(`Pallet ${iNome} configurado!`,'success');
    document.getElementById('modal-pallet-carregado').style.display='none';
    loadProducao();
  } catch(e) { toast(e.message,'error'); }
}
function abrirModalPallet(pallet) {
  document.getElementById('modal-pallet-titulo').textContent = pallet ? 'Editar Pallet' : 'Novo Pallet';
  const s=(id,val)=>{const e=document.getElementById(id);if(e)e.value=val||'';};
  s('p-nome',pallet?.nome); s('p-comp',pallet?.comprimento); s('p-larg',pallet?.largura);
  s('p-alt',pallet?.altura); s('p-peso-max',pallet?.peso_max); s('p-cubagem',pallet?.cubagem); s('p-obs',pallet?.observacao);
  document.getElementById('modal-pallet').dataset.editId = pallet?.id||'';
  document.getElementById('modal-pallet').style.display='flex';
}
function abrirModalItem(item) {
  document.getElementById('modal-item-titulo').textContent = item ? 'Editar Item' : 'Novo Item';
  const s=(id,val)=>{const e=document.getElementById(id);if(e)e.value=val||'';};
  s('i-nome',item?.nome); s('i-peso',item?.peso); s('i-comp',item?.comprimento);
  s('i-larg',item?.largura); s('i-alt',item?.altura); s('i-obs',item?.observacao);
  document.getElementById('modal-item').dataset.editId = item?.id||'';
  document.getElementById('modal-item').style.display='flex';
}
async function salvarPallet() {
  const editId = document.getElementById('modal-pallet').dataset.editId;
  const c=parseFloat(document.getElementById('p-comp').value)||0;
  const l=parseFloat(document.getElementById('p-larg').value)||0;
  const a=parseFloat(document.getElementById('p-alt').value)||0;
  const body = {
    nome:document.getElementById('p-nome').value,
    comprimento:c,largura:l,altura:a,
    cubagem:c&&l&&a?parseFloat((c*l*a).toFixed(4)):0,
    peso_max:parseFloat(document.getElementById('p-peso-max').value)||0,
    observacao:document.getElementById('p-obs').value||null,
  };
  if(!body.nome){toast('Nome é obrigatório!','error');return;}
  try {
    if(editId) await api('PATCH',`/producao/pallets/${editId}`,body);
    else await api('POST','/producao/pallets',body);
    toast(editId?'Pallet atualizado!':'Pallet cadastrado!','success');
    document.getElementById('modal-pallet').style.display='none';
    loadProducao();
  } catch(e){toast(e.message,'error');}
}
async function salvarItem() {
  const editId = document.getElementById('modal-item').dataset.editId;
  const body = {
    nome:document.getElementById('i-nome').value,
    peso:parseFloat(document.getElementById('i-peso').value)||0,
    comprimento:parseFloat(document.getElementById('i-comp').value)||0,
    largura:parseFloat(document.getElementById('i-larg').value)||0,
    altura:parseFloat(document.getElementById('i-alt').value)||0,
    un_pallet:parseInt(document.getElementById('i-un-pallet').value)||0,
    top:document.getElementById('i-top').value||'1000',
    observacao:document.getElementById('i-obs').value||null,
  };
  if(!body.nome||!body.peso){toast('Nome e peso são obrigatórios!','error');return;}
  try {
    if(editId) await api('PATCH',`/producao/itens/${editId}`,body);
    else await api('POST','/producao/itens',body);
    toast(editId?'Item atualizado!':'Item cadastrado!','success');
    document.getElementById('modal-item').style.display='none';
    loadProducao();
  } catch(e){toast(e.message,'error');}
}
async function editarPallet(id){const p=palletsData.find(x=>x.id===id);if(p)abrirModalPallet(p);}
async function editarItem(id){const i=itensData.find(x=>x.id===id);if(i)abrirModalItem(i);}
async function deletarPallet(id){if(!confirm('Remover?'))return;try{await api('DELETE',`/producao/pallets/${id}`);toast('Removido!');loadProducao();}catch(e){toast(e.message,'error');}}
async function deletarItem(id){if(!confirm('Remover?'))return;try{await api('DELETE',`/producao/itens/${id}`);toast('Removido!');loadProducao();}catch(e){toast(e.message,'error');}}
'''

# ── Funções de Ocorrências ────────────────────────────────────────
ocorrencias_js = '''
let _ocorrencias = [];
let _ocGravSel   = 'info';
let _assinaturaCtx = null;
let _assinaturaDrawing = false;

function selecionarGravidade(grav) {
  _ocGravSel = grav;
  const cores = {info:'#10b981',media:'#f59e0b',alta:'#f97316',critica:'#f87171'};
  ['info','media','alta','critica'].forEach(g => {
    const el = document.getElementById('grav-'+g); if(!el) return;
    if(g===grav){
      el.style.border=`2px solid ${cores[g]}`;
      el.style.background=`rgba(${g==='info'?'16,185,129':g==='media'?'245,158,11':g==='alta'?'249,115,22':'248,113,113'},.15)`;
      el.querySelector('div:nth-child(2)').style.color=cores[g];
    } else {
      el.style.border='2px solid #1e3a5c'; el.style.background='transparent';
      el.querySelector('div:nth-child(2)').style.color='#90afd4';
    }
  });
  document.getElementById('oc-gravidade-sel').value=grav;
}
function initAssinatura() {
  const canvas = document.getElementById('oc-assinatura'); if(!canvas) return;
  const ctx = canvas.getContext('2d'); _assinaturaCtx=ctx;
  ctx.strokeStyle='#64B4FF'; ctx.lineWidth=2; ctx.lineCap='round';
  const getPos=(e)=>{const r=canvas.getBoundingClientRect();const src=e.touches?e.touches[0]:e;return{x:src.clientX-r.left,y:src.clientY-r.top};};
  canvas.onmousedown=canvas.ontouchstart=(e)=>{e.preventDefault();_assinaturaDrawing=true;const p=getPos(e);ctx.beginPath();ctx.moveTo(p.x,p.y);};
  canvas.onmousemove=canvas.ontouchmove=(e)=>{if(!_assinaturaDrawing)return;e.preventDefault();const p=getPos(e);ctx.lineTo(p.x,p.y);ctx.stroke();};
  canvas.onmouseup=canvas.ontouchend=()=>{_assinaturaDrawing=false;};
}
function limparAssinatura(){const c=document.getElementById('oc-assinatura');if(c&&_assinaturaCtx)_assinaturaCtx.clearRect(0,0,c.width,c.height);}
async function abrirModalOcorrencia(oc) {
  selecionarGravidade('info');
  document.getElementById('modal-oc-titulo').textContent=oc?'Editar Ocorrência':'Nova Ocorrência';
  ['oc-pedido','oc-cliente','oc-descricao'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
  document.getElementById('oc-tipo-novo').value=oc?.tipo||'';
  const selV=document.getElementById('oc-veiculo-novo');
  if(selV){
    selV.innerHTML='<option value="">— Selecione —</option>';
    try{const veics=await api('GET','/vehicles');veics.filter(v=>v.status==='active').forEach(v=>{selV.innerHTML+=`<option value="${v.id}">${v.vda||v.plate} — ${v.plate}</option>`;});}catch(e){}
  }
  if(oc){
    const s=(id,val)=>{const e=document.getElementById(id);if(e)e.value=val||'';};
    s('oc-pedido',oc.pedido);s('oc-cliente',oc.cliente);s('oc-descricao',oc.descricao);
    selecionarGravidade(oc.gravidade||'info');
    document.getElementById('modal-ocorrencia').dataset.editId=oc.id;
  } else { delete document.getElementById('modal-ocorrencia').dataset.editId; }
  limparAssinatura();
  document.getElementById('oc-foto-preview').style.display='none';
  document.getElementById('oc-foto-placeholder').style.display='block';
  document.getElementById('oc-foto-base64').value='';
  document.getElementById('modal-ocorrencia').style.display='flex';
  setTimeout(initAssinatura,100);
}
function filtrarOcorrencia(status){const sel=document.getElementById('oc-status');if(sel){sel.value=status;loadOcorrencias();}}
function tempoDecorrido(createdAt){if(!createdAt)return'—';const diff=(Date.now()-new Date(createdAt))/60000;if(diff<60)return Math.floor(diff)+'min';return(diff/60).toFixed(1)+'h';}
function gravBadge(g){const m={info:'🟢',media:'🟡',alta:'🟠',critica:'🔴'};return`<span style="font-size:16px">${m[g]||'⚪'}</span>`;}
function tipoOcLabel(tipo){const m={avaria:'🧊 Avaria',recusa:'🚫 Recusa',atraso:'⏰ Atraso',faturamento:'💰 Faturamento',localizacao:'📍 Localização',veiculo:'🚛 Veículo',outros:'📋 Outros'};return m[tipo]||tipo||'—';}
async function loadOcorrencias() {
  document.getElementById('oc-tbody').innerHTML='<tr><td colspan="9" class="loading-state">Carregando...</td></tr>';
  const tipo=document.getElementById('oc-tipo')?.value||'';
  const gravidade=document.getElementById('oc-gravidade')?.value||'';
  const status=document.getElementById('oc-status')?.value||'';
  try {
    let ocs=await api('GET','/ocorrencias');
    if(tipo) ocs=ocs.filter(o=>o.tipo===tipo);
    if(gravidade) ocs=ocs.filter(o=>o.gravidade===gravidade);
    if(status) ocs=ocs.filter(o=>o.status===status);
    _ocorrencias=ocs;
    const el=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
    el('oc-kpi-pendentes',ocs.filter(o=>o.status==='pendente').length);
    el('oc-kpi-tratamento',ocs.filter(o=>o.status==='em_tratamento').length);
    el('oc-kpi-criticas',ocs.filter(o=>o.gravidade==='critica'&&o.status!=='resolvida').length);
    el('oc-kpi-resolvidas',ocs.filter(o=>o.status==='resolvida').length);
    const agora=Date.now();
    document.getElementById('oc-tbody').innerHTML=ocs.length
      ?ocs.map(o=>{
          const alerta15=o.gravidade==='critica'&&o.status!=='resolvida'&&(agora-new Date(o.created_at))>15*60000;
          const corLinha=o.gravidade==='critica'?'rgba(248,113,113,.08)':o.gravidade==='alta'?'rgba(249,115,22,.05)':'';
          return`<tr style="background:${corLinha}">
            <td style="text-align:center">${gravBadge(o.gravidade)}</td>
            <td style="font-size:11px;color:#90afd4">${o.created_at?new Date(o.created_at).toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}):'—'}</td>
            <td style="font-size:11px">${tipoOcLabel(o.tipo)}</td>
            <td><div style="font-size:12px;font-weight:600">${o.cliente||'—'}</div><div style="font-size:10px;color:#90afd4">${o.pedido||''}</div></td>
            <td style="font-size:11px;color:#90afd4">${o.veiculo||'—'}</td>
            <td style="font-size:11px;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${o.descricao||'—'}</td>
            <td style="font-size:11px;color:${alerta15?'#f87171':'#90afd4'}">${tempoDecorrido(o.created_at)}${alerta15?' ⚠️':''}</td>
            <td><span class="badge ${o.status||'pendente'}" style="font-size:10px">${o.status||'pendente'}</span></td>
            <td style="display:flex;gap:4px">
              ${o.foto?`<button class="btn btn-sm btn-secondary" onclick="verFotoOc('${o.id}')">📷</button>`:''}
              <button class="btn btn-sm btn-secondary" onclick="resolverOcorrencia('${o.id}')">✅</button>
              <button class="btn btn-sm btn-secondary" onclick="abrirModalOcorrencia(_ocorrencias.find(x=>x.id==='${o.id}'))">✏️</button>
            </td>
          </tr>`;
        }).join('')
      :'<tr><td colspan="9" class="loading-state">Nenhuma ocorrência encontrada</td></tr>';
  } catch(e){document.getElementById('oc-tbody').innerHTML=`<tr><td colspan="9" class="loading-state">${e.message}</td></tr>`;}
}
async function salvarOcorrencia() {
  const editId=document.getElementById('modal-ocorrencia').dataset.editId;
  const tipo=document.getElementById('oc-tipo-novo').value;
  const desc=document.getElementById('oc-descricao').value;
  if(!tipo||!desc){toast('Tipo e descrição são obrigatórios!','error');return;}
  const canvas=document.getElementById('oc-assinatura');
  const body={
    tipo, gravidade:document.getElementById('oc-gravidade-sel').value,
    pedido:document.getElementById('oc-pedido').value||null,
    cliente:document.getElementById('oc-cliente').value||null,
    veiculo:document.getElementById('oc-veiculo-novo').options[document.getElementById('oc-veiculo-novo').selectedIndex]?.text||null,
    descricao:desc, foto:document.getElementById('oc-foto-base64').value||null,
    assinatura:canvas?canvas.toDataURL():null, status:'pendente',
    gerar_devolucao:document.getElementById('oc-gerar-devolucao').checked,
    atualizar_estoque:document.getElementById('oc-atualizar-estoque').checked,
  };
  try {
    if(editId) await api('PATCH',`/ocorrencias/${editId}`,body);
    else await api('POST','/ocorrencias',body);
    toast(editId?'Atualizado!':'Registrado!','success');
    document.getElementById('modal-ocorrencia').style.display='none';
    loadOcorrencias();
  } catch(e){toast(e.message,'error');}
}
async function resolverOcorrencia(id){try{await api('PATCH',`/ocorrencias/${id}`,{status:'resolvida'});toast('Resolvida!','success');loadOcorrencias();}catch(e){toast(e.message,'error');}}
function verFotoOc(id){const oc=_ocorrencias.find(o=>o.id===id);if(!oc?.foto)return;const w=window.open('','_blank');w.document.write(`<img src="${oc.foto}" style="max-width:100%">`);}
'''

# Injeta nos marcadores corretos
if 'function loadVehicles' not in content:
    content = content.replace('// ── VEHICLES ──', '// ── VEHICLES ──\n' + veiculos_js)
    print('Veículos injetados!')

if 'function selecionarTipoDriver' not in content:
    content = content.replace('// ── DRIVERS ──', '// ── DRIVERS ──\n' + motoristas_js)
    print('Motoristas injetados!')

if 'function switchProducaoTab' not in content:
    # Adiciona antes de MONITORING
    content = content.replace('// ── MONITORING ──', producao_js + '\n// ── MONITORING ──')
    print('Produção injetada!')

if 'function selecionarGravidade' not in content:
    content = content.replace('// ── OCORRÊNCIAS ──', '// ── OCORRÊNCIAS ──\n' + ocorrencias_js)
    print('Ocorrências injetadas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
