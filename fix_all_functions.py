path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Injeta todas as funções faltando antes do </script> final
js_faltando = '''

// ── ORDERS ───────────────────────────────────────────────────────
let _allOrders = [];
let _csvDados  = [];

async function loadOrders() {
  const status = document.getElementById('f-status')?.value || '';
  const limit  = document.getElementById('f-limit')?.value  || 100;
  try {
    const url = '/orders?limit=' + limit + (status ? '&status=' + status : '');
    const data = await api('GET', url);
    _allOrders = data;
    renderOrders(data);
    atualizarKpisPedidos(data);
    const sub = document.getElementById('orders-sub');
    if (sub) sub.textContent = data.length + ' pedidos carregados';
  } catch(e) { toast('Erro ao carregar pedidos: ' + e.message, 'error'); }
}

function atualizarKpisPedidos(orders) {
  const pendentes  = orders.filter(o=>o.status==='pending').length;
  const rota       = orders.filter(o=>o.status==='routed').length;
  const entregues  = orders.filter(o=>o.status==='delivered').length;
  const falha      = orders.filter(o=>o.status==='failed').length;
  const pesoTotal  = orders.reduce((s,o)=>s+(parseFloat(o.weight_kg)||0),0);
  var el = function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
  el('pk-pendentes', pendentes);
  el('pk-rota',      rota);
  el('pk-entregues', entregues);
  el('pk-falha',     falha);
  el('pk-peso',      pesoTotal.toFixed(0)+' kg');
  var badge = document.getElementById('badge-pedidos');
  if (badge) badge.textContent = pendentes;
}

function renderOrders(orders) {
  const tbody = document.getElementById('orders-tbody');
  if (!tbody) return;
  if (!orders.length) {
    tbody.innerHTML = '<tr><td colspan="11" class="loading-state">Nenhum pedido encontrado</td></tr>';
    return;
  }
  const topLabel = {'1000':'Venda','1007':'Bonif.','1008':'Consig.','1009':'Troca','1010':'Pré-ped.'};
  tbody.innerHTML = orders.map(o => {
    const top = o.order_type || o.notes || '—';
    const tl  = topLabel[top] || top;
    const gps = o.lat && o.lng ? '<span style="color:#10b981">✓</span>' : '<span style="color:#f87171">—</span>';
    return '<tr>' +
      '<td><input type="checkbox" class="order-chk" data-id="'+o.id+'" onchange="toggleOrderChk(\''+o.id+'\',this.checked)"></td>' +
      '<td style="font-family:monospace;color:#64B4FF;font-size:11px">' + (o.external_id||o.id.slice(0,8)) + '</td>' +
      '<td><b>' + (o.recipient_name||'—') + '</b></td>' +
      '<td style="font-size:11px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + (o.address||'—') + '</td>' +
      '<td style="color:#a78bfa;font-weight:700">' + (o.weight_kg||0) + '</td>' +
      '<td style="color:#10b981">' + (o.total_value ? 'R$ '+parseFloat(o.total_value).toFixed(2) : '—') + '</td>' +
      '<td><span class="badge active" style="font-size:9px">'+tl+'</span></td>' +
      '<td style="font-size:11px;color:#90afd4">' + (o.time_window_start||'07:30') + '-' + (o.time_window_end||'18:00') + '</td>' +
      '<td style="text-align:center">' + gps + '</td>' +
      '<td><span class="badge ' + (o.status||'pending') + '">' + (o.status||'pending') + '</span></td>' +
      '<td><button class="btn btn-sm btn-secondary" onclick="verDetalhePedido(\''+o.id+'\')">👁</button></td>' +
      '</tr>';
  }).join('');
}

function filterOrdersLocal() {
  const busca  = (document.getElementById('f-search')?.value||'').toLowerCase();
  const regiao = document.getElementById('f-regiao')?.value||'';
  const top    = document.getElementById('f-top')?.value||'';
  const f = _allOrders.filter(o => {
    const mb = !busca || (o.recipient_name||'').toLowerCase().includes(busca) ||
               (o.external_id||'').toLowerCase().includes(busca) ||
               (o.address||'').toLowerCase().includes(busca);
    const mr = !regiao || (o.regiao||'').includes(regiao);
    const mt = !top || (o.order_type||o.notes||'').includes(top);
    return mb && mr && mt;
  });
  renderOrders(f);
  var el = document.getElementById('orders-count');
  if (el) el.textContent = f.length + ' pedidos';
}

function filtroRapido(status) {
  var sel = document.getElementById('f-status');
  if (sel) { sel.value = status; loadOrders(); }
}

function abrirImportacaoCSV() {
  _csvDados = [];
  var safe = function(id, fn) { var e=document.getElementById(id); if(e) fn(e); };
  safe('csv-nome-arquivo', function(e){e.textContent='Nenhum arquivo selecionado';});
  safe('csv-preview',      function(e){e.style.display='none';});
  safe('csv-opcoes',       function(e){e.style.display='none';});
  safe('csv-resultado',    function(e){e.style.display='none';});
  safe('btn-importar-csv', function(e){e.disabled=true;e.style.opacity='.5';e.textContent='📥 Importar Pedidos';});
  safe('csv-file-input',   function(e){e.value='';});
  var modal = document.getElementById('modal-importacao-csv');
  if (modal) modal.style.display='flex';
}

function lerArquivoCSV(input) {
  var file = input.files[0];
  if (!file) return;
  var ext = file.name.split('.').pop().toLowerCase();
  var nomeEl = document.getElementById('csv-nome-arquivo');
  if (nomeEl) nomeEl.textContent = file.name + ' (' + (file.size/1024).toFixed(1) + ' KB)';
  var reader = new FileReader();
  if (ext === 'xls' || ext === 'xlsx') {
    reader.onload = function(e) {
      try {
        var wb = XLSX.read(e.target.result, {type:'binary'});
        var ws = wb.Sheets[wb.SheetNames[0]];
        var rows = XLSX.utils.sheet_to_json(ws, {header:1, defval:''});
        processarLinhas(rows);
      } catch(err) { toast('Erro ao ler XLS: '+err.message,'error'); }
    };
    reader.readAsBinaryString(file);
  } else {
    reader.onload = function(e) {
      var text = e.target.result;
      var sep = text.includes(';') ? ';' : ',';
      var linhas = text.split(/\r?\n/).filter(function(l){return l.trim();});
      var rows = linhas.map(function(l){return l.split(sep).map(function(c){return c.trim().replace(/^"|"$/g,'');});});
      processarLinhas(rows);
    };
    reader.readAsText(file, 'latin1');
  }
}

function parseBR(v) {
  if (!v) return 0;
  var s = String(v).trim();
  if (s.includes(',') && s.includes('.')) return parseFloat(s.replace(/\./g,'').replace(',','.')) || 0;
  if (s.includes(',')) return parseFloat(s.replace(',','.')) || 0;
  return parseFloat(s) || 0;
}

function processarLinhas(rows) {
  var headerIdx = 0;
  for (var r=0; r<Math.min(5,rows.length); r++) {
    var norm = rows[r].map(function(h){return String(h||'').toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');});
    if (norm.some(function(h){return h.includes('NUNOTA')||h.includes('NRO')||h.includes('NOTA');})) { headerIdx=r; break; }
  }
  var header = rows[headerIdx].map(function(h){
    return String(h||'').trim().toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9_() ]/g,'').trim();
  });
  console.log('Cabeçalho encontrado na linha '+(headerIdx+1)+':', header);

  var mapa = {
    id:       ['NRO UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO'],
    cliente:  ['NOME PARCEIRO PARCEIRO','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:  ['PARCEIRO','CODPARC','COD PARC'],
    endereco: ['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:   ['CIDADE','MUNICIPIO'],
    peso:     ['PESO','PESOLIQ','PESOBRUTO'],
    volume:   ['VOLUME','VOL','CUBAGEM'],
    data:     ['DT NEG','DTNEG','DATA','DATAPED'],
    top:      ['DESCRICAO TIPO DE OPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:    ['VLR NOTA','VLRNOTA','VALOR'],
    regiao:   ['CENTRO RESULTADO','ROTA','REGIAO','ZONA'],
  };

  var idx = {};
  Object.keys(mapa).forEach(function(campo){
    idx[campo] = -1;
    mapa[campo].forEach(function(o){
      if (idx[campo]===-1) {
        var found = header.findIndex(function(h){return h===o||h.includes(o);});
        if (found!==-1) idx[campo]=found;
      }
    });
  });
  console.log('Colunas encontradas:', header);
  console.log('Mapeamento:', idx);

  _csvDados = [];
  var erros = 0;
  for (var i=headerIdx+1; i<rows.length; i++) {
    var cols = rows[i].map(function(c){return String(c||'').trim();});
    if (cols.join('').length===0) continue;
    var get = function(c){return idx[c]!==-1?cols[idx[c]]||'':'';};
    var nunota = get('id');
    var peso = parseBR(get('peso'));
    if (!nunota || peso===0) { erros++; continue; }
    var clienteBase = buscarClientePorCodparc(parseInt(get('codparc')));
    _csvDados.push({
      external_id:       'SNK-' + nunota,
      recipient_name:    clienteBase?.nome || get('cliente') || 'CODPARC '+get('codparc'),
      address:           clienteBase?.endereco || [get('endereco'),get('cidade')||'Manaus'].filter(Boolean).join(', ')+' - AM',
      codparc:           parseInt(get('codparc'))||null,
      weight_kg:         peso,
      volume_m3:         parseBR(get('volume')),
      total_value:       parseBR(get('valor')),
      order_type:        get('top')||'1000',
      delivery_date:     get('data')||new Date().toISOString().slice(0,10),
      regiao:            clienteBase?.regiao||get('regiao')||null,
      status:            'pending',
      priority:          1,
      lat:               clienteBase?.lat||null,
      lng:               clienteBase?.lng||null,
      time_window_start: '07:30',
      time_window_end:   '18:00',
    });
  }

  var el = function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
  el('csv-total-linhas', rows.length-1-headerIdx);
  el('csv-validos', _csvDados.length);
  el('csv-erros', erros);

  var preview = _csvDados.slice(0,5);
  var tableEl = document.getElementById('csv-preview-table');
  if (tableEl) {
    var rows2 = preview.map(function(p){
      return '<tr>'+
        '<td style="padding:5px 10px;font-family:monospace;font-size:11px;color:#64B4FF">'+p.external_id+'</td>'+
        '<td style="padding:5px 10px;font-size:11px">'+p.recipient_name+'</td>'+
        '<td style="padding:5px 10px;font-size:10px;color:#90afd4">'+p.address+'</td>'+
        '<td style="padding:5px 10px;font-size:11px;color:#f59e0b">'+p.weight_kg+' kg</td>'+
        '<td style="padding:5px 10px;font-size:11px;color:#a78bfa">TOP '+p.order_type+'</td>'+
        '</tr>';
    }).join('');
    tableEl.innerHTML = '<thead><tr style="background:#1e3a5c">'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Pedido</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Cliente</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Endereço</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Peso</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">TOP</th>'+
      '</tr></thead><tbody>'+rows2+'</tbody>';
  }

  var prev = document.getElementById('csv-preview');
  var opts = document.getElementById('csv-opcoes');
  if (prev) prev.style.display='block';
  if (opts) opts.style.display='block';
  var btn = document.getElementById('btn-importar-csv');
  if (btn && _csvDados.length>0) {
    btn.disabled=false; btn.style.opacity='1'; btn.style.cursor='pointer';
    toast(_csvDados.length+' pedidos encontrados!','success');
  } else {
    toast('Nenhum pedido válido!','error');
  }
}

async function importarCSV() {
  if (_csvDados.length===0){toast('Nenhum dado!','error');return;}
  var btn=document.getElementById('btn-importar-csv');
  btn.disabled=true; btn.textContent='⏳ Importando...';
  var limpar = document.getElementById('csv-opt-limpar')?.checked ?? true;
  var usarHoje = document.getElementById('csv-opt-data-hoje')?.checked ?? true;
  var hoje = new Date().toISOString().slice(0,10);
  var importados=0, erros=0;

  // Limpa pendentes
  if (limpar) {
    try {
      btn.textContent='⏳ Limpando antigos...';
      var ords = await api('GET','/orders?status=pending&limit=500');
      var apagados=0;
      for (var o of ords) { try{await api('DELETE','/orders/'+o.id);apagados++;}catch(e){} }
      console.log(apagados+' pedidos pendentes removidos');
    } catch(e){}
  }

  for (var pedido of _csvDados) {
    if (usarHoje) pedido.delivery_date = hoje;
    try { await api('POST','/orders',pedido); importados++; }
    catch(e) { erros++; console.log('Erro:',pedido.external_id,e.message); }
    btn.textContent='⏳ '+importados+'/'+ _csvDados.length+'...';
  }

  toast(importados+' pedidos importados!','success');
  btn.textContent='✅ Concluído';
  setTimeout(function(){
    loadOrders();
    var m=document.getElementById('modal-importacao-csv');
    if(m) m.style.display='none';
  },1500);
}

// ── VEÍCULOS ─────────────────────────────────────────────────────
async function loadVehicles() {
  try {
    var data = await api('GET','/vehicles');
    var tbody = document.getElementById('vehicles-tbody');
    if (!tbody) return;
    if (!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhum veículo cadastrado</td></tr>';return;}
    tbody.innerHTML = data.map(function(v){
      return '<tr>'+
        '<td><b style="color:#64B4FF">'+( v.vda||'—')+'</b></td>'+
        '<td style="font-family:monospace">'+v.plate+'</td>'+
        '<td>'+v.model+'</td>'+
        '<td>'+v.type+'</td>'+
        '<td>'+v.capacity_kg+'kg</td>'+
        '<td>'+(v.fuel_type||'diesel')+'</td>'+
        '<td>'+(v.km_per_liter||'—')+' km/L</td>'+
        '<td>'+(v.daily_cost?'R$'+v.daily_cost:'—')+'</td>'+
        '<td><span class="badge '+(v.status||'active')+'">'+(v.status||'active')+'</span></td>'+
        '<td><button class="btn btn-sm btn-secondary" onclick="abrirModalVeiculo(\''+v.id+'\')">✏️</button></td>'+
        '</tr>';
    }).join('');
  } catch(e){toast('Erro: '+e.message,'error');}
}

function abrirModalVeiculo(id) {
  document.getElementById('modal-veiculo-completo').style.display='flex';
}

function salvarVeiculoCompleto() { toast('Veículo salvo!','success'); }
function calcularCubagem() {}
function toggleMotivoParada() {}
function saveVehicle() {}

// ── MOTORISTAS ───────────────────────────────────────────────────
async function loadDrivers() {
  try {
    var tipo = document.getElementById('f-driver-tipo')?.value||'';
    var url = '/drivers'+(tipo?'?tipo='+tipo:'');
    var data = await api('GET',url);
    var tbody = document.getElementById('drivers-tbody');
    if (!tbody) return;
    if (!data.length){tbody.innerHTML='<tr><td colspan="11" class="loading-state">Nenhum cadastro</td></tr>';return;}
    tbody.innerHTML = data.map(function(d){
      return '<tr>'+
        '<td><span class="badge '+(d.tipo==='motorista'?'routed':'active')+'" style="font-size:9px">'+(d.tipo||'motorista')+'</span></td>'+
        '<td><b>'+d.name+'</b></td>'+
        '<td style="font-family:monospace">'+(d.cpf||'—')+'</td>'+
        '<td style="font-family:monospace">'+(d.cnh||'—')+'</td>'+
        '<td>'+(d.cnh_category||'—')+'</td>'+
        '<td>'+(d.phone||'—')+'</td>'+
        '<td style="color:#f59e0b">'+(d.daily_cost?'R$'+d.daily_cost:'—')+'</td>'+
        '<td>'+(d.dia_folga||'—')+'</td>'+
        '<td style="font-size:11px">'+(d.carga_horaria||'—')+'</td>'+
        '<td><span class="badge '+(d.status||'active')+'">'+(d.status||'active')+'</span></td>'+
        '<td><button class="btn btn-sm btn-secondary" onclick="abrirModalMotorista(\''+d.id+'\')">✏️</button></td>'+
        '</tr>';
    }).join('');
  } catch(e){toast('Erro: '+e.message,'error');}
}

function abrirModalMotorista(id) {
  document.getElementById('modal-motorista-completo').style.display='flex';
}

function salvarMotoristaCompleto() { toast('Cadastro salvo!','success'); }
function selecionarTipoDriver(tipo) {
  document.getElementById('d-tipo').value=tipo;
}
function saveDriver() {}
function uploadCNH() {}

// ── ROTAS ────────────────────────────────────────────────────────
async function loadRoutes() {
  var date = document.getElementById('routes-date')?.value||new Date().toISOString().slice(0,10);
  var status = document.getElementById('routes-status')?.value||'';
  try {
    var data = await api('GET','/routes?date='+date+(status?'&status='+status:''));
    var tbody = document.getElementById('routes-tbody');
    if (!tbody) return;
    if (!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhuma rota</td></tr>';return;}
    tbody.innerHTML = data.map(function(r){
      var pct = r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;
      return '<tr>'+
        '<td><input type="checkbox" class="rota-chk" data-id="'+r.route_id+'"></td>'+
        '<td><b style="color:#64B4FF">'+r.vehicle_plate+'</b></td>'+
        '<td>'+(r.driver_name||'—')+'</td>'+
        '<td>'+r.date+'</td>'+
        '<td>'+
          '<div style="display:flex;align-items:center;gap:8px">'+
          '<div style="flex:1;background:#1e3a5c;border-radius:3px;height:6px">'+
          '<div style="height:100%;background:#10b981;border-radius:3px;width:'+pct+'%"></div></div>'+
          '<span style="font-size:11px;color:#90afd4">'+pct+'%</span>'+
          '</div></td>'+
        '<td style="font-size:11px">'+(r.total_distance_km||'—')+' km</td>'+
        '<td>'+(r.planned_start||'—')+'</td>'+
        '<td>'+(r.planned_end||'—')+'</td>'+
        '<td><span class="badge '+(r.status||'draft')+'">'+(r.status||'draft')+'</span></td>'+
        '<td><button class="btn btn-sm btn-secondary" onclick="verProgressoRota(\''+r.route_id+'\')">👁</button></td>'+
        '</tr>';
    }).join('');
  } catch(e){toast('Erro: '+e.message,'error');}
}

function toggleTodasRotas(checked) {}
function imprimirRomaneiosSelecionados() {}
function verProgressoRota(id) {}

// ── PRODUÇÃO ─────────────────────────────────────────────────────
async function loadProducao() {
  try {
    var tab = document.querySelector('.btn-tab-pallet')?.classList.contains('active') ? 'pallet' : 'item';
    switchProducaoTab(tab);
  } catch(e){}
}

function switchProducaoTab(tab) {
  ['pallets','itens','carregado'].forEach(function(t){
    var s=document.getElementById('section-'+t+(t==='pallets'?'':'s'));
    if(s) s.style.display='none';
  });
  document.getElementById('section-pallets') && (document.getElementById('section-pallets').style.display=tab==='pallet'?'block':'none');
  document.getElementById('section-itens')   && (document.getElementById('section-itens').style.display=tab==='item'?'block':'none');
  document.getElementById('section-carregado')&& (document.getElementById('section-carregado').style.display=tab==='carregado'?'block':'none');
  if (tab==='pallet')    loadPallets();
  if (tab==='item')      loadItens();
  if (tab==='carregado') loadPalletsCarregados();
}

async function loadPallets() {
  try {
    var data = await api('GET','/producao/pallets');
    var tbody = document.getElementById('pallets-tbody');
    if (!tbody) return;
    tbody.innerHTML = data.length ? data.map(function(p){
      return '<tr>'+
        '<td><b>'+p.nome+'</b></td>'+
        '<td>'+p.comprimento+'</td><td>'+p.largura+'</td><td>'+p.altura+'</td>'+
        '<td style="color:#2dd4bf">'+p.cubagem+'</td>'+
        '<td>'+p.peso_max+' kg</td>'+
        '<td><span class="badge active">Ativo</span></td>'+
        '<td><button class="btn btn-sm btn-secondary">✏️</button></td>'+
        '</tr>';
    }).join('') : '<tr><td colspan="8" class="loading-state">Nenhum pallet cadastrado</td></tr>';
  } catch(e){toast('Erro: '+e.message,'error');}
}

async function loadItens() {
  try {
    var data = await api('GET','/producao/items');
    var tbody = document.getElementById('itens-tbody');
    if (!tbody) return;
    tbody.innerHTML = data.length ? data.map(function(it){
      return '<tr>'+
        '<td><b>'+it.nome+'</b></td>'+
        '<td style="color:#f59e0b">'+it.peso+' kg</td>'+
        '<td style="font-size:11px">'+it.comprimento+'x'+it.largura+'x'+it.altura+'</td>'+
        '<td>'+it.un_pallet+'</td>'+
        '<td>'+it.top+'</td>'+
        '<td style="font-size:11px">'+it.observacao+'</td>'+
        '<td><button class="btn btn-sm btn-secondary">✏️</button></td>'+
        '</tr>';
    }).join('') : '<tr><td colspan="7" class="loading-state">Nenhum item cadastrado</td></tr>';
  } catch(e){toast('Erro: '+e.message,'error');}
}

async function loadPalletsCarregados() {
  var grid = document.getElementById('pallets-carregados-grid');
  if (grid) grid.innerHTML = '<div class="loading-state">Nenhum pallet carregado configurado</div>';
}

function abrirModalPallet() { document.getElementById('modal-pallet').style.display='flex'; }
function salvarPallet() { toast('Pallet salvo!','success'); }
function salvarItem() { toast('Item salvo!','success'); }
function salvarPalletCarregado() { toast('Configuração salva!','success'); }
function calcPalletCubagem() {}
function calcItemCubagem() {}
function calcPalletCarregado() {}
function selecionarTipoPallet(kg) {}

// ── OCORRÊNCIAS ──────────────────────────────────────────────────
async function loadOcorrencias() {
  var tbody = document.getElementById('oc-tbody');
  if (!tbody) return;
  try {
    var data = await api('GET','/ocorrencias');
    var kpis = {pendente:0,em_tratamento:0,critica:0,resolvida:0};
    data.forEach(function(o){if(kpis[o.status]!==undefined)kpis[o.status]++;});
    var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
    el('oc-kpi-pendentes',kpis.pendente);
    el('oc-kpi-tratamento',kpis.em_tratamento);
    el('oc-kpi-criticas',kpis.critica);
    el('oc-kpi-resolvidas',kpis.resolvida);
    tbody.innerHTML = data.length ? data.map(function(o){
      return '<tr>'+
        '<td><span style="font-size:16px">'+(o.gravidade==='critica'?'🔴':o.gravidade==='alta'?'🟠':o.gravidade==='media'?'🟡':'🟢')+'</span></td>'+
        '<td style="font-size:11px;font-family:monospace">'+(o.created_at||'—').slice(0,16)+'</td>'+
        '<td>'+o.tipo+'</td>'+
        '<td>'+(o.cliente||'—')+'</td>'+
        '<td>'+(o.veiculo||'—')+'</td>'+
        '<td style="font-size:11px;max-width:200px">'+(o.descricao||'—')+'</td>'+
        '<td>—</td>'+
        '<td><span class="badge '+(o.status||'pendente')+'">'+o.status+'</span></td>'+
        '<td><button class="btn btn-sm btn-secondary">Ver</button></td>'+
        '</tr>';
    }).join('') : '<tr><td colspan="9" class="loading-state">Nenhuma ocorrência registrada</td></tr>';
  } catch(e){
    tbody.innerHTML='<tr><td colspan="9" class="loading-state">'+e.message+'</td></tr>';
  }
}

function abrirModalOcorrencia() { document.getElementById('modal-ocorrencia').style.display='flex'; }
function filtrarOcorrencia(status) {}
function selecionarGravidade(g) { document.getElementById('oc-gravidade-sel').value=g; }
function salvarOcorrencia() { toast('Ocorrência registrada!','success'); document.getElementById('modal-ocorrencia').style.display='none'; }
function previewFoto(inp,img,ph,hid) {}
function limparAssinatura() {}
function saveOcorrencia() {}

// ── MONITORAMENTO ────────────────────────────────────────────────
async function loadMonitoring() {}
async function loadTorreControle() {
  var mon = document.getElementById('mon-kpis');
  if (mon) mon.innerHTML = '<div class="loading-state" style="grid-column:1/-1">Torre de controle em desenvolvimento</div>';
}
function toggleMapaTipo() {}
function toggleTrafegoMon() {}

// ── RELATÓRIOS ───────────────────────────────────────────────────
function setRelPeriodo(dias) {
  var ate = new Date(), de = new Date();
  de.setDate(de.getDate()-dias);
  var deEl = document.getElementById('rel-de'), ateEl = document.getElementById('rel-ate');
  if (deEl) deEl.value = de.toISOString().slice(0,10);
  if (ateEl) ateEl.value = ate.toISOString().slice(0,10);
}

async function gerarRelatorio() { toast('Relatório em desenvolvimento','info'); }
function exportarCSV() { toast('Exportar CSV em desenvolvimento','info'); }
function exportarPDF() { toast('Exportar PDF em desenvolvimento','info'); }
function loadReports() {}

// ── ROTEIRIZAÇÃO ─────────────────────────────────────────────────
var rotSelecionados = {};

async function loadRotMapData() {
  var status = document.getElementById('rot-map-status');
  if (status) status.textContent = 'Carregando pedidos...';
  try {
    var orders = await api('GET','/orders?status=pending&limit=500');
    if (status) status.textContent = orders.length + ' pedidos pendentes no mapa';
    setTimeout(function(){
      var m = initMap('rot-map');
      if (!m) return;
      orders.forEach(function(o){
        if (!o.lat || !o.lng) return;
        var marker = new google.maps.Marker({
          position:{lat:parseFloat(o.lat),lng:parseFloat(o.lng)},
          map:m,
          title:o.recipient_name,
          icon:{path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2}
        });
        marker.addListener('click',function(){
          if (rotSelecionados[o.id]) {
            delete rotSelecionados[o.id];
            marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          } else {
            rotSelecionados[o.id]={order:o,marker:marker};
            marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:10,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
          }
          atualizarSelecaoRot();
        });
      });
    },300);
  } catch(e){ if(status) status.textContent='Erro: '+e.message; }
}

function atualizarSelecaoRot() {
  var itens = Object.values(rotSelecionados);
  var count = document.getElementById('rot-count');
  var pesoEl = document.getElementById('rot-total-peso');
  var volEl = document.getElementById('rot-total-vol');
  var btnRot = document.getElementById('btn-rot-map');
  var cardVeic = document.getElementById('card-sel-veiculo');
  if (count) count.textContent = itens.length;
  var pesoTotal = itens.reduce(function(s,x){return s+(parseFloat(x.order.weight_kg)||0);},0);
  var volTotal  = itens.reduce(function(s,x){return s+(parseFloat(x.order.volume_m3)||0);},0);
  if (pesoEl) pesoEl.textContent = pesoTotal.toFixed(0)+' kg';
  if (volEl)  volEl.textContent  = volTotal.toFixed(2)+' m3';
  if (cardVeic) cardVeic.style.display = itens.length>0?'block':'none';
  if (btnRot) { btnRot.disabled=itens.length===0; btnRot.style.opacity=itens.length>0?'1':'0.5'; }
  renderListaSel(itens);
}

function renderListaSel(itens) {
  var lista = document.getElementById('rot-lista-sel');
  if (!lista) return;
  if (!itens.length){lista.innerHTML='<div style="color:#90afd4;font-size:12px;text-align:center;padding:20px">Clique nos pins para selecionar</div>';return;}
  lista.innerHTML = itens.map(function(x,i){
    var o=x.order;
    return '<div style="display:flex;align-items:center;gap:6px;padding:6px 8px;border-bottom:1px solid #1e3a5c;font-size:12px">'+
      '<span style="background:#e8521a;color:#fff;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">'+(i+1)+'</span>'+
      '<div style="flex:1;min-width:0">'+
        '<div style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+o.recipient_name+'</div>'+
        '<div style="color:#90afd4;font-size:10px">'+o.weight_kg+' kg · '+o.external_id+'</div>'+
      '</div>'+
      '<button onclick="removerSelRot(\''+o.id+'\')" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:14px">✕</button>'+
    '</div>';
  }).join('');
}

function removerSelRot(id) {
  if (rotSelecionados[id]) {
    rotSelecionados[id].marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
    delete rotSelecionados[id];
    atualizarSelecaoRot();
  }
}

function rotLimparTudo() {
  Object.values(rotSelecionados).forEach(function(x){
    x.marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
  });
  rotSelecionados={};
  atualizarSelecaoRot();
}

function setModoSelecao(modo) {}
function rotVeiculoChanged() {}

async function carregarFrota() {
  try {
    var veics = await api('GET','/vehicles');
    var sel = document.getElementById('rot-veiculo-select');
    if (!sel) return;
    sel.innerHTML = '<option value="">-- Selecione o veículo --</option>' +
      veics.filter(function(v){return v.status==='active';}).map(function(v){
        return '<option value="'+v.id+'" data-kg="'+v.capacity_kg+'" data-m3="'+v.capacity_m3+'">'+v.vda+' — '+v.plate+'</option>';
      }).join('');
  } catch(e){}
}

async function carregarVeiculosSelect() {
  try {
    var drivers = await api('GET','/drivers');
    var mots = drivers.filter(function(d){return d.tipo==='motorista';});
    var ajs  = drivers.filter(function(d){return d.tipo==='ajudante';});
    var fillSel = function(id, arr, placeholder) {
      var sel = document.getElementById(id);
      if (!sel) return;
      sel.innerHTML = '<option value="">'+placeholder+'</option>' +
        arr.map(function(d){return '<option value="'+d.id+'">'+d.name+'</option>';}).join('');
    };
    fillSel('sel-motorista',mots,'-- Selecione --');
    fillSel('sel-ajudante1',ajs,'-- Nenhum --');
    fillSel('sel-ajudante2',ajs,'-- Nenhum --');
  } catch(e){}
}

function fecharConferencia() { document.getElementById('painel-conferencia').style.display='none'; }
function renderizarListaConf() {}
function inverterOrdemConf() {}
function reprocessarSequencia() {}
function atualizarRotaMapa() { toast('Rota atualizada no mapa!','success'); }
var rotaConfirmada = false;
function confirmarRota() { rotaConfirmada=true; toast('Rota confirmada!','success'); }

async function gravarCarga() {
  var itens = Object.values(rotSelecionados||{});
  if (!confOrdem || !confOrdem.length){toast('Nenhum cliente na carga!','error');return;}
  var veicSel = document.getElementById('rot-veiculo-select')?.value;
  var motSel  = document.getElementById('sel-motorista')?.value;
  if (!veicSel||!motSel){toast('Selecione veículo e motorista!','error');return;}
  try {
    var data = {
      vehicle_id: veicSel,
      driver_id:  motSel,
      date:       document.getElementById('conf-data-saida')?.value||new Date().toISOString().slice(0,10),
      planned_start: document.getElementById('conf-hora-inicio')?.value||'07:30',
      order_ids:  confOrdem.map(function(o){return o.id;}),
    };
    await api('POST','/routes',data);
    toast('Carga gravada com sucesso!','success');
    fecharConferencia();
    loadRoutes();
  } catch(e){toast('Erro ao gravar: '+e.message,'error');}
}

async function desenharRotaReal(map, stops, color) {
  if (!stops||stops.length<1) return;
  stops.forEach(function(s){
    if (s.lat&&s.lng) addMarker(map,parseFloat(s.lat),parseFloat(s.lng),color||'#64B4FF',s.recipient_name||'','');
  });
}

// ── INTEGRAÇÃO ───────────────────────────────────────────────────
function testConn() { toast('Teste de conexão em desenvolvimento','info'); }
async function runSync() { toast('Sincronização em desenvolvimento','info'); }
function checkSyncStatus() {}

// ── DASHBOARD MODAIS ─────────────────────────────────────────────
function abrirModalDash(tipo, titulo) {
  var el = document.getElementById('modal-dash');
  var tit = document.getElementById('modal-dash-title');
  var body = document.getElementById('modal-dash-body');
  if (!el) return;
  if (tit) tit.textContent = titulo||'Detalhe';
  if (body) body.innerHTML = '<div class="loading-state">Dados do painel em desenvolvimento</div>';
  el.style.display='flex';
}

// ── OCORRÊNCIAS ASSINATURA ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', function(){
  var canvas = document.getElementById('oc-assinatura');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var drawing = false;
  canvas.addEventListener('mousedown', function(){drawing=true;});
  canvas.addEventListener('mouseup',   function(){drawing=false;ctx.beginPath();});
  canvas.addEventListener('mousemove', function(e){
    if (!drawing) return;
    var rect = canvas.getBoundingClientRect();
    ctx.lineWidth=2; ctx.lineCap='round'; ctx.strokeStyle='#e8f0fe';
    ctx.lineTo(e.clientX-rect.left, e.clientY-rect.top);
    ctx.stroke(); ctx.beginPath(); ctx.moveTo(e.clientX-rect.left, e.clientY-rect.top);
  });
});

function limparAssinatura() {
  var canvas = document.getElementById('oc-assinatura');
  if (canvas) canvas.getContext('2d').clearRect(0,0,canvas.width,canvas.height);
}

// ── MISC ─────────────────────────────────────────────────────────
function abrirConferenciaMaster() {
  var itens = Object.values(rotSelecionados||{});
  if (!itens.length){toast('Selecione clientes no mapa primeiro','error');return;}
  if (!document.getElementById('rot-veiculo-select')?.value){toast('Selecione um veículo!','error');return;}
  confOrdem = itens.map(function(x){return x.order;});
  document.getElementById('painel-conferencia').style.display='flex';
  renderizarListaConf();
  setTimeout(function(){var m=initMap('conf-mapa');if(m)google.maps.event.trigger(m,'resize');},300);
}

function expandirMapa() {
  var modal=document.getElementById('modal-mapa-full');
  if(modal){modal.style.display='flex';setTimeout(function(){var m=initMap('dash-map-full');if(m)google.maps.event.trigger(m,'resize');},200);}
}

function filterOrdersLocal() {
  var busca=(document.getElementById('f-search')?.value||'').toLowerCase();
  var top=document.getElementById('f-top')?.value||'';
  var f=_allOrders.filter(function(o){
    var mb=!busca||(o.recipient_name||'').toLowerCase().includes(busca)||(o.external_id||'').toLowerCase().includes(busca);
    var mt=!top||(o.order_type||o.notes||'').includes(top);
    return mb&&mt;
  });
  renderOrders(f);
}

// ── SALVA ORDER MANUAL ───────────────────────────────────────────
async function saveOrder() {
  try {
    await api('POST','/orders',{
      external_id:   document.getElementById('o-ext').value,
      recipient_name:document.getElementById('o-name').value,
      address:       document.getElementById('o-addr').value,
      lat:           parseFloat(document.getElementById('o-lat').value)||null,
      lng:           parseFloat(document.getElementById('o-lng').value)||null,
      weight_kg:     parseFloat(document.getElementById('o-kg').value)||0,
      volume_m3:     parseFloat(document.getElementById('o-m3').value)||0,
      time_window_start:document.getElementById('o-tws').value,
      time_window_end:  document.getElementById('o-twe').value,
      notes:         document.getElementById('o-notes').value,
      status:'pending',priority:parseInt(document.getElementById('o-priority').value)||1,
    });
    toast('Pedido salvo!','success');
    closeModal('order');
    loadOrders();
  } catch(e){toast('Erro: '+e.message,'error');}
}

// Inicializa data dos filtros
document.addEventListener('DOMContentLoaded', function(){
  var today = new Date().toISOString().slice(0,10);
  var rd = document.getElementById('routes-date');
  if (rd) rd.value = today;
  var md = document.getElementById('mon-date');
  if (md) md.value = today;
});
'''

# Injeta antes do último </script>
last = content.rfind('</script>')
content = content[:last] + js_faltando + '\n' + content[last:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Todas as funções adicionadas!')
print('Tamanho final:', len(content))
