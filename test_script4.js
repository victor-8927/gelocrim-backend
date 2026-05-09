
var XLSX={read:function(){return{SheetNames:['s'],Sheets:{s:{}}};},utils:{sheet_to_json:function(){return[];}}};
var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};this.setMap=function(){};},
  SymbolPath:{CIRCLE:0},Map:function(){this.fitBounds=function(){};},
  LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},
  LatLng:function(){},DirectionsService:function(){this.route=function(){};},
  DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},
  TrafficLayer:function(){this.setMap=function(){};},
  TravelMode:{DRIVING:'DRIVING'},Polyline:function(){this.setMap=function(){};},
  InfoWindow:function(){this.open=function(){};},
  event:{trigger:function(){}}}};
function api(){}function toast(){}function initMap(){return null;}function addMarker(){}
function closeModal(){}function openModal(){}function goTo(){}function loadRoutes(){}
var token='';var maps={};var confOrdem=[];var confMap=null;var rotaConfirmada=false;
var rotSelecionados={};var _tgfiteTipo=null;var _tgfiteNome=null;var _tgfitePeso=null;
var _tgfiteDados=[];

var _clientesCache = {};
var _todosClientes = [];
var _allOrders = [];
var _csvDados  = [];

// ── CLIENTES/PARCEIROS ───────────────────────────────────────────
function buscarClientePorCodparc(codparc) {
  return _clientesCache[parseInt(codparc)] || null;
}

async function carregarBaseClientes() {
  try {
    var lista = await api('GET', '/clientes');
    _clientesCache = {};
    lista.forEach(function(c){ _clientesCache[c.codparc] = c; });
    return lista.length;
  } catch(e) { return 0; }
}

async function loadClientes() {
  try {
    var lista = await api('GET', '/clientes');
    _todosClientes = lista;
    var comGps = lista.filter(function(c){return c.lat&&c.lng;}).length;
    var ativos  = lista.filter(function(c){return c.ativo==='S';}).length;
    var regsSet = {};
    lista.forEach(function(c){if(c.regiao) regsSet[c.regiao]=1;});
    var regioes = Object.keys(regsSet).length;
    var el = function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
    el('cli-total',lista.length); el('cli-gps',comGps); el('cli-ativos',ativos); el('cli-regioes',regioes);
    el('clientes-sub',lista.length+' parceiros cadastrados');
    var sel = document.getElementById('cli-regiao');
    if(sel){
      var regs = Object.keys(regsSet).sort();
      var opts = '<option value="">Todas as regioes</option>';
      regs.forEach(function(r){opts+='<option value="'+r+'">'+r+'</option>';});
      sel.innerHTML = opts;
    }
    renderClientes(lista);
  } catch(e){ toast('Erro: '+e.message,'error'); }
}

function filtrarClientes() {
  var busca  = (document.getElementById('cli-busca')||{value:''}).value.toLowerCase();
  var regiao = (document.getElementById('cli-regiao')||{value:''}).value;
  var gps    = (document.getElementById('cli-gps-filtro')||{value:''}).value;
  var f = _todosClientes.filter(function(c){
    var mb = !busca||(c.nome||'').toLowerCase().indexOf(busca)>=0||(c.endereco||'').toLowerCase().indexOf(busca)>=0||String(c.codparc||'').indexOf(busca)>=0;
    var mr = !regiao||c.regiao===regiao;
    var mg = !gps||(gps==='sim'?(c.lat&&c.lng):!(c.lat&&c.lng));
    return mb&&mr&&mg;
  });
  renderClientes(f);
}

function limparFiltrosClientes(){
  ['cli-busca','cli-regiao','cli-gps-filtro'].forEach(function(id){var e=document.getElementById(id);if(e)e.value='';});
  renderClientes(_todosClientes);
}

function renderClientes(lista) {
  var tbody  = document.getElementById('clientes-tbody');
  var rodape = document.getElementById('clientes-rodape');
  if(!tbody) return;
  if(!lista.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhum parceiro</td></tr>';return;}
  var rows = '';
  lista.forEach(function(c){
    var gps = (c.lat&&c.lng)
      ? '<span style="color:#10b981;font-size:10px">✓ '+parseFloat(c.lat).toFixed(4)+', '+parseFloat(c.lng).toFixed(4)+'</span>'
      : '<span style="color:#f87171">Sem GPS</span>';
    var at  = c.ativo==='S'?'active':'inactive';
    var cidade = (c.cidade||'').replace(' - AM','');
    var codStr = String(c.codparc||'');
    rows += '<tr>'+
      '<td style="font-family:monospace;color:#64B4FF">'+codStr+'</td>'+
      '<td><b>'+(c.nome||'—')+'</b></td>'+
      '<td style="font-size:11px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+(c.endereco||'—')+'</td>'+
      '<td style="font-size:11px">'+(c.bairro||'—')+'</td>'+
      '<td style="font-size:11px">'+cidade+'</td>'+
      '<td><span class="badge active" style="font-size:9px">'+(c.regiao||'—')+'</span></td>'+
      '<td style="font-size:10px">'+gps+'</td>'+
      '<td style="font-size:11px">'+(c.telefone||'—')+'</td>'+
      '<td><span class="badge '+at+'">'+(c.ativo==='S'?'Ativo':'Inativo')+'</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-idx="'+codStr+'" onclick="detalharParceiro('+codStr+')">🔍 Ver</button></td>'+
      '</tr>';
  });
  tbody.innerHTML = rows;
  if(rodape) rodape.textContent = lista.length+' parceiros';
}

function detalharParceiro(codparc) {
  var c = _todosClientes.find(function(x){return x.codparc == codparc;});
  if(!c) return;

  var gpsInfo = (c.lat && c.lng)
    ? '<div style="display:flex;align-items:center;gap:12px">'+
      '<span style="color:#10b981;font-size:13px">✓ GPS: '+parseFloat(c.lat).toFixed(6)+', '+parseFloat(c.lng).toFixed(6)+'</span>'+
      '<a href="https://www.google.com/maps?q='+c.lat+','+c.lng+'" target="_blank" class="btn btn-sm btn-secondary">📍 Ver Mapa</a>'+
      '</div>'
    : '<span style="color:#f87171">⚠️ Sem coordenadas GPS — necessário para roteirização</span>';

  var tempoEntrega = c.tempo_entrega || c.tempo_medio || '—';
  var janela = tempoEntrega !== '—' ? tempoEntrega + ' min' : '—';

  var html =
    // GPS em destaque
    '<div style="background:#0a1628;border:1px solid '+(c.lat&&c.lng?'#10b981':'#f87171')+';border-radius:8px;padding:12px;margin-bottom:16px">'+
    '<div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px">📍 GEOLOCALIZAÇÃO</div>'+
    gpsInfo+
    '</div>'+

    // Grid de informações
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px">'+
    campo('Código ERP', c.codparc)+
    campo('Nome Fantasia', c.nome)+
    campo('Razão Social', c.razao_social)+
    campo('CPF/CNPJ', c.cpf_cnpj)+
    campo('Telefone', c.telefone)+
    campo('Segmento', c.segmento)+
    '</div>'+

    '<div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:8px">📦 LOGÍSTICA E ROTEIRIZAÇÃO</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:16px">'+
    campoDestaque('Rota', c.rota || c.regiao, '#f59e0b')+
    campoDestaque('Zona Geo', c.zona_geo, '#a78bfa')+
    campoDestaque('⏱️ Tempo Médio', janela, '#64B4FF')+
    '</div>'+

    '<div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:8px">🏠 ENDEREÇO</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px">'+
    '<div style="grid-column:1/-1">'+campo('Endereço Completo', c.endereco)+'</div>'+
    campo('Bairro', c.bairro)+
    campo('Cidade', c.cidade ? c.cidade.replace(' - AM','').replace('/AM','') : '—')+
    campo('CEP', c.cep)+
    campo('Estado', 'AM')+
    '</div>'+

    '<div style="font-size:10px;font-weight:700;color:#64B4FF;letter-spacing:1.5px;margin-bottom:8px">📋 OUTROS</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'+
    campo('Comodatos', c.comodatos)+
    campo('Status', c.ativo==="S"?"✅ Ativo":"❌ Inativo")+
    '</div>';

  var existing = document.getElementById('modal-parceiro-detalhe');
  if(!existing){
    var div = document.createElement('div');
    div.id = 'modal-parceiro-detalhe';
    div.onclick = function(e){if(e.target===div)div.style.display='none';};
    div.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;align-items:center;justify-content:center;padding:20px';
    div.innerHTML =
      '<div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:700px;max-height:88vh;overflow-y:auto">'+
      '<div style="padding:16px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0;z-index:1">'+
      '<span style="font-size:15px;font-weight:700;color:#e8f0fe" id="modal-parc-titulo">Parceiro</span>'+
      '<button onclick="document.getElementById(&quot;modal-parceiro-detalhe&quot;).style.display=&quot;none&quot;" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">&#x2715;</button>'+
      '</div><div id="modal-parc-body" style="padding:20px 24px"></div></div>';
    document.body.appendChild(div);
    existing = div;
  }

  document.getElementById('modal-parc-titulo').textContent = '🤝 ' + (c.nome || 'Parceiro') + ' — Cód. ' + c.codparc;
  document.getElementById('modal-parc-body').innerHTML = html;
  existing.style.display = 'flex';
}

function campo(label, valor) {
  return '<div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px">'+
    '<div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px;margin-bottom:3px">'+label+'</div>'+
    '<div style="font-size:13px;color:#e8f0fe;font-weight:500">'+(valor||'—')+'</div>'+
    '</div>';
}

function campoDestaque(label, valor, cor) {
  return '<div style="background:#0a1628;border:1px solid '+(cor||'#1e3a5c')+';border-radius:8px;padding:10px;border-left:3px solid '+(cor||'#64B4FF')+'">'+
    '<div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px;margin-bottom:3px">'+label+'</div>'+
    '<div style="font-size:15px;color:'+(cor||'#e8f0fe')+';font-weight:700">'+(valor||'—')+'</div>'+
    '</div>';
}


function abrirImportacaoBaseClientes() {
  var modal = document.getElementById('modal-base-clientes');
  if(!modal){toast('Modal não encontrado','error');return;}
  var n = document.getElementById('base-clientes-nome');
  var c = document.getElementById('base-clientes-count');
  var b = document.getElementById('btn-importar-base');
  var inp = document.getElementById('base-clientes-input');
  if(n) n.textContent = 'Nenhum arquivo';
  if(c) c.textContent = '';
  if(b){b.disabled=true;b.style.opacity='.5';b.textContent='Importar';}
  if(inp) inp.value = '';
  window._clientesParaImportar = [];
  modal.style.display = 'flex';
}

function lerBaseClientesXLS(input) {
  var file = input.files[0];
  if(!file) return;
  var nomeEl = document.getElementById('base-clientes-nome');
  if(nomeEl) nomeEl.textContent = file.name;
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var wb   = XLSX.read(e.target.result, {type:'binary'});
      var ws   = wb.Sheets[wb.SheetNames[0]];
      var rows = XLSX.utils.sheet_to_json(ws, {header:1, defval:''});
      var headerIdx = 0;
      for(var r=0;r<Math.min(5,rows.length);r++){
        var norm = rows[r].map(function(h){return String(h||'').toUpperCase();});
        if(norm.some(function(h){return h.indexOf('CODIGO')>=0||h.indexOf('COD')>=0;})){headerIdx=r;break;}
      }
      var header = rows[headerIdx].map(function(h){
        return String(h||'').trim().toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9_\/]/g,'').trim();
      });
      var m = {
        codparc:      ['CODIGO_ERP','CODPARC','CODIGO','COD'],
        nome:         ['NOME_FANTASIA','NOMEFANTASIA','NOME FANTASIA','NOME'],
        razao_social: ['RAZAO_SOCIAL','RAZAOSOCIAL','RAZAO SOCIAL'],
        endereco:     ['ENDERECO'],
        cep:          ['CEP'],
        bairro:       ['BAIRRO'],
        cidade:       ['CIDADE/UF','CIDADEUF','CIDADE UF','CIDADE'],
        lat:          ['LATITUDE','LAT'],
        lng:          ['LONGITUDE','LNG'],
        cpf_cnpj:     ['CPF/CNPJ','CPFCNPJ','CPF CNPJ'],
        segmento:     ['SEGMENTO'],
        zona_geo:     ['ZONA_GEO','ZONAGEO','ZONA GEO'],
        comodatos:    ['COMODATOS'],
        tempo_entrega:['TEMPO MEDIO ENTREGA','TEMPO MDIO ENTREGA','TEMPOMEDIO','TEMPO MEDIO','TEMPO ENTREGA','TEMPO MEDIOENTREGA','TEMPOMEDIOENTREGA','TEMPO'],
        rota:         ['ROTA'],
      };
      var idx = {};
      Object.keys(m).forEach(function(campo){
        idx[campo]=-1;
        m[campo].forEach(function(o){if(idx[campo]===-1&&header.indexOf(o)!==-1)idx[campo]=header.indexOf(o);});
      });
      var parceiros=[],semGps=0;
      for(var i=headerIdx+1;i<rows.length;i++){
        var cols = rows[i].map(function(c){return String(c||'').trim();});
        if(cols.join('').length===0) continue;
        var get = function(c){return idx[c]!==-1?cols[idx[c]]||'':'';};
        var codparc = parseInt(get('codparc'));
        if(!codparc||isNaN(codparc)) continue;
        var parseCoord = function(v){if(!v)return null;return parseFloat(String(v).replace(',','.').replace(/[^\d.\-]/g,''))||null;};
        var lat=parseCoord(get('lat')),lng=parseCoord(get('lng'));
        if(!lat||!lng) semGps++;
        var end=get('endereco'),bairro=get('bairro');
        var cidade=get('cidade').replace('/AM','').replace('- AM','').trim()||'Manaus';
        var endFull=[end,bairro,cidade+' - AM'].filter(Boolean).join(', ');
        parceiros.push({codparc:codparc,nome:get('nome')||get('razao_social'),razao_social:get('razao_social'),
          endereco:endFull,cep:get('cep'),bairro:bairro,cidade:get('cidade'),lat:lat,lng:lng,
          cpf_cnpj:get('cpf_cnpj'),segmento:get('segmento'),zona_geo:get('zona_geo'),
          regiao:get('zona_geo')||get('rota'),comodatos:get('comodatos'),
          tempo_entrega:get('tempo_entrega'),rota:get('rota'),telefone:'',ativo:'S'});
      }
      var countEl=document.getElementById('base-clientes-count');
      if(countEl) countEl.textContent=parceiros.length+' parceiros ('+semGps+' sem GPS)';
      var btn=document.getElementById('btn-importar-base');
      if(btn&&parceiros.length>0){btn.disabled=false;btn.style.opacity='1';btn.style.cursor='pointer';}
      // Converte tempo Excel para minutos
      parceiros.forEach(function(p){
        if(p.tempo_entrega && p.tempo_entrega !== '') {
          var val = p.tempo_entrega;
          var minutos = 0;
          if(String(val).indexOf(':')>=0){
            // Formato HH:MM:SS
            var parts = String(val).split(':');
            minutos = (parseInt(parts[0])||0)*60 + (parseInt(parts[1])||0);
          } else {
            var num = parseFloat(val);
            if(!isNaN(num)){
              if(num < 1) {
                // Fração de dia do Excel: 0.0625 = 90min
                minutos = Math.round(num * 24 * 60);
              } else {
                // Já em minutos
                minutos = Math.round(num);
              }
            }
          }
          p.tempo_entrega = minutos > 0 ? String(minutos) : '';
        }
        // Extrai só a cidade antes de /UF
        if(p.cidade && p.cidade.indexOf('/')>=0){
          p.cidade = p.cidade.split('/')[0].trim();
        }
        if(p.cidade && p.cidade.indexOf('-')>=0 && p.cidade.length < 6){
          p.cidade = 'Manaus';
        }
        if(!p.cidade || p.cidade.trim()==='') p.cidade = 'Manaus';
      });
      window._clientesParaImportar=parceiros;
      toast(parceiros.length+' parceiros prontos! ('+parceiros.filter(function(p){return p.tempo_entrega&&p.tempo_entrega!=='0';}).length+' com tempo médio)','success');
    } catch(err){toast('Erro: '+err.message,'error');}
  };
  reader.readAsBinaryString(file);
}

async function importarBaseClientes() {
  var parceiros=window._clientesParaImportar||[];
  if(!parceiros.length){toast('Nenhum dado!','error');return;}
  var btn=document.getElementById('btn-importar-base');
  if(btn){btn.disabled=true;btn.textContent='Importando...';}
  try {
    var total=0;
    for(var i=0;i<parceiros.length;i+=500){
      var res=await api('POST','/clientes/bulk',parceiros.slice(i,i+500));
      total+=(res.inserted||0)+(res.updated||0);
      if(btn) btn.textContent=''+total+'/'+parceiros.length+'...';
    }
    await carregarBaseClientes();
    toast(''+total+' parceiros importados!','success');
    if(btn) btn.textContent='Importado';
    setTimeout(function(){
      var m=document.getElementById('modal-base-clientes');
      if(m) m.style.display='none';
      if(typeof loadClientes==='function') loadClientes();
    },1500);
  } catch(e){toast('Erro: '+e.message,'error');if(btn){btn.textContent='Importar';btn.disabled=false;}}
}

// ── ORDERS ───────────────────────────────────────────────────────
async function loadOrders() {
  var status = document.getElementById('f-status') ? document.getElementById('f-status').value : '';
  var limit  = document.getElementById('f-limit')  ? document.getElementById('f-limit').value  : 100;
  try {
    var url  = '/orders?limit='+limit+(status?'&status='+status:'');
    var data = await api('GET', url);
    _allOrders = data;
    renderOrders(data);
    atualizarKpisPedidos(data);
    var sub = document.getElementById('orders-sub');
    if(sub) sub.textContent = data.length+' pedidos carregados';
  } catch(e){toast('Erro ao carregar pedidos: '+e.message,'error');}
}

function atualizarKpisPedidos(orders) {
  var pendentes = orders.filter(function(o){return o.status==='pending';}).length;
  var rota      = orders.filter(function(o){return o.status==='routed';}).length;
  var entregues = orders.filter(function(o){return o.status==='delivered';}).length;
  var falha     = orders.filter(function(o){return o.status==='failed';}).length;
  var pesoTotal = orders.reduce(function(s,o){return s+(parseFloat(o.weight_kg)||0);},0);
  var el = function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
  el('pk-pendentes',pendentes); el('pk-rota',rota); el('pk-entregues',entregues);
  el('pk-falha',falha); el('pk-peso',pesoTotal.toFixed(0)+' kg');
  var badge=document.getElementById('badge-pedidos');
  if(badge) badge.textContent=pendentes;
}

function renderOrders(orders) {
  var tbody=document.getElementById('orders-tbody');
  if(!tbody) return;
  if(!orders.length){tbody.innerHTML='<tr><td colspan="11" class="loading-state">Nenhum pedido encontrado</td></tr>';return;}
  var topLabel={'1000':'Venda','1007':'Bonif.','1008':'Consig.','1009':'Troca','1010':'Pre-ped.'};
  tbody.innerHTML=orders.map(function(o){
    var top=o.order_type||o.notes||'—';
    var tl=topLabel[top]||top;
    var gps=o.lat&&o.lng?'<span style="color:#10b981">OK</span>':'<span style="color:#f87171">—</span>';
    var eid=o.external_id||o.id.slice(0,8);
    return '<tr>'+
      '<td><input type="checkbox" class="order-chk" data-id="'+o.id+'" onchange="toggleOrderChk(this.dataset.id,this.checked)"></td>'+
      '<td style="font-family:monospace;color:#64B4FF;font-size:11px">'+eid+'</td>'+
      '<td><b>'+(o.recipient_name||'—')+'</b></td>'+
      '<td style="font-size:11px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+(o.address||'—')+'</td>'+
      '<td style="color:#a78bfa;font-weight:700">'+(o.weight_kg||0)+'</td>'+
      '<td style="color:#10b981">'+(o.total_value?'R$ '+parseFloat(o.total_value).toFixed(2):'—')+'</td>'+
      '<td><span class="badge active" style="font-size:9px">'+tl+'</span></td>'+
      '<td style="font-size:11px;color:#90afd4">'+(o.time_window_start||'07:30')+'-'+(o.time_window_end||'18:00')+'</td>'+
      '<td style="text-align:center">'+gps+'</td>'+
      '<td><span class="badge '+(o.status||'pending')+'">'+(o.status||'pending')+'</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+o.id+'" onclick="verDetalhePedido(this.dataset.id)">Ver</button></td>'+
      '</tr>';
  }).join('');
}

function filterOrdersLocal() {
  var busca  = document.getElementById('f-search')  ? document.getElementById('f-search').value.toLowerCase()  : '';
  var regiao = document.getElementById('f-regiao')  ? document.getElementById('f-regiao').value  : '';
  var top    = document.getElementById('f-top')     ? document.getElementById('f-top').value     : '';
  var f=_allOrders.filter(function(o){
    var mb=!busca||(o.recipient_name||'').toLowerCase().indexOf(busca)>=0||(o.external_id||'').toLowerCase().indexOf(busca)>=0||(o.address||'').toLowerCase().indexOf(busca)>=0;
    var mr=!regiao||(o.regiao||'').indexOf(regiao)>=0;
    var mt=!top||(o.order_type||o.notes||'').indexOf(top)>=0;
    return mb&&mr&&mt;
  });
  renderOrders(f);
  var el=document.getElementById('orders-count');
  if(el) el.textContent=f.length+' pedidos';
}

function filtroRapido(status) {
  var sel=document.getElementById('f-status');
  if(sel){sel.value=status;loadOrders();}
}

// ── IMPORTAÇÃO CSV/XLS ───────────────────────────────────────────
function abrirImportacaoCSV() {
  _csvDados=[];
  var safe=function(id,fn){var e=document.getElementById(id);if(e)fn(e);};
  safe('csv-nome-arquivo',function(e){e.textContent='Nenhum arquivo selecionado';});
  safe('csv-preview',function(e){e.style.display='none';});
  safe('csv-opcoes',function(e){e.style.display='none';});
  safe('csv-resultado',function(e){e.style.display='none';});
  safe('btn-importar-csv',function(e){e.disabled=true;e.style.opacity='.5';e.textContent='Importar Pedidos';});
  safe('csv-file-input',function(e){e.value='';});
  var modal=document.getElementById('modal-importacao-csv');
  if(modal) modal.style.display='flex';
}

function lerArquivoCSV(input) {
  console.log('lerArquivoCSV chamado!', input.files[0]);
  var file=input.files[0];
  if(!file) return;
  var ext=file.name.split('.').pop().toLowerCase();
  var nomeEl=document.getElementById('csv-nome-arquivo');
  if(nomeEl) nomeEl.textContent=file.name+' ('+(file.size/1024).toFixed(1)+' KB)';
  var reader=new FileReader();
  if(ext==='xls'||ext==='xlsx'){
    reader.onload=function(e){
      try{
        var wb=XLSX.read(e.target.result,{type:'binary'});
        var ws=wb.Sheets[wb.SheetNames[0]];
        var rows=XLSX.utils.sheet_to_json(ws,{header:1,defval:''});
        processarLinhas(rows);
      }catch(err){toast('Erro ao ler XLS: '+err.message,'error');}
    };
    reader.readAsBinaryString(file);
  } else {
    reader.onload=function(e){
      var text=e.target.result;
      var sep=text.indexOf(';')>=0?';':',';
      var linhas=text.split('\n').filter(function(l){return l.trim();});
      var rows=linhas.map(function(l){return l.split(sep).map(function(c){return c.trim().replace(/^"|"$/g,'');});});
      processarLinhas(rows);
    };
    reader.readAsText(file,'latin1');
  }
}

function parseBR(v) {
  if(!v) return 0;
  var s=String(v).trim();
  if(s.indexOf(',')>=0&&s.indexOf('.')>=0) return parseFloat(s.replace(/\./g,'').replace(',','.'))||0;
  if(s.indexOf(',')>=0) return parseFloat(s.replace(',','.'))||0;
  return parseFloat(s)||0;
}

function processarLinhas(rows) {
  console.log('processarLinhas chamado! rows:', rows.length, 'primeira linha:', rows[0]);
  var headerIdx=0;
  for(var r=0;r<Math.min(10,rows.length);r++){
    var norm=rows[r].map(function(h){return String(h||'').toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');});
    if(norm.some(function(h){return h.indexOf('NUNOTA')>=0||h.indexOf('NRO')>=0||h.indexOf('NOTA')>=0||h.indexOf('PARCEIRO')>=0||h.indexOf('PESO')>=0;})){
      headerIdx=r;
      console.log('Cabecalho encontrado na linha', r+1, ':', rows[r]);
      break;
    }
  }
  console.log('headerIdx:', headerIdx, 'header:', rows[headerIdx]);
  var header=rows[headerIdx].map(function(h){
    return String(h||'').trim().toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9_ ]/g,'').trim();
  });
  var mapa={
    id:['NRO UNICO','NUNOTA','NUMNOTA','NRO NOTA','NUMERO'],
    cliente:['NOME PARCEIRO','NOMEPARC','NOME PARC','CLIENTE','RAZAOSOCIAL'],
    codparc:['PARCEIRO','CODPARC','COD PARC'],
    endereco:['ENDERECO','ENDCLIENTE','LOGRADOURO'],
    cidade:['CIDADE','MUNICIPIO'],
    peso:['PESO','PESOLIQ','PESOBRUTO'],
    volume:['VOLUME','VOL','CUBAGEM'],
    data:['DT NEG','DTNEG','DATA','DATAPED'],
    top:['DESCRICAO TIPO DE OPERACAO','CODTIPOPER','TIPOPER','TOP'],
    valor:['VLR NOTA','VLRNOTA','VALOR'],
    regiao:['CENTRO RESULTADO','ROTA','REGIAO','ZONA'],
  };
  var idx={};
  Object.keys(mapa).forEach(function(campo){
    idx[campo]=-1;
    mapa[campo].forEach(function(o){
      if(idx[campo]===-1){
        var found=header.findIndex(function(h){return h===o||h.indexOf(o)>=0;});
        if(found!==-1) idx[campo]=found;
      }
    });
  });
  _csvDados=[];
  var erros=0;
  for(var i=headerIdx+1;i<rows.length;i++){
    var cols=rows[i].map(function(c){return String(c||'').trim();});
    if(cols.join('').length===0) continue;
    var get=function(c){return idx[c]!==-1?cols[idx[c]]||'':'';};
    var nunota=get('id');
    var peso=parseBR(get('peso'));
    if(!nunota){erros++;continue;} // peso pode ser 0 para bonificacoes
    var clienteBase=buscarClientePorCodparc(parseInt(get('codparc')));
    _csvDados.push({
      external_id:'SNK-'+nunota,
      recipient_name:(clienteBase&&clienteBase.nome)||get('cliente')||'CODPARC '+get('codparc'),
      address:(clienteBase&&clienteBase.endereco)||([get('endereco'),get('cidade')||'Manaus'].filter(Boolean).join(', ')+' - AM'),
      codparc:parseInt(get('codparc'))||null,
      lat:(clienteBase&&clienteBase.lat)||null,
      lng:(clienteBase&&clienteBase.lng)||null,
      time_window_end:(clienteBase&&clienteBase.tempo_entrega)?String(parseInt(clienteBase.tempo_entrega)):'60',
      weight_kg:peso,volume_m3:parseBR(get('volume')),total_value:parseBR(get('valor')),
      order_type:(function(){
        var t=get('top')||'';
        // Normaliza TOPs do Sankhya para TOPs do app
        var mapa={'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};
        return mapa[t]||t||'1000';
      })(),delivery_date:get('data')||new Date().toISOString().slice(0,10),
      regiao:(clienteBase&&clienteBase.regiao)||(clienteBase&&clienteBase.rota)||get('regiao')||null,
      status:'pending',priority:1,
      lat:(clienteBase&&clienteBase.lat)||null,lng:(clienteBase&&clienteBase.lng)||null,
      time_window_start:'07:30',time_window_end:'18:00',
    });
  }
  var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
  el('csv-total-linhas',rows.length-1-headerIdx);
  el('csv-validos',_csvDados.length);
  el('csv-erros',erros);
  var preview=_csvDados.slice(0,5);
  var tableEl=document.getElementById('csv-preview-table');
  if(tableEl){
    tableEl.innerHTML='<thead><tr style="background:#1e3a5c">'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Pedido</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Cliente</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">Peso</th>'+
      '<th style="padding:6px 10px;font-size:10px;color:#64B4FF">TOP</th>'+
      '</tr></thead><tbody>'+
      preview.map(function(p){return '<tr>'+
        '<td style="padding:5px 10px;font-family:monospace;font-size:11px;color:#64B4FF">'+p.external_id+'</td>'+
        '<td style="padding:5px 10px;font-size:11px">'+p.recipient_name+'</td>'+
        '<td style="padding:5px 10px;font-size:11px;color:#f59e0b">'+p.weight_kg+' kg</td>'+
        '<td style="padding:5px 10px;font-size:11px;color:#a78bfa">TOP '+p.order_type+'</td>'+
        '</tr>';}).join('')+
      '</tbody>';
  }
  var prev=document.getElementById('csv-preview');
  var opts=document.getElementById('csv-opcoes');
  if(prev) prev.style.display='block';
  if(opts) opts.style.display='block';
  var btn=document.getElementById('btn-importar-csv');
  if(btn&&_csvDados.length>0){
    btn.disabled=false;btn.style.opacity='1';btn.style.cursor='pointer';
    toast(_csvDados.length+' pedidos encontrados!','success');
  } else {
    toast('Nenhum pedido valido!','error');
  }
}

async function importarCSV() {
  if(_csvDados.length===0){toast('Nenhum dado!','error');return;}
  var btn=document.getElementById('btn-importar-csv');
  btn.disabled=true;btn.textContent='Importando...';
  var limparEl=document.getElementById('csv-opt-limpar');
  var hojeEl=document.getElementById('csv-opt-data-hoje');
  var limpar=limparEl?limparEl.checked:true;
  var usarHoje=hojeEl?hojeEl.checked:true;
  var hoje=new Date().toISOString().slice(0,10);
  var importados=0,erros=0;
  if(limpar){
    try{
      btn.textContent='Limpando antigos...';
      var ords=await api('GET','/orders?status=pending&limit=500');
      for(var o of ords){try{await api('DELETE','/orders/'+o.id);}catch(e){}}
    }catch(e){}
  }
  for(var pedido of _csvDados){
    if(usarHoje) pedido.delivery_date=hoje;
    try{await api('POST','/orders',pedido);importados++;}
    catch(e){erros++;console.log('Erro:',pedido.external_id,e.message);}
    btn.textContent=''+importados+'/'+_csvDados.length+'...';
  }
  toast(importados+' pedidos importados!','success');
  btn.textContent='Concluido';
  setTimeout(function(){
    loadOrders();
    var m=document.getElementById('modal-importacao-csv');
    if(m) m.style.display='none';
  },1500);
}

// ── VEÍCULOS ─────────────────────────────────────────────────────
async function loadVehicles() {
  try{
    var data=await api('GET','/vehicles');
    var tbody=document.getElementById('vehicles-tbody');
    if(!tbody) return;
    if(!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhum veiculo</td></tr>';return;}
    tbody.innerHTML=data.map(function(v){return '<tr>'+
      '<td><b style="color:#64B4FF">'+(v.vda||'—')+'</b></td>'+
      '<td style="font-family:monospace">'+v.plate+'</td>'+
      '<td>'+v.model+'</td><td>'+v.type+'</td>'+
      '<td>'+v.capacity_kg+'kg</td>'+
      '<td>'+(v.fuel_type||'diesel')+'</td>'+
      '<td>'+(v.km_per_liter||'—')+' km/L</td>'+
      '<td>'+(v.daily_cost?'R$'+v.daily_cost:'—')+'</td>'+
      '<td><span class="badge '+(v.status||'active')+'">'+(v.status||'active')+'</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+v.id+'" onclick="abrirModalVeiculo(this.dataset.id)">Editar</button></td>'+
      '</tr>';}).join('');
  }catch(e){toast('Erro: '+e.message,'error');}
}
function abrirModalVeiculo(id){
  // Limpa form
  ['v-vda','v-plate','v-model','v-kg','v-m3','v-pallets','v-comp','v-larg','v-alt',
   'v-kml','v-preco-comb','v-ipva','v-manut','v-custo-dia','v-custo-oleo'].forEach(function(id){
    var e=document.getElementById(id); if(e) e.value='';
  });
  var titulo=document.getElementById('modal-veic-titulo');
  if(titulo) titulo.textContent='Novo Veículo';
  _editVeiculoId = null;
  window.veiculoEditId = null;
  var h=document.getElementById('v-edit-id'); if(h) h.value='';
  document.getElementById('modal-veiculo-completo').style.display='flex';
}

async function editarVeiculo(id){
  _editVeiculoId = id;
  try{
    var data = await api('GET','/vehicles');
    var v = data.find(function(x){return x.id===id;});
    if(!v){ toast('Veículo não encontrado!','error'); return; }

    console.log('Editando veículo:', v);

    document.getElementById('modal-veiculo-completo').style.display='flex';

    function setVal(eid, val){
      var e = document.getElementById(eid);
      if(e && val!==null && val!==undefined && val!=='') e.value = val;
    }

    setVal('v-vda',         v.vda);
    setVal('v-plate',       v.plate);
    setVal('v-model',       v.model);
    setVal('v-type',        v.type);
    setVal('v-kg',          v.capacity_kg);
    setVal('v-m3',          v.capacity_m3);
    setVal('v-pallets',     v.pallets);
    setVal('v-comp',        v.bau_comp);
    setVal('v-larg',        v.bau_larg);
    setVal('v-alt',         v.bau_alt);
    setVal('v-combustivel', v.fuel_type);
    setVal('v-kml',         v.km_per_liter);
    setVal('v-preco-comb',  v.fuel_price);
    setVal('v-ipva',        v.ipva_anual);
    setVal('v-manut',       v.manut_mes);
    setVal('v-custo-dia',   v.daily_cost);
    setVal('v-ult-oleo',    v.oleo_ult_data);
    setVal('v-prox-oleo',   v.oleo_prox_data);
    setVal('v-custo-oleo',  v.oleo_custo);
    setVal('v-status',      v.status);

    var titulo = document.getElementById('modal-veic-titulo');
    if(titulo) titulo.textContent = 'Editar — ' + (v.vda||v.plate);

    window.veiculoEditId = id;
    var hiddenId = document.getElementById('v-edit-id');
    if(hiddenId) hiddenId.value = id;
    console.log('veiculoEditId setado:', window.veiculoEditId);

    if(v.bau_comp && v.bau_larg && v.bau_alt) calcularCubagem();

  }catch(e){ toast('Erro: '+e.message,'error'); }
}
async function salvarVeiculoCompleto(editId){
  editId = editId || window.veiculoEditId || null;
  console.log('editId final:', editId, 'window:', window.veiculoEditId);("editId ao salvar:", editId, "| _editVeiculoId:", typeof _editVeiculoId !== "undefined" ? _editVeiculoId : "NAO DEFINIDA");
  var body = {
    vda:          document.getElementById('v-vda').value,
    plate:        document.getElementById('v-plate').value,
    model:        document.getElementById('v-model').value,
    type:         document.getElementById('v-type').value,
    capacity_kg:  parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:  parseFloat(document.getElementById('v-m3').value)||0,
    pallets:      parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:     parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:     parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:      parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:    document.getElementById('v-combustivel').value,
    km_per_liter: parseFloat(document.getElementById('v-kml').value)||0,
    fuel_price:   parseFloat(document.getElementById('v-preco-comb').value)||0,
    ipva_anual:   parseFloat(document.getElementById('v-ipva').value)||0,
    manut_mes:    parseFloat(document.getElementById('v-manut').value)||0,
    daily_cost:   parseFloat(document.getElementById('v-custo-dia').value)||0,
    oleo_ult_data: document.getElementById('v-ult-oleo').value||null,
    oleo_prox_data:document.getElementById('v-prox-oleo').value||null,
    oleo_custo:   parseFloat(document.getElementById('v-custo-oleo').value)||0,
    status:       document.getElementById('v-status').value,
  };
  if(!body.plate||!body.model){toast('Placa e modelo obrigatórios!','error');return;}
  try{
    if(editId){
      // PATCH — atualiza sem verificar placa duplicada
      await api('PATCH','/vehicles/'+editId, body);
      toast('Veículo atualizado com sucesso!','success');
    } else {
      await api('POST','/vehicles', body);
      toast('Veículo cadastrado!','success');
    }
    var modal = document.getElementById('modal-veiculo-completo');
    modal.style.display='none';
    _editVeiculoId = null;
    loadVehicles();
  }catch(e){toast('Erro ao salvar: '+e.message,'error');}
}
async function calcularCubagem(){
  var comp = parseFloat(document.getElementById('v-comp').value)||0;
  var larg = parseFloat(document.getElementById('v-larg').value)||0;
  var alt  = parseFloat(document.getElementById('v-alt').value)||0;
  var elInfo = document.getElementById('v-cubagem-calc');

  if(!comp || !larg || !alt){
    if(elInfo) elInfo.textContent = 'Cubagem calculada: — m³ (preencha as dimensões)';
    return;
  }

  var cubagem = comp * larg * alt;

  // Calcula quantos pallets cabem — busca pallets carregados
  try{
    var pallets = await api('GET','/producao/pallets');
    var itens   = await api('GET','/producao/itens');

    var pallet = pallets.length > 0 ? pallets[0] : null;
    var pComp  = pallet ? parseFloat(pallet.comprimento)||1.20 : 1.20;
    var pLarg  = pallet ? parseFloat(pallet.largura)||1.00    : 1.00;

    // Quantos pallets cabem no comprimento e largura do baú
    var colsComp = Math.floor(comp / pComp);
    var colsLarg = Math.floor(larg / pLarg);
    var totalPallets = colsComp * colsLarg;

    // Atualiza campo de pallets
    var elPallets = document.getElementById('v-pallets');
    if(elPallets && totalPallets > 0) elPallets.value = totalPallets;

    // Atualiza capacity_m3
    var elM3 = document.getElementById('v-m3');
    if(elM3) elM3.value = cubagem.toFixed(2);

    // Monta tabela de tipos de gelo x pallets
    var configs = [
      {nome:'Gelo 5kg',  kg:5,  un:180},
      {nome:'Gelo 10kg', kg:10, un:110},
      {nome:'Gelo 20kg', kg:20, un:50},
      {nome:'Gelo 40kg', kg:40, un:27},
    ];

    var linhas = configs.map(function(cfg){
      var item = itens.find(function(it){
        var n = (it.nome||'').toLowerCase().replace(/\s/g,'');
        return n.indexOf(cfg.kg+'kg')>=0;
      });
      var pesoUnit = item ? parseFloat(item.peso) : cfg.kg;
      var pesoTotal = (cfg.un * pesoUnit * totalPallets) + (6 * totalPallets); // +6kg tara/pallet
      return '<tr style="border-bottom:1px solid #1e3a5c">'+
        '<td style="padding:4px 8px;color:#64B4FF">'+cfg.nome+'</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#f59e0b">'+cfg.un+' un/pallet</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#a78bfa">'+totalPallets+' pallets</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#10b981">'+cfg.un*totalPallets+' un total</td>'+
        '<td style="padding:4px 8px;text-align:center;color:#f87171">'+pesoTotal.toFixed(0)+' kg</td>'+
        '</tr>';
    }).join('');

    if(elInfo) elInfo.innerHTML =
      '<div style="margin-bottom:8px">'+
        '<b style="color:#64B4FF">Cubagem do baú: '+cubagem.toFixed(3)+' m³</b> &nbsp;|&nbsp; '+
        '<b style="color:#f59e0b">'+totalPallets+' pallets</b> ('+pComp+'x'+pLarg+'m cada)'+
      '</div>'+
      '<table style="width:100%;font-size:11px">'+
        '<thead><tr style="background:#1e3a5c">'+
          '<th style="padding:4px 8px;text-align:left;color:#90afd4">Tipo</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Un/Pallet</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Pallets</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Total Un.</th>'+
          '<th style="padding:4px 8px;color:#90afd4">Peso Total</th>'+
        '</tr></thead>'+
        '<tbody>'+linhas+'</tbody>'+
      '</table>';

  } catch(e) {
    if(elInfo) elInfo.textContent = 'Cubagem: '+cubagem.toFixed(3)+' m³ | Erro ao calcular pallets: '+e.message;
  }
}
function toggleMotivoParada(){}
function saveVehicle(){}

// ── MOTORISTAS ───────────────────────────────────────────────────
async function loadDrivers() {
  try{
    var tipo=document.getElementById('f-driver-tipo')?document.getElementById('f-driver-tipo').value:'';
    var data=await api('GET','/drivers'+(tipo?'?tipo='+tipo:''));
    var tbody=document.getElementById('drivers-tbody');
    if(!tbody) return;
    if(!data.length){tbody.innerHTML='<tr><td colspan="11" class="loading-state">Nenhum cadastro</td></tr>';return;}
    tbody.innerHTML=data.map(function(d){return '<tr>'+
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
      '<td><button class="btn btn-sm btn-secondary" data-id="'+d.id+'" onclick="abrirModalMotorista(this.dataset.id)">Editar</button></td>'+
      '</tr>';}).join('');
  }catch(e){toast('Erro: '+e.message,'error');}
}
function abrirModalMotorista(id){document.getElementById('modal-motorista-completo').style.display='flex';}
function salvarMotoristaCompleto(){toast('Cadastro salvo!','success');}
function selecionarTipoDriver(tipo){document.getElementById('d-tipo').value=tipo;}
function saveDriver(){}
function uploadCNH(){}

// ── ROTAS ────────────────────────────────────────────────────────
async function loadRoutes() {
  var dateEl=document.getElementById('routes-date');
  var statusEl=document.getElementById('routes-status');
  var date=dateEl?dateEl.value:new Date().toISOString().slice(0,10);
  var status=statusEl?statusEl.value:'';
  try{
    var data=await api('GET','/routes?date='+date+(status?'&status='+status:''));
    var tbody=document.getElementById('routes-tbody');
    if(!tbody) return;
    if(!data.length){tbody.innerHTML='<tr><td colspan="10" class="loading-state">Nenhuma rota — grave uma carga na Conferência Master</td></tr>';return;}
    var statusLabel={'optimized':'Conferida','released':'Liberada','executing':'Em Execução','done':'Concluída','draft':'Rascunho','cancelled':'Cancelada'};
    tbody.innerHTML=data.map(function(r){
      var pct=r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;
      var trip=r.trip_number||'—';
      var btnLiberar='';
      if(r.status==='optimized'){
        btnLiberar='<button class="btn btn-sm" style="background:rgba(16,185,129,.2);border:1px solid #10b981;color:#10b981" '+
          'onclick="liberarRota(''+r.route_id+'')" title="Liberar para motorista">🟢 Liberar</button>';
      }
      return '<tr>'+
        '<td><input type="checkbox" class="rota-chk" data-id="'+r.route_id+'"></td>'+
        '<td><b style="font-family:monospace;color:#64B4FF;font-size:12px">'+trip+'</b></td>'+
        '<td><b style="color:#64B4FF">'+(r.vehicle_plate||r.vda||'—')+'</b></td>'+
        '<td>'+(r.driver_name||'—')+'</td>'+
        '<td style="font-size:12px">'+(r.date||'—')+'</td>'+
        '<td><div style="display:flex;align-items:center;gap:8px">'+
        '<div style="flex:1;background:#1e3a5c;border-radius:3px;height:6px">'+
        '<div style="height:100%;background:#10b981;border-radius:3px;width:'+pct+'%"></div></div>'+
        '<span style="font-size:11px;color:#90afd4">'+pct+'% ('+r.total_stops+' paradas)</span></div></td>'+
        '<td style="font-size:11px">'+(r.total_distance_km||'—')+' km</td>'+
        '<td style="font-size:12px">'+(r.planned_start||'—')+'</td>'+
        '<td><span class="badge '+(r.status||'draft')+'">'+(statusLabel[r.status]||r.status||'draft')+'</span></td>'+
        '<td style="display:flex;gap:6px;flex-wrap:wrap">'+
          btnLiberar+
          '<button class="btn btn-sm btn-secondary" data-id="'+r.route_id+'" onclick="verProgressoRota(this.dataset.id)">👁 Ver</button>'+
        '</td>'+
        '</tr>';
    }).join('');
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function liberarRota(routeId) {
  if(!confirm('Liberar esta rota para o motorista?')) return;
  try{
    await api('POST', '/routes/'+routeId+'/liberar');
    toast('✅ Rota liberada! Motorista já pode ver no app.','success');
    loadRoutes();
  }catch(e){toast('Erro: '+e.message,'error');}
}
function toggleTodasRotas(checked){}
function imprimirRomaneiosSelecionados(){}
function verProgressoRota(id){}

// ── PRODUÇÃO ─────────────────────────────────────────────────────
async function loadProducao(){switchProducaoTab('pallet');}
function switchProducaoTab(tab){
  var secs={pallet:'section-pallets',item:'section-itens',carregado:'section-carregado'};
  Object.keys(secs).forEach(function(k){
    var el=document.getElementById(secs[k]);
    if(el) el.style.display=k===tab?'block':'none';
  });
  // Atualiza botao de novo
  var btnNovo=document.getElementById('btn-novo-producao');
  if(btnNovo){
    if(tab==='pallet'){btnNovo.textContent='+ Novo Pallet';btnNovo.onclick=function(){abrirModalPallet();};}
    else if(tab==='item'){btnNovo.textContent='+ Novo Item';btnNovo.onclick=function(){abrirModalItem();};}
    else{btnNovo.textContent='+ Novo';btnNovo.onclick=null;}
  }
  if(tab==='pallet')    loadPallets();
  if(tab==='item')      loadItens();
  if(tab==='carregado') loadPalletsCarregados();
}
async function loadPallets(){
  try{
    var data=await api('GET','/producao/pallets');
    var tbody=document.getElementById('pallets-tbody');
    if(!tbody) return;
    tbody.innerHTML=data.length?data.map(function(p){return '<tr>'+
      '<td><b>'+p.nome+'</b></td>'+
      '<td>'+(p.comprimento||0)+'</td>'+
      '<td>'+(p.largura||0)+'</td>'+
      '<td>'+(p.altura||0)+'</td>'+
      '<td style="color:#2dd4bf">'+(p.cubagem||0)+'</td>'+
      '<td>'+(p.peso_max||0)+' kg</td>'+
      '<td><span class="badge active">Ativo</span></td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+p.id+'" onclick="editarPallet(this.dataset.id)">✏️ Editar</button></td>'+
      '</tr>';}).join('')
    :'<tr><td colspan="8" class="loading-state">Nenhum pallet cadastrado</td></tr>';
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function editarPallet(id){
  try{
    var data=await api('GET','/producao/pallets');
    var p=data.find(function(x){return x.id===id;});
    if(!p) return;
    document.getElementById('p-nome').value=p.nome||'';
    document.getElementById('p-comp').value=p.comprimento||'';
    document.getElementById('p-larg').value=p.largura||'';
    document.getElementById('p-alt').value=p.altura||'';
    document.getElementById('p-peso-max').value=p.peso_max||'';
    document.getElementById('p-cubagem').value=p.cubagem||'';
    document.getElementById('p-obs').value=p.observacao||'';
    var titulo=document.getElementById('modal-pallet-titulo');
    if(titulo) titulo.textContent='Editar Pallet';
    // Guarda id para salvar
    document.getElementById('modal-pallet').dataset.editId=id;
    document.getElementById('modal-pallet').style.display='flex';
  }catch(e){toast('Erro: '+e.message,'error');}
}
async function loadItens(){
  try{
    var data=await api('GET','/producao/itens');
    var tbody=document.getElementById('itens-tbody');
    if(!tbody) return;
    tbody.innerHTML=data.length?data.map(function(it){return '<tr>'+
      '<td><b>'+(it.nome||'—')+'</b></td>'+
      '<td style="color:#f59e0b">'+(it.peso||0)+' kg</td>'+
      '<td style="font-size:11px">'+(it.comprimento||0)+'x'+(it.largura||0)+'x'+(it.altura||0)+' m</td>'+
      '<td style="font-size:11px">'+(it.observacao||'—')+'</td>'+
      '<td><button class="btn btn-sm btn-secondary" data-id="'+it.id+'" onclick="editarItem(this.dataset.id)">✏️ Editar</button></td>'+
      '</tr>';}).join('')
    :'<tr><td colspan="7" class="loading-state">Nenhum item cadastrado</td></tr>';
  }catch(e){toast('Erro: '+e.message,'error');}
}

async function editarItem(id){
  try{
    var data=await api('GET','/producao/itens');
    var it=data.find(function(x){return x.id===id;});
    if(!it) return;
    document.getElementById('i-nome').value=it.nome||'';
    document.getElementById('i-peso').value=it.peso||'';
    document.getElementById('i-comp').value=it.comprimento||'';
    document.getElementById('i-larg').value=it.largura||'';
    document.getElementById('i-alt').value=it.altura||'';
    document.getElementById('i-obs').value=it.observacao||'';
    document.getElementById('i-un-pallet').value=it.un_pallet||0;
    document.getElementById('i-top').value=it.top||'1000';
    var titulo=document.getElementById('modal-item-titulo');
    if(titulo) titulo.textContent='Editar Item';
    document.getElementById('modal-item').dataset.editId=id;
    document.getElementById('modal-item').style.display='flex';
  }catch(e){toast('Erro: '+e.message,'error');}
}
async function loadPalletsCarregados(){
  var grid=document.getElementById('pallets-carregados-grid');
  if(!grid) return;

  try{
    var pallets = await api('GET','/producao/pallets');
    var itens   = await api('GET','/producao/itens');

    // Configurações fixas: tipo gelo -> qtd unidades por pallet
    var configs = [
      {kg:5,  un:180, cor:'#64B4FF',  emoji:'🧊'},
      {kg:10, un:110, cor:'#2dd4bf',  emoji:'🧊'},
      {kg:20, un:50,  cor:'#a78bfa',  emoji:'🧊'},
      {kg:40, un:27,  cor:'#f59e0b',  emoji:'🧊'},
    ];

    // Pallet base padrão (usa o primeiro cadastrado ou default)
    var palletBase = pallets.length > 0 ? pallets[0] : {
      nome:'Padrão', comprimento:1.20, largura:1.00, altura:0.15,
      cubagem:0.18, peso_max:1000
    };

    var cards = configs.map(function(cfg){
      // Encontra item correspondente ao kg
      // Busca item pelo nome (ex: 'Gelo 5kg', 'Gelo 5 kg')
      var item = itens.find(function(it){
        var nome = (it.nome||'').toLowerCase().replace(/\s/g,'');
        return nome.indexOf(cfg.kg+'kg')>=0 || nome.indexOf(cfg.kg+' kg')>=0;
      });
      // Fallback: busca pelo índice da config
      if(!item && itens[configs.indexOf(cfg)]) item = itens[configs.indexOf(cfg)];

      // Dimensões do pallet base
      var pComp = parseFloat(palletBase.comprimento)||1.20;
      var pLarg = parseFloat(palletBase.largura)||1.00;
      var pAlt  = parseFloat(palletBase.altura)||0.15;
      var pPeso = parseFloat(palletBase.peso_max)||25;

      // Dimensões do item
      var iComp = item ? parseFloat(item.comprimento)||0.30 : 0.30;
      var iLarg = item ? parseFloat(item.largura)||0.20    : 0.20;
      var iAlt  = item ? parseFloat(item.altura)||0.10     : 0.10;

      // Calcula empilhamento
      // Quantos itens cabem por camada (área do pallet / área do item)
      var itensPorCamada = Math.floor((pComp/iComp)) * Math.floor((pLarg/iLarg));
      // Quantas camadas cabem na altura útil (considera 1.50m altura total - pallet base)
      var alturaUtil = 1.50 - pAlt;
      var camadas = Math.floor(alturaUtil / iAlt);
      var totalUn = itensPorCamada * camadas;

      // Usa a qtd padrão da config se o cálculo der muito diferente
      var unFinal = totalUn > 0 ? Math.min(totalUn, cfg.un*2) : cfg.un;
      // Para simplificar, usa a configuração padrão
      unFinal = cfg.un;

      // Peso total — usa peso REAL do item cadastrado
      var pesoUnitario = item ? parseFloat(item.peso) : cfg.kg;
      var pesoItens    = cfg.un * pesoUnitario;
      var pesoPallet   = parseFloat(palletBase.peso_max)||25;
      var pesoTotal    = pesoItens + pesoPallet;

      // Cubagem total do pallet carregado
      // Pallet base + volume ocupado pelos itens empilhados
      var altTotal   = pAlt + (Math.ceil(cfg.un / Math.max(1, Math.floor((pComp/iComp)*Math.floor((pLarg/iLarg))))) * iAlt);
      var cubTotal   = pComp * pLarg * Math.min(altTotal, 1.80);

      // Pct capacidade (peso)
      var pctPeso = Math.min(100, Math.round(pesoItens/1000*100));

      return '<div class="card" style="padding:0;margin-bottom:0;border:1px solid '+cfg.cor+';border-radius:12px;overflow:hidden">'+
        '<div style="background:'+cfg.cor+'22;padding:14px;border-bottom:1px solid '+cfg.cor+'44;display:flex;align-items:center;gap:10px">'+
          '<span style="font-size:28px">'+cfg.emoji+'</span>'+
          '<div>'+
            '<div style="font-size:16px;font-weight:800;color:'+cfg.cor+'">Gelo '+cfg.kg+' kg</div>'+
            '<div style="font-size:11px;color:#90afd4">'+palletBase.nome+' + '+cfg.un+' unidades</div>'+
          '</div>'+
        '</div>'+
        '<div style="padding:14px;display:grid;gap:8px">'+
          '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">'+
            '<div style="background:#0a1628;border-radius:8px;padding:10px;text-align:center">'+
              '<div style="font-size:20px;font-weight:800;color:'+cfg.cor+'">'+cfg.un+'</div>'+
              '<div style="font-size:10px;color:#90afd4">un/pallet</div>'+
            '</div>'+
            '<div style="background:#0a1628;border-radius:8px;padding:10px;text-align:center">'+
              '<div style="font-size:20px;font-weight:800;color:#f87171">'+(pesoItens+pesoPallet).toFixed(0)+'</div>'+
              '<div style="font-size:10px;color:#90afd4">kg total</div>'+
            '</div>'+
            '<div style="background:#0a1628;border-radius:8px;padding:10px;text-align:center">'+
              '<div style="font-size:20px;font-weight:800;color:#2dd4bf">'+cubTotal.toFixed(3)+'</div>'+
              '<div style="font-size:10px;color:#90afd4">m³ total</div>'+
            '</div>'+
          '</div>'+
          '<div>'+
            '<div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:3px">'+
              '<span style="color:#90afd4">Peso da carga</span>'+
              '<span style="color:'+cfg.cor+'">'+pesoItens+' kg</span>'+
            '</div>'+
            '<div style="background:#1e3a5c;border-radius:4px;height:6px">'+
              '<div style="height:100%;background:'+cfg.cor+';border-radius:4px;width:'+pctPeso+'%"></div>'+
            '</div>'+
          '</div>'+
          '<div style="font-size:10px;color:#90afd4;display:grid;grid-template-columns:1fr 1fr;gap:4px">'+
            '<span>📦 Pallet: '+pComp+'x'+pLarg+'x'+pAlt+' m</span>'+
            '<span>🧊 Item: '+iComp+'x'+iLarg+'x'+iAlt+' m</span>'+
            '<span>⚖️ Peso unit.: '+pesoUnitario+' kg</span>'+
            '<span>📐 Alt total: '+Math.min(altTotal,1.80).toFixed(2)+' m</span>'+
          '</div>'+
        '</div>'+
      '</div>';
    });

    grid.innerHTML = cards.join('');

  }catch(e){
    grid.innerHTML='<div class="loading-state" style="grid-column:1/-1">Erro: '+e.message+'<br><small>Cadastre pallets e itens primeiro</small></div>';
  }
}
function abrirModalPallet(){document.getElementById('modal-pallet').style.display='flex';}
function abrirModalItem(){document.getElementById('modal-item').style.display='flex';}
async function salvarPallet(){
  var modal=document.getElementById('modal-pallet');
  var editId=modal?modal.dataset.editId:null;
  var body={
    nome:document.getElementById('p-nome').value,
    comprimento:parseFloat(document.getElementById('p-comp').value)||0,
    largura:parseFloat(document.getElementById('p-larg').value)||0,
    altura:parseFloat(document.getElementById('p-alt').value)||0,
    peso_max:parseFloat(document.getElementById('p-peso-max').value)||0,
    cubagem:parseFloat(document.getElementById('p-cubagem').value)||0,
    observacao:document.getElementById('p-obs').value
  };
  if(!body.nome){toast('Nome obrigatório!','error');return;}
  try{
    if(editId){
      await api('PATCH','/producao/pallets/'+editId,body);
      toast('Pallet atualizado!','success');
    } else {
      await api('POST','/producao/pallets',body);
      toast('Pallet criado!','success');
    }
    if(modal){modal.style.display='none';delete modal.dataset.editId;}
    var titulo=document.getElementById('modal-pallet-titulo');
    if(titulo) titulo.textContent='Novo Pallet';
    loadPallets();
  }catch(e){toast('Erro: '+e.message,'error');}
}
async function salvarItem(){
  var modal=document.getElementById('modal-item');
  var editId=modal?modal.dataset.editId:null;
  var body={
    nome:document.getElementById('i-nome').value,
    peso:parseFloat(document.getElementById('i-peso').value)||0,
    comprimento:parseFloat(document.getElementById('i-comp').value)||0,
    largura:parseFloat(document.getElementById('i-larg').value)||0,
    altura:parseFloat(document.getElementById('i-alt').value)||0,
    observacao:document.getElementById('i-obs').value,
    un_pallet:parseInt(document.getElementById('i-un-pallet').value)||0,
    top:document.getElementById('i-top').value||'1000'
  };
  if(!body.nome){toast('Nome obrigatório!','error');return;}
  try{
    if(editId){
      await api('PATCH','/producao/itens/'+editId,body);
      toast('Item atualizado!','success');
    } else {
      await api('POST','/producao/itens',body);
      toast('Item criado!','success');
    }
    if(modal){modal.style.display='none';delete modal.dataset.editId;}
    var titulo=document.getElementById('modal-item-titulo');
    if(titulo) titulo.textContent='Novo Item';
    loadItens();
  }catch(e){toast('Erro: '+e.message,'error');}
}
function salvarPalletCarregado(){toast('Configuracao salva!','success');}
function calcPalletCubagem(){
  var c=parseFloat(document.getElementById('p-comp').value)||0;
  var l=parseFloat(document.getElementById('p-larg').value)||0;
  var a=parseFloat(document.getElementById('p-alt').value)||0;
  var cub=document.getElementById('p-cubagem');
  if(cub && c&&l&&a) cub.value=(c*l*a).toFixed(4);
}
function calcItemCubagem(){
  var c=parseFloat(document.getElementById('i-comp').value)||0;
  var l=parseFloat(document.getElementById('i-larg').value)||0;
  var a=parseFloat(document.getElementById('i-alt').value)||0;
  var cub=document.getElementById('i-cubagem');
  if(cub && c&&l&&a) cub.value=(c*l*a).toFixed(4);
}
function calcPalletCarregado(){}
function selecionarTipoPallet(kg){}

// ── OCORRÊNCIAS ──────────────────────────────────────────────────
async function loadOcorrencias(){
  var tbody=document.getElementById('oc-tbody');
  if(!tbody) return;
  try{
    var data=await api('GET','/ocorrencias');
    var kpis={pendente:0,em_tratamento:0,critica:0,resolvida:0};
    data.forEach(function(o){if(kpis[o.status]!==undefined)kpis[o.status]++;});
    var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
    el('oc-kpi-pendentes',kpis.pendente);el('oc-kpi-tratamento',kpis.em_tratamento);
    el('oc-kpi-criticas',kpis.critica);el('oc-kpi-resolvidas',kpis.resolvida);
    tbody.innerHTML=data.length?data.map(function(o){return '<tr>'+
      '<td><span style="font-size:16px">'+(o.gravidade==='critica'?'🔴':o.gravidade==='alta'?'🟠':o.gravidade==='media'?'🟡':'🟢')+'</span></td>'+
      '<td style="font-size:11px;font-family:monospace">'+(o.created_at||'—').slice(0,16)+'</td>'+
      '<td>'+o.tipo+'</td><td>'+(o.cliente||'—')+'</td><td>'+(o.veiculo||'—')+'</td>'+
      '<td style="font-size:11px;max-width:200px">'+(o.descricao||'—')+'</td>'+
      '<td>—</td>'+
      '<td><span class="badge '+(o.status||'pendente')+'">'+o.status+'</span></td>'+
      '<td><button class="btn btn-sm btn-secondary">Ver</button></td></tr>';}).join('')
    :'<tr><td colspan="9" class="loading-state">Nenhuma ocorrencia</td></tr>';
  }catch(e){tbody.innerHTML='<tr><td colspan="9" class="loading-state">'+e.message+'</td></tr>';}
}
function abrirModalOcorrencia(){document.getElementById('modal-ocorrencia').style.display='flex';}
function filtrarOcorrencia(status){}
function selecionarGravidade(g){var e=document.getElementById('oc-gravidade-sel');if(e)e.value=g;}
function salvarOcorrencia(){toast('Ocorrencia registrada!','success');document.getElementById('modal-ocorrencia').style.display='none';}
function previewFoto(inp,img,ph,hid){}
function saveOcorrencia(){}

// ── MONITORAMENTO ────────────────────────────────────────────────
async function loadMonitoring(){}
async function loadTorreControle(){
  var mon=document.getElementById('mon-kpis');
  if(mon) mon.innerHTML='<div class="loading-state" style="grid-column:1/-1">Torre de controle em desenvolvimento</div>';
}
function toggleMapaTipo(){}
function toggleTrafegoMon(){}

// ── RELATÓRIOS ───────────────────────────────────────────────────
function setRelPeriodo(dias){
  var ate=new Date(),de=new Date();
  de.setDate(de.getDate()-dias);
  var deEl=document.getElementById('rel-de'),ateEl=document.getElementById('rel-ate');
  if(deEl) deEl.value=de.toISOString().slice(0,10);
  if(ateEl) ateEl.value=ate.toISOString().slice(0,10);
}
async function gerarRelatorio(){toast('Relatorio em desenvolvimento','info');}
function exportarCSV(){toast('Exportar CSV em desenvolvimento','info');}
function exportarPDF(){toast('Exportar PDF em desenvolvimento','info');}
function loadReports(){}

// ── ROTEIRIZAÇÃO ─────────────────────────────────────────────────


function atualizarSelecaoRot(){
  var itens = Object.values(window.rotSelecionados);
  var count    = document.getElementById('rot-count');
  var pesoEl   = document.getElementById('rot-total-peso');
  var volEl    = document.getElementById('rot-total-vol');
  var btnRot   = document.getElementById('btn-rot-map');
  var cardVeic = document.getElementById('card-sel-veiculo');

  var pesoTotal = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).weight_kg)||0); }, 0);
  var volTotal  = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).volume_m3)||0); }, 0);
  // Pallets estimados: peso máx por pallet = 700kg
  var PESO_PALLET = 700;
  var palletsEst = Math.ceil(pesoTotal / PESO_PALLET) || 0;

  if(count)  count.textContent  = itens.length;
  if(pesoEl) pesoEl.textContent = pesoTotal.toFixed(0)+' kg';
  if(volEl)  volEl.textContent  = volTotal.toFixed(2)+' m³';

  // Painel de resumo
  var painel = document.getElementById('rot-sugestao-veiculo');
  if(painel){
    painel.style.display = itens.length>0 ? 'block' : 'none';
    var el = function(id){ return document.getElementById(id); };
    if(el('sug-clientes'))   el('sug-clientes').textContent   = itens.length;
    if(el('sug-peso-total')) el('sug-peso-total').textContent = pesoTotal.toFixed(0)+' kg';
    if(el('sug-pallets'))    el('sug-pallets').textContent    = palletsEst+' pallet(s)';
  }

  if(cardVeic) cardVeic.style.display = itens.length>0 ? 'block' : 'none';
  if(btnRot){ btnRot.disabled=itens.length===0; btnRot.style.opacity=itens.length>0?'1':'0.5'; }
  renderListaSel(itens);
}

function renderListaSel(itens){
  var lista=document.getElementById('rot-lista-sel');
  if(!lista) return;
  if(!itens.length){lista.innerHTML='<div style="color:#90afd4;font-size:12px;text-align:center;padding:20px">Clique nos pins para selecionar</div>';return;}
  lista.innerHTML=itens.map(function(x,i){
    var o=x.order;
    return '<div style="display:flex;align-items:center;gap:6px;padding:6px 8px;border-bottom:1px solid #1e3a5c;font-size:12px">'+
      '<span style="background:#e8521a;color:#fff;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">'+(i+1)+'</span>'+
      '<div style="flex:1;min-width:0">'+
        '<div style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+o.recipient_name+'</div>'+
        '<div style="color:#90afd4;font-size:10px">'+o.weight_kg+' kg</div>'+
      '</div>'+
      '<button data-id="'+o.id+'" onclick="removerSelRot(this.dataset.id)" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:14px">x</button>'+
    '</div>';
  }).join('');
}

function removerSelRot(id){
  if(rotSelecionados[id]){
    rotSelecionados[id].marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
    delete rotSelecionados[id];
    atualizarSelecaoRot();
  }
}

function rotLimparTudo(){
  Object.values(window.rotSelecionados).forEach(function(x){
    x.marker.setIcon({path:google.maps.SymbolPath.CIRCLE,scale:8,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2});
  });
  window.rotSelecionados={};
  atualizarSelecaoRot();
}

function setModoSelecao(modo){
  window._rotModo = modo;
  var btnClick = document.getElementById('btn-modo-click');
  var btnArea  = document.getElementById('btn-modo-area');
  var dica     = document.getElementById('dica-modo');

  if(btnClick) btnClick.style.border = modo==='click' ? '2px solid #e8521a' : '2px solid #1e3a5c';
  if(btnClick) btnClick.style.background = modo==='click' ? 'rgba(232,82,26,.25)' : 'transparent';
  if(btnArea)  btnArea.style.border  = modo==='area'  ? '2px solid #10b981' : '2px solid #1e3a5c';
  if(btnArea)  btnArea.style.background  = modo==='area'  ? 'rgba(16,185,129,.25)' : 'transparent';

  // Para DrawingManager anterior
  if(window._drawingManager){
    window._drawingManager.setDrawingMode(null);
    window._drawingManager.setMap(null);
    window._drawingManager = null;
  }

  if(modo === 'area'){
    if(dica) dica.textContent = '✏️ Desenhe um polígono no mapa para selecionar clientes';
    var m = initMap('rot-map');
    if(!m){ toast('Carregue o mapa primeiro!','warn'); return; }

    if(typeof google.maps.drawing === 'undefined'){
      toast('DrawingManager não disponível nesta versão da API','warn');
      // Fallback: modo retângulo manual
      _iniciarSelecaoRetangulo(m);
      return;
    }

    var dm = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.POLYGON,
      drawingControl: false,
      polygonOptions: {
        fillColor:'#10b981', fillOpacity:0.2,
        strokeColor:'#10b981', strokeWeight:2, clickable:false
      }
    });
    dm.setMap(m);
    window._drawingManager = dm;

    google.maps.event.addListener(dm, 'polygoncomplete', function(polygon){
      dm.setDrawingMode(null);
      var path = polygon.getPath();
      var selecionados = 0;
      var cache = window._rotOrdersCache || [];
      cache.forEach(function(o){
        if(!o.lat || !o.lng) return;
        var pt = new google.maps.LatLng(parseFloat(o.lat), parseFloat(o.lng));
        if(google.maps.geometry.poly.containsLocation(pt, polygon)){
          if(!window.rotSelecionados[o.id]){
            window.rotSelecionados[o.id] = {order:o, marker:null};
            selecionados++;
          }
        }
      });
      polygon.setMap(null);
      renderRotMapMarkers(cache);
      atualizarSelecaoRot();
      toast(selecionados+' clientes selecionados na área!','success');
      setModoSelecao('click');
    });
  } else {
    if(dica) dica.textContent = '📌 Clique nos pins para selecionar individualmente';
  }
}

function _iniciarSelecaoRetangulo(m){
  // Fallback: clique-e-arraste cria um retângulo
  toast('Clique e arraste no mapa para selecionar área','info');
  var startLatLng = null;
  var rect = null;
  var dica = document.getElementById('dica-modo');
  if(dica) dica.textContent = '🖱️ Clique e arraste para selecionar área';

  var lDown = google.maps.event.addListener(m, 'mousedown', function(e){
    m.setOptions({draggable:false});
    startLatLng = e.latLng;
  });
  var lMove = google.maps.event.addListener(m, 'mousemove', function(e){
    if(!startLatLng) return;
    if(rect) rect.setMap(null);
    rect = new google.maps.Rectangle({
      bounds: new google.maps.LatLngBounds(
        new google.maps.LatLng(Math.min(startLatLng.lat(),e.latLng.lat()), Math.min(startLatLng.lng(),e.latLng.lng())),
        new google.maps.LatLng(Math.max(startLatLng.lat(),e.latLng.lat()), Math.max(startLatLng.lng(),e.latLng.lng()))
      ),
      fillColor:'#10b981', fillOpacity:0.2, strokeColor:'#10b981', strokeWeight:2, map:m
    });
  });
  var lUp = google.maps.event.addListener(m, 'mouseup', function(e){
    if(!startLatLng) return;
    m.setOptions({draggable:true});
    var bounds = rect ? rect.getBounds() : null;
    var sel=0;
    if(bounds){
      (window._rotOrdersCache||[]).forEach(function(o){
        if(!o.lat||!o.lng) return;
        if(bounds.contains(new google.maps.LatLng(parseFloat(o.lat),parseFloat(o.lng)))){
          if(!window.rotSelecionados[o.id]){ window.rotSelecionados[o.id]={order:o,marker:null}; sel++; }
        }
      });
      if(rect) rect.setMap(null);
    }
    startLatLng = null;
    google.maps.event.removeListener(lDown);
    google.maps.event.removeListener(lMove);
    google.maps.event.removeListener(lUp);
    renderRotMapMarkers(window._rotOrdersCache||[]);
    atualizarSelecaoRot();
    toast(sel+' clientes selecionados!','success');
    setModoSelecao('click');
  });
}

function rotVeiculoChanged(){
  var sel = document.getElementById('rot-veiculo-select');
  if(!sel || !sel.value) return;
  var opt = sel.options[sel.selectedIndex];

  var capKg     = parseFloat(opt.getAttribute('data-kg'))  || 0;
  var capM3     = parseFloat(opt.getAttribute('data-m3'))  || 0;
  var capPallets= parseInt(opt.getAttribute('data-pallets'))|| 0;
  var bauComp   = parseFloat(opt.getAttribute('data-bcomp'))|| 0;
  var bauLarg   = parseFloat(opt.getAttribute('data-blarg'))|| 0;
  var bauAlt    = parseFloat(opt.getAttribute('data-balt')) || 0;

  // Pega peso e volume da seleção atual
  var itens = Object.values(window.rotSelecionados);
  var pesoTotal = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).weight_kg)||0); }, 0);
  var volTotal  = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).volume_m3)||0); }, 0);

  // Pallets estimados (peso / capacidade por pallet)
  var PESO_PALLET = 700;
  var palletsUsados = Math.ceil(pesoTotal / PESO_PALLET);

  // Atualiza barras de capacidade
  var capInfo = document.getElementById('rot-cap-info');
  if(capInfo) capInfo.style.display = 'block';

  var setPct = function(barId, txtId, val, cap, unit){
    var pct = cap > 0 ? Math.min(100, (val/cap*100)) : 0;
    var bar = document.getElementById(barId);
    var txt = document.getElementById(txtId);
    if(bar){ bar.style.width = pct+'%'; bar.style.background = pct>90?'#ef4444':pct>70?'#f59e0b':'#10b981'; }
    if(txt) txt.textContent = val.toFixed(unit==='kg'?0:2)+' '+unit+' / '+cap+' '+unit+' ('+pct.toFixed(0)+'%)';
  };

  setPct('rot-barra-peso', 'rot-peso-txt', pesoTotal, capKg, 'kg');
  setPct('rot-barra-vol',  'rot-vol-txt',  volTotal,  capM3, 'm³');

  // Pallets
  var palPct = capPallets > 0 ? Math.min(100, palletsUsados/capPallets*100) : 0;
  var barPal = document.getElementById('rot-barra-pallets');
  var txtPal = document.getElementById('rot-pallets-txt');
  var capPalTxt = document.getElementById('rot-cap-pallets-txt');
  if(barPal){ barPal.style.width=palPct+'%'; barPal.style.background=palPct>90?'#ef4444':palPct>70?'#f59e0b':'#a78bfa'; }
  if(txtPal) txtPal.textContent = palletsUsados+' / '+capPallets+' pallets ('+palPct.toFixed(0)+'%)';
  if(capPalTxt){
    var bauInfo = bauComp>0 ? bauComp+'×'+bauLarg+'×'+bauAlt+' cm' : '—';
    capPalTxt.textContent = capPallets+' pallets | Baú: '+bauInfo;
  }

  // Atualiza sug-pallets no card carga
  var sugPal = document.getElementById('sug-pallets');
  if(sugPal) sugPal.textContent = palletsUsados+(capPallets>0?' / '+capPallets:'');
}

async function carregarFrota(){
  try{
    var veics=await api('GET','/vehicles');
    var sel=document.getElementById('rot-veiculo-select');
    if(!sel) return;
    sel.innerHTML='<option value="">-- Selecione o veiculo --</option>'+
      veics.filter(function(v){return v.status==='active';}).map(function(v){
        return '<option value="'+v.id+'" data-kg="'+(v.capacity_kg||0)+'" data-m3="'+(v.capacity_m3||0)+'" data-pallets="'+(v.pallets||0)+'" data-bcomp="'+(v.bau_comp||0)+'" data-blarg="'+(v.bau_larg||0)+'" data-balt="'+(v.bau_alt||0)+'">'+v.vda+' — '+v.plate+'</option>';
      }).join('');
  }catch(e){}
}

async function carregarVeiculosSelect(){
  try{
    var drivers=await api('GET','/drivers');
    var mots=drivers.filter(function(d){return d.tipo==='motorista';});
    var ajs=drivers.filter(function(d){return d.tipo==='ajudante';});
    var fillSel=function(id,arr,ph){
      var sel=document.getElementById(id);
      if(!sel) return;
      sel.innerHTML='<option value="">'+ph+'</option>'+arr.map(function(d){return '<option value="'+d.id+'">'+d.name+'</option>';}).join('');
    };
    fillSel('sel-motorista',mots,'-- Selecione --');
    fillSel('sel-ajudante1',ajs,'-- Nenhum --');
    fillSel('sel-ajudante2',ajs,'-- Nenhum --');
  }catch(e){}
}

function fecharConferencia(){document.getElementById('painel-conferencia').style.display='none';}
function renderizarListaConf(){}
function inverterOrdemConf(){}
function reprocessarSequencia(){}
function atualizarRotaMapa(){toast('Rota atualizada!','success');}
function confirmarRota(){rotaConfirmada=true;toast('Rota confirmada!','success');}

async function gravarCarga(){
  if(!confOrdem||!confOrdem.length){toast('Nenhum cliente na carga!','error');return;}
  var veicSel=document.getElementById('rot-veiculo-select')?document.getElementById('rot-veiculo-select').value:'';
  var motSel=document.getElementById('sel-motorista')?document.getElementById('sel-motorista').value:'';
  if(!veicSel||!motSel){toast('Selecione veiculo e motorista!','error');return;}
  try{
    var dataSaida=document.getElementById('conf-data-saida')?document.getElementById('conf-data-saida').value:new Date().toISOString().slice(0,10);
    var horaInicio=document.getElementById('conf-hora-inicio')?document.getElementById('conf-hora-inicio').value:'07:30';
    await api('POST','/routes',{vehicle_id:veicSel,driver_id:motSel,date:dataSaida,planned_start:horaInicio,order_ids:confOrdem.map(function(o){return o.id;})});
    toast('Carga gravada com sucesso!','success');
    fecharConferencia();
    loadRoutes();
  }catch(e){toast('Erro ao gravar: '+e.message,'error');}
}

async function desenharRotaReal(map,stops,color){
  if(!stops||stops.length<1) return;
  stops.forEach(function(s){if(s.lat&&s.lng) addMarker(map,parseFloat(s.lat),parseFloat(s.lng),color||'#64B4FF',s.recipient_name||'','');});
}

// ── INTEGRAÇÃO ───────────────────────────────────────────────────
function testConn(){toast('Teste de conexao em desenvolvimento','info');}
async function runSync(){toast('Sincronizacao em desenvolvimento','info');}
function checkSyncStatus(){}

// ── DASHBOARD MODAIS ─────────────────────────────────────────────
function abrirModalDash(tipo,titulo){
  var el=document.getElementById('modal-dash');
  var tit=document.getElementById('modal-dash-title');
  var body=document.getElementById('modal-dash-body');
  if(!el) return;
  if(tit) tit.textContent=titulo||'Detalhe';
  if(body) body.innerHTML='<div class="loading-state">Em desenvolvimento</div>';
  el.style.display='flex';
}

// ── MISC ─────────────────────────────────────────────────────────
function saveOrder(){
  api('POST','/orders',{
    external_id:document.getElementById('o-ext').value,
    recipient_name:document.getElementById('o-name').value,
    address:document.getElementById('o-addr').value,
    lat:parseFloat(document.getElementById('o-lat').value)||null,
    lng:parseFloat(document.getElementById('o-lng').value)||null,
    weight_kg:parseFloat(document.getElementById('o-kg').value)||0,
    volume_m3:parseFloat(document.getElementById('o-m3').value)||0,
    time_window_start:document.getElementById('o-tws').value,
    time_window_end:document.getElementById('o-twe').value,
    notes:document.getElementById('o-notes').value,
    status:'pending',priority:1,
  }).then(function(){toast('Pedido salvo!','success');closeModal('order');loadOrders();})
  .catch(function(e){toast('Erro: '+e.message,'error');});
}

function limparAssinatura(){
  var canvas=document.getElementById('oc-assinatura');
  if(canvas) canvas.getContext('2d').clearRect(0,0,canvas.width,canvas.height);
}

// Inicialização
document.addEventListener('DOMContentLoaded', function(){
  var today=new Date().toISOString().slice(0,10);
  ['routes-date','mon-date'].forEach(function(id){var e=document.getElementById(id);if(e)e.value=today;});
  carregarBaseClientes();
});

// ── IMPORTAÇÃO TGFITE ─────────────────────────────────────────────
var _tgfiteTipo = null;
var _tgfiteNome = null;
var _tgfitePeso = null;
var _tgfiteDados = [];

function abrirModalItens(){
  var m = document.getElementById('modal-importacao-itens');
  if(m){ m.style.display='flex'; carregarStatusItens(); }
}
function fecharModalItens(){
  var m = document.getElementById('modal-importacao-itens');
  if(m) m.style.display='none';
}

function selecionarTipoGelo(tipo, nome, pesoUnit){
  _tgfiteTipo = tipo; _tgfiteNome = nome; _tgfitePeso = pesoUnit;
  ['gelo5','gelo10','gelo20','gelo40'].forEach(function(t){
    var b = document.getElementById('btn-'+t);
    if(b){ b.style.borderColor = t===tipo ? '#10b981' : '#1e3a5c'; b.style.color = t===tipo ? '#10b981' : '#90afd4'; b.style.background = t===tipo ? 'rgba(16,185,129,.15)' : '#0a1628'; }
  });
  verificarBtnImportarItens();
}

function verificarBtnImportarItens(){
  var btn = document.getElementById('btn-importar-itens');
  var ok = _tgfiteTipo && _tgfiteDados.length > 0;
  if(btn){ btn.disabled = !ok; btn.style.opacity = ok ? '1' : '0.5'; }
}

function lerArquivoTGFITE(input){
  var file = input.files[0];
  if(!file) return;
  document.getElementById('tgfite-nome-arquivo').textContent = file.name;
  var ext = file.name.split('.').pop().toLowerCase();
  var reader = new FileReader();
  if(ext === 'csv' || ext === 'txt'){
    reader.onload = function(e){ processarTGFITE(e.target.result.split('\n').map(function(r){return r.split(';');})); };
    reader.readAsText(file, 'latin1');
  } else {
    reader.onload = function(e){
      var wb = XLSX.read(e.target.result, {type:'binary'});
      var ws = wb.Sheets[wb.SheetNames[0]];
      processarTGFITE(XLSX.utils.sheet_to_json(ws, {header:1, defval:''}));
    };
    reader.readAsBinaryString(file);
  }
}

function processarTGFITE(rows){
  // Mapeamento TOP Sankhya → App
  var topMap = {'1100':'1000','1126':'1009','1117':'1007','1118':'1008','1127':'1010'};

  // Encontra cabeçalho
  var headerIdx = 0;
  var header = [];
  for(var r=0; r<Math.min(10,rows.length); r++){
    var norm = rows[r].map(function(h){ return String(h||'').toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim(); });
    if(norm.some(function(h){ return h.indexOf('PARCEIRO')>=0 || h.indexOf('QTD')>=0; })){
      headerIdx = r; header = norm; break;
    }
  }

  // Mapeamento de colunas
  var idx = {};
  var mapa = {
    codparc: ['PARCEIRO','CODPARC','COD PARC'],
    qtd:     ['QTD NEG','QTDNEG','QTD. NEG.','QTD'],
    top:     ['TOP','CODTIPOPER','DESCRICAO DA TOP'],
    data:    ['DT. NEG.','DT NEG','DATA'],
    nome:    ['NOME DO PARCEIRO','NOMEPARC','NOME PARCEIRO'],
  };
  Object.keys(mapa).forEach(function(campo){
    mapa[campo].forEach(function(alias){
      if(idx[campo]!==undefined) return;
      header.forEach(function(h,i){ if(h.indexOf(alias)>=0 && idx[campo]===undefined) idx[campo]=i; });
    });
  });

  var get = function(row, campo){ return idx[campo]!==undefined ? String(row[idx[campo]]||'').trim() : ''; };

  _tgfiteDados = [];
  var erros = 0;
  for(var i=headerIdx+1; i<rows.length; i++){
    var row = rows[i];
    if(!row || row.every(function(c){return !c;})) continue;
    var codparc = parseInt(get(row,'codparc'));
    var qtd = parseInt(get(row,'qtd')) || 0;
    if(!codparc || qtd===0){ erros++; continue; }
    var topRaw = get(row,'top');
    var topApp = topMap[topRaw] || topRaw || '1000';
    _tgfiteDados.push({
      codparc: codparc,
      top_app: topApp,
      item_tipo: _tgfiteTipo || 'gelo5',
      item_nome: _tgfiteNome || 'Gelo',
      peso_unit: _tgfitePeso || 6,
      qtd: qtd,
      dt_neg: get(row,'data') || new Date().toISOString().slice(0,10)
    });
  }

  // Preview
  var prev = document.getElementById('tgfite-preview');
  if(prev) prev.style.display = 'block';
  document.getElementById('tgfite-total').textContent = _tgfiteDados.length + erros;
  document.getElementById('tgfite-validos').textContent = _tgfiteDados.length;
  document.getElementById('tgfite-erros').textContent = erros;

  var tbl = document.getElementById('tgfite-preview-table');
  if(tbl && _tgfiteDados.length>0){
    var header_row = '<tr style="background:#1e3a5c"><th style="padding:4px 8px;color:#64B4FF">CODPARC</th><th style="padding:4px 8px;color:#64B4FF">QTD</th><th style="padding:4px 8px;color:#64B4FF">TOP</th><th style="padding:4px 8px;color:#64B4FF">DATA</th></tr>';
    var rows_html = _tgfiteDados.slice(0,10).map(function(d){
      return '<tr style="border-bottom:1px solid #1e3a5c"><td style="padding:4px 8px;color:#e8f0fe">'+d.codparc+'</td><td style="padding:4px 8px;color:#10b981">'+d.qtd+'</td><td style="padding:4px 8px;color:#f59e0b">'+d.top_app+'</td><td style="padding:4px 8px;color:#90afd4">'+d.dt_neg+'</td></tr>';
    }).join('');
    tbl.innerHTML = header_row + rows_html;
  }
  verificarBtnImportarItens();
}

async function importarItensTGFITE(){
  if(!_tgfiteTipo || !_tgfiteDados.length){ toast('Selecione o tipo e o arquivo!','warn'); return; }
  var btn = document.getElementById('btn-importar-itens');
  if(btn){ btn.disabled=true; btn.textContent='Importando...'; }
  try{
    var res = await api('POST', '/order_items/bulk', {items: _tgfiteDados});
    toast(res.inserted+' itens de '+_tgfiteNome+' importados!','success');
    // Atualiza status
    var statusEl = document.getElementById('status-'+_tgfiteTipo);
    var countEl  = document.getElementById('count-'+_tgfiteTipo);
    if(statusEl) statusEl.textContent = '✅';
    if(countEl)  countEl.textContent  = res.inserted+' clientes';
    // Reset
    _tgfiteDados = [];
    document.getElementById('tgfite-file-input').value='';
    document.getElementById('tgfite-nome-arquivo').textContent='Nenhum arquivo selecionado';
    document.getElementById('tgfite-preview').style.display='none';
    if(btn){ btn.disabled=true; btn.textContent='📦 Importar Itens'; btn.style.opacity='0.5'; }
  }catch(e){
    toast('Erro: '+e.message,'error');
    if(btn){ btn.disabled=false; btn.textContent='📦 Importar Itens'; }
  }
}

async function carregarStatusItens(){
  try{
    var itens = await api('GET','/order_items');
    var tipos = {gelo5:0, gelo10:0, gelo20:0, gelo40:0};
    itens.forEach(function(it){ if(tipos[it.item_tipo]!==undefined) tipos[it.item_tipo]++; });
    Object.keys(tipos).forEach(function(t){
      var s = document.getElementById('status-'+t);
      var c = document.getElementById('count-'+t);
      if(s) s.textContent = tipos[t]>0 ? '✅' : '⬜';
      if(c) c.textContent = tipos[t]>0 ? tipos[t]+' clientes' : '';
    });
  }catch(e){}
}
