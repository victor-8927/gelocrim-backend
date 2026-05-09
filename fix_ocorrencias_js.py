path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_js = '''
// ── OCORRÊNCIAS ───────────────────────────────────────────────────
let _ocorrencias = [];
let _ocGravSel   = 'info';
let _assinaturaCtx = null;
let _assinaturaDrawing = false;

function selecionarGravidade(grav) {
  _ocGravSel = grav;
  const cores = {info:'#10b981', media:'#f59e0b', alta:'#f97316', critica:'#f87171'};
  ['info','media','alta','critica'].forEach(g => {
    const el = document.getElementById('grav-'+g);
    if (!el) return;
    if (g === grav) {
      el.style.border = `2px solid ${cores[g]}`;
      el.style.background = `rgba(${g==='info'?'16,185,129':g==='media'?'245,158,11':g==='alta'?'249,115,22':'248,113,113'},.15)`;
      el.querySelector('div:nth-child(2)').style.color = cores[g];
    } else {
      el.style.border = '2px solid #1e3a5c';
      el.style.background = 'transparent';
      el.querySelector('div:nth-child(2)').style.color = '#90afd4';
    }
  });
  document.getElementById('oc-gravidade-sel').value = grav;
}

function initAssinatura() {
  const canvas = document.getElementById('oc-assinatura');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  _assinaturaCtx = ctx;
  ctx.strokeStyle = '#64B4FF';
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';

  const getPos = (e) => {
    const r = canvas.getBoundingClientRect();
    const src = e.touches ? e.touches[0] : e;
    return {x: src.clientX - r.left, y: src.clientY - r.top};
  };
  canvas.onmousedown = canvas.ontouchstart = (e) => {
    e.preventDefault();
    _assinaturaDrawing = true;
    const p = getPos(e);
    ctx.beginPath(); ctx.moveTo(p.x, p.y);
  };
  canvas.onmousemove = canvas.ontouchmove = (e) => {
    if (!_assinaturaDrawing) return;
    e.preventDefault();
    const p = getPos(e);
    ctx.lineTo(p.x, p.y); ctx.stroke();
  };
  canvas.onmouseup = canvas.ontouchend = () => { _assinaturaDrawing = false; };
}

function limparAssinatura() {
  const canvas = document.getElementById('oc-assinatura');
  if (canvas && _assinaturaCtx) _assinaturaCtx.clearRect(0, 0, canvas.width, canvas.height);
}

async function abrirModalOcorrencia(oc) {
  selecionarGravidade('info');
  document.getElementById('modal-oc-titulo').textContent = oc ? 'Editar Ocorrência' : 'Nova Ocorrência';
  ['oc-pedido','oc-cliente','oc-descricao'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = oc ? (oc[id.replace('oc-','')] || '') : '';
  });
  document.getElementById('oc-tipo-novo').value = oc?.tipo || '';

  // Carrega veículos
  const selV = document.getElementById('oc-veiculo-novo');
  if (selV) {
    selV.innerHTML = '<option value="">— Selecione —</option>';
    try {
      const veics = await api('GET', '/vehicles');
      veics.filter(v=>v.status==='active').forEach(v => {
        selV.innerHTML += `<option value="${v.id}">${v.vda||v.plate} — ${v.plate}</option>`;
      });
    } catch(e) {}
  }

  limparAssinatura();
  document.getElementById('oc-foto-preview').style.display = 'none';
  document.getElementById('oc-foto-placeholder').style.display = 'block';
  document.getElementById('oc-foto-base64').value = '';
  document.getElementById('modal-ocorrencia').dataset.editId = oc?.id || '';
  document.getElementById('modal-ocorrencia').style.display = 'flex';
  setTimeout(initAssinatura, 100);
}

function filtrarOcorrencia(status) {
  const sel = document.getElementById('oc-status');
  if (sel) { sel.value = status; loadOcorrencias(); }
}

function tempoDecorrido(createdAt) {
  if (!createdAt) return '—';
  const diff = (Date.now() - new Date(createdAt)) / 60000;
  if (diff < 60) return Math.floor(diff) + 'min';
  return (diff/60).toFixed(1) + 'h';
}

function gravBadge(g) {
  const m = {info:'🟢',media:'🟡',alta:'🟠',critica:'🔴'};
  const c = {info:'#10b981',media:'#f59e0b',alta:'#f97316',critica:'#f87171'};
  return `<span style="font-size:16px" title="${g}">${m[g]||'⚪'}</span>`;
}

function tipoOcLabel(tipo) {
  const m = {avaria:'🧊 Avaria',recusa:'🚫 Recusa',atraso:'⏰ Atraso',faturamento:'💰 Faturamento',localizacao:'📍 Localização',veiculo:'🚛 Veículo',outros:'📋 Outros'};
  return m[tipo] || tipo || '—';
}

async function loadOcorrencias() {
  document.getElementById('oc-tbody').innerHTML = '<tr><td colspan="9" class="loading-state">Carregando...</td></tr>';
  const tipo     = document.getElementById('oc-tipo')?.value || '';
  const gravidade= document.getElementById('oc-gravidade')?.value || '';
  const status   = document.getElementById('oc-status')?.value || '';

  try {
    let ocs = await api('GET', '/ocorrencias');
    if (tipo)      ocs = ocs.filter(o => o.tipo === tipo);
    if (gravidade) ocs = ocs.filter(o => o.gravidade === gravidade);
    if (status)    ocs = ocs.filter(o => o.status === status);
    _ocorrencias = ocs;

    // KPIs
    const el = (id,v) => { const e=document.getElementById(id); if(e) e.textContent=v; };
    el('oc-kpi-pendentes',  ocs.filter(o=>o.status==='pendente').length);
    el('oc-kpi-tratamento', ocs.filter(o=>o.status==='em_tratamento').length);
    el('oc-kpi-criticas',   ocs.filter(o=>o.gravidade==='critica'&&o.status!=='resolvida').length);
    el('oc-kpi-resolvidas', ocs.filter(o=>o.status==='resolvida').length);

    const agora = Date.now();
    document.getElementById('oc-tbody').innerHTML = ocs.length
      ? ocs.map(o => {
          const tempo = tempoDecorrido(o.created_at);
          const alerta15 = o.gravidade==='critica' && o.status!=='resolvida' &&
            (agora - new Date(o.created_at)) > 15*60000;
          const corLinha = o.gravidade==='critica'?'rgba(248,113,113,.08)':o.gravidade==='alta'?'rgba(249,115,22,.05)':'';
          return `<tr style="background:${corLinha}">
            <td style="text-align:center">${gravBadge(o.gravidade)}</td>
            <td style="font-size:11px;color:#90afd4">${o.created_at?new Date(o.created_at).toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}):'—'}</td>
            <td style="font-size:11px">${tipoOcLabel(o.tipo)}</td>
            <td>
              <div style="font-size:12px;font-weight:600">${o.cliente||'—'}</div>
              <div style="font-size:10px;color:#90afd4">${o.pedido||''}</div>
            </td>
            <td style="font-size:11px;color:#90afd4">${o.veiculo||'—'}</td>
            <td style="font-size:11px;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${o.descricao||''}">${o.descricao||'—'}</td>
            <td style="font-size:11px;color:${alerta15?'#f87171':'#90afd4'};font-weight:${alerta15?'700':'400'}">
              ${tempo}${alerta15?' ⚠️':''}
            </td>
            <td><span class="badge ${o.status||'pendente'}" style="font-size:10px">${o.status||'pendente'}</span></td>
            <td style="display:flex;gap:4px">
              ${o.foto?`<button class="btn btn-sm btn-secondary" onclick="verFotoOc('${o.id}')" title="Ver foto">📷</button>`:''}
              <button class="btn btn-sm btn-secondary" onclick="resolverOcorrencia('${o.id}')" title="Marcar resolvida">✅</button>
              <button class="btn btn-sm btn-secondary" onclick="abrirModalOcorrencia(${JSON.stringify(o).replace(/"/g,"'")})" title="Editar">✏️</button>
            </td>
          </tr>`;
        }).join('')
      : '<tr><td colspan="9" class="loading-state">Nenhuma ocorrência encontrada</td></tr>';
  } catch(e) {
    document.getElementById('oc-tbody').innerHTML = `<tr><td colspan="9" class="loading-state">${e.message}</td></tr>`;
  }
}

async function salvarOcorrencia() {
  const editId = document.getElementById('modal-ocorrencia').dataset.editId;
  const tipo = document.getElementById('oc-tipo-novo').value;
  const desc = document.getElementById('oc-descricao').value;
  if (!tipo || !desc) { toast('Tipo e descrição são obrigatórios!', 'error'); return; }

  const canvas = document.getElementById('oc-assinatura');
  const assinatura = canvas ? canvas.toDataURL() : null;

  const body = {
    tipo,
    gravidade:   document.getElementById('oc-gravidade-sel').value,
    pedido:      document.getElementById('oc-pedido').value || null,
    cliente:     document.getElementById('oc-cliente').value || null,
    veiculo:     document.getElementById('oc-veiculo-novo').options[document.getElementById('oc-veiculo-novo').selectedIndex]?.text || null,
    descricao:   desc,
    foto:        document.getElementById('oc-foto-base64').value || null,
    assinatura:  assinatura,
    status:      'pendente',
    gerar_devolucao:   document.getElementById('oc-gerar-devolucao').checked,
    atualizar_estoque: document.getElementById('oc-atualizar-estoque').checked,
  };

  try {
    if (editId) await api('PATCH', `/ocorrencias/${editId}`, body);
    else await api('POST', '/ocorrencias', body);
    toast(editId ? 'Ocorrência atualizada!' : 'Ocorrência registrada!', 'success');
    document.getElementById('modal-ocorrencia').style.display = 'none';
    loadOcorrencias();
  } catch(e) { toast(e.message, 'error'); }
}

async function resolverOcorrencia(id) {
  try {
    await api('PATCH', `/ocorrencias/${id}`, {status:'resolvida'});
    toast('Ocorrência resolvida!', 'success');
    loadOcorrencias();
  } catch(e) { toast(e.message, 'error'); }
}

function verFotoOc(id) {
  const oc = _ocorrencias.find(o=>o.id===id);
  if (!oc?.foto) return;
  const w = window.open('', '_blank');
  w.document.write(`<img src="${oc.foto}" style="max-width:100%">`);
}

'''

if 'function selecionarGravidade' not in content:
    content = content.replace('// ── VEÍCULOS COMPLETO ──', new_js + '// ── VEÍCULOS COMPLETO ──')
    print('JS de Ocorrências adicionado!')
else:
    print('JS já existe!')

# Adiciona chamada loadOcorrencias no goTo
old_goto = "if(page==='producao') { switchProducaoTab('pallet'); }"
new_goto = "if(page==='producao') { switchProducaoTab('pallet'); }\n  if(page==='ocorrencias') loadOcorrencias();"
if "if(page==='ocorrencias')" not in content:
    content = content.replace(old_goto, new_goto)
    print('goTo ocorrências adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('JS salvo!')
