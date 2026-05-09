path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total atual: {len(lines)}')

# Encontra onde o HTML do modal de CSV termina (último </div> antes dos scripts extras)
# Procura pela linha que tem o modal-importacao-csv fechando
corte = None
for i in range(len(lines)-1, 3400, -1):
    if '  </div>' in lines[i] and i < 3460:
        # Verifica se é o fechamento do modal CSV
        corte = i + 1
        break

# Procura mais especificamente
for i in range(3440, 3470):
    if i < len(lines):
        print(f'{i+1}: {repr(lines[i][:80])}')

# O corte deve ser após a linha que fecha o modal (linha ~3455 com </div>)
# Vamos cortar na linha 3456 e adicionar fechamento limpo
corte = 3455  # após o último </div> do modal CSV

print(f'\nCortando na linha {corte+1}')
print(f'Última linha mantida: {repr(lines[corte-1][:80])}')

# Mantém até a linha do corte
linhas_boas = lines[:corte]

# Adiciona fim limpo
fim_limpo = '''
  <!-- MODAL BASE DE CLIENTES -->
  <div id="modal-base-clientes" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:3000;align-items:center;justify-content:center;padding:20px">
    <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:560px">
      <div style="padding:16px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:15px;font-weight:700;color:#e8f0fe">&#x1F91D; Importar Parceiros</div>
          <div style="font-size:11px;color:#90afd4">CODIGO_ERP, LATITUDE, LONGITUDE e demais campos</div>
        </div>
        <button onclick="document.getElementById('modal-base-clientes').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">&#x2715;</button>
      </div>
      <div style="padding:20px 24px">
        <div onclick="document.getElementById('base-clientes-input').click()" style="border:2px dashed #1e3a5c;border-radius:10px;padding:28px;text-align:center;cursor:pointer;margin-bottom:16px">
          <div style="font-size:32px;margin-bottom:8px">&#x1F4C4;</div>
          <div style="font-size:14px;color:#e8f0fe;font-weight:600">Clique para selecionar XLS/XLSX</div>
          <div style="font-size:11px;color:#90afd4;margin-top:4px" id="base-clientes-nome">Nenhum arquivo</div>
          <div style="font-size:12px;color:#64B4FF;margin-top:6px" id="base-clientes-count"></div>
        </div>
        <input type="file" id="base-clientes-input" accept=".xls,.xlsx,.csv" style="display:none" onchange="lerBaseClientesXLS(this)">
        <div style="display:flex;gap:10px;justify-content:flex-end">
          <button onclick="document.getElementById('modal-base-clientes').style.display='none'" class="btn btn-secondary">Cancelar</button>
          <button id="btn-importar-base" onclick="importarBaseClientes()" disabled class="btn btn-primary" style="opacity:.5;cursor:not-allowed">&#x1F4E5; Importar</button>
        </div>
      </div>
    </div>
  </div>

<script>
var _clientesCache = {};
var _todosClientes = [];

function uploadParceiros() { abrirImportacaoBaseClientes(); }

function abrirImportacaoBaseClientes() {
  var modal = document.getElementById('modal-base-clientes');
  if (!modal) { toast('Modal nao encontrado', 'error'); return; }
  var n = document.getElementById('base-clientes-nome');
  var c = document.getElementById('base-clientes-count');
  var b = document.getElementById('btn-importar-base');
  var inp = document.getElementById('base-clientes-input');
  if (n) n.textContent = 'Nenhum arquivo';
  if (c) c.textContent = '';
  if (b) { b.disabled=true; b.style.opacity='.5'; b.textContent='Importar'; }
  if (inp) inp.value = '';
  window._clientesParaImportar = [];
  modal.style.display = 'flex';
}

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

function lerBaseClientesXLS(input) {
  var file = input.files[0];
  if (!file) return;
  var nomeEl = document.getElementById('base-clientes-nome');
  if (nomeEl) nomeEl.textContent = file.name;
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var wb = XLSX.read(e.target.result, {type:'binary'});
      var ws = wb.Sheets[wb.SheetNames[0]];
      var rows = XLSX.utils.sheet_to_json(ws, {header:1, defval:''});
      var headerIdx = 0;
      for (var r = 0; r < Math.min(5, rows.length); r++) {
        var norm = rows[r].map(function(h){return String(h||'').toUpperCase();});
        if (norm.some(function(h){return h.indexOf('CODIGO')>=0||h.indexOf('COD')>=0;})) { headerIdx=r; break; }
      }
      var header = rows[headerIdx].map(function(h){
        return String(h||'').trim().toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9_\\/]/g,'').trim();
      });
      var m = {
        codparc:['CODIGO_ERP','CODPARC','CODIGO'],
        nome:['NOME_FANTASIA','NOMEFANTASIA','NOME'],
        razao_social:['RAZAO_SOCIAL','RAZAOSOCIAL'],
        endereco:['ENDERECO'],
        cep:['CEP'],
        bairro:['BAIRRO'],
        cidade:['CIDADEUF','CIDADE'],
        lat:['LATITUDE','LAT'],
        lng:['LONGITUDE','LNG'],
        cpf_cnpj:['CPFCNPJ','CPF/CNPJ'],
        segmento:['SEGMENTO'],
        zona_geo:['ZONA_GEO','ZONAGEO'],
        comodatos:['COMODATOS'],
        tempo_entrega:['TEMPOMEDIO'],
        rota:['ROTA'],
      };
      var idx = {};
      Object.keys(m).forEach(function(campo){
        idx[campo] = -1;
        m[campo].forEach(function(o){ if(idx[campo]===-1 && header.indexOf(o)!==-1) idx[campo]=header.indexOf(o); });
      });
      var parceiros = []; var semGps = 0;
      for (var i = headerIdx+1; i < rows.length; i++) {
        var cols = rows[i].map(function(c){return String(c||'').trim();});
        if (cols.join('').length===0) continue;
        var get = function(c){return idx[c]!==-1?cols[idx[c]]||'':'';};
        var codparc = parseInt(get('codparc'));
        if (!codparc || isNaN(codparc)) continue;
        var parseCoord = function(v){if(!v)return null; return parseFloat(String(v).replace(',','.').replace(/[^\d.\-]/g,''))||null;};
        var lat = parseCoord(get('lat')), lng = parseCoord(get('lng'));
        if (!lat||!lng) semGps++;
        var end = get('endereco'), bairro = get('bairro');
        var cidade = get('cidade').replace('/AM','').replace('- AM','').trim()||'Manaus';
        var endFull = [end,bairro,cidade+' - AM'].filter(Boolean).join(', ');
        parceiros.push({codparc:codparc,nome:get('nome')||get('razao_social'),razao_social:get('razao_social'),
          endereco:endFull,cep:get('cep'),bairro:bairro,cidade:get('cidade'),lat:lat,lng:lng,
          cpf_cnpj:get('cpf_cnpj'),segmento:get('segmento'),zona_geo:get('zona_geo'),regiao:get('zona_geo')||get('rota'),
          comodatos:get('comodatos'),tempo_entrega:get('tempo_entrega'),rota:get('rota'),telefone:'',ativo:'S'});
      }
      var countEl = document.getElementById('base-clientes-count');
      if (countEl) countEl.textContent = parceiros.length+' parceiros ('+semGps+' sem GPS)';
      var btn = document.getElementById('btn-importar-base');
      if (btn && parceiros.length>0){btn.disabled=false;btn.style.opacity='1';btn.style.cursor='pointer';}
      window._clientesParaImportar = parceiros;
      toast(parceiros.length+' parceiros prontos!','success');
    } catch(err) { toast('Erro: '+err.message,'error'); }
  };
  reader.readAsBinaryString(file);
}

async function importarBaseClientes() {
  var parceiros = window._clientesParaImportar||[];
  if (!parceiros.length){toast('Nenhum dado!','error');return;}
  var btn = document.getElementById('btn-importar-base');
  if(btn){btn.disabled=true;btn.textContent='Importando...';}
  try {
    var total=0;
    for(var i=0;i<parceiros.length;i+=500){
      var res = await api('POST','/clientes/bulk',parceiros.slice(i,i+500));
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

async function loadClientes() {
  try {
    var lista = await api('GET', '/clientes');
    _todosClientes = lista;
    var comGps=lista.filter(function(c){return c.lat&&c.lng;}).length;
    var ativos=lista.filter(function(c){return c.ativo==='S';}).length;
    var regsSet={};
    lista.forEach(function(c){if(c.regiao) regsSet[c.regiao]=1;});
    var regioes=Object.keys(regsSet).length;
    var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
    el('cli-total',lista.length); el('cli-gps',comGps); el('cli-ativos',ativos); el('cli-regioes',regioes);
    el('clientes-sub',lista.length+' parceiros cadastrados');
    var sel=document.getElementById('cli-regiao');
    if(sel){
      var regs=Object.keys(regsSet).sort();
      var opts='<option value="">Todas as regioes</option>';
      regs.forEach(function(r){opts+='<option value="'+r+'">'+r+'</option>';});
      sel.innerHTML=opts;
    }
    renderClientes(lista);
  } catch(e){toast('Erro: '+e.message,'error');}
}

function filtrarClientes() {
  var busca=(document.getElementById('cli-busca')||{value:''}).value.toLowerCase();
  var regiao=(document.getElementById('cli-regiao')||{value:''}).value;
  var gps=(document.getElementById('cli-gps-filtro')||{value:''}).value;
  var f=_todosClientes.filter(function(c){
    var mb=!busca||(c.nome||'').toLowerCase().indexOf(busca)>=0||(c.endereco||'').toLowerCase().indexOf(busca)>=0||String(c.codparc||'').indexOf(busca)>=0;
    var mr=!regiao||c.regiao===regiao;
    var mg=!gps||(gps==='sim'?(c.lat&&c.lng):!(c.lat&&c.lng));
    return mb&&mr&&mg;
  });
  renderClientes(f);
}

function limparFiltrosClientes(){
  ['cli-busca','cli-regiao','cli-gps-filtro'].forEach(function(id){var e=document.getElementById(id);if(e)e.value='';});
  renderClientes(_todosClientes);
}

function renderClientes(lista) {
  var tbody=document.getElementById('clientes-tbody');
  var rodape=document.getElementById('clientes-rodape');
  if(!tbody) return;
  if(!lista.length){tbody.innerHTML='<tr><td colspan="9" class="loading-state">Nenhum parceiro</td></tr>';return;}
  var rows='';
  lista.forEach(function(c){
    var gps=(c.lat&&c.lng)?'<span style="color:#10b981">GPS</span>':'<span style="color:#f87171">Sem GPS</span>';
    var at=c.ativo==='S'?'active':'inactive';
    var cidade=(c.cidade||'').replace(' - AM','');
    rows+='<tr>'+
      '<td style="font-family:monospace;color:#64B4FF">'+(c.codparc||'—')+'</td>'+
      '<td><b>'+(c.nome||'—')+'</b></td>'+
      '<td style="font-size:11px;color:#90afd4">'+(c.endereco||'—')+'</td>'+
      '<td style="font-size:11px">'+(c.bairro||'—')+'</td>'+
      '<td style="font-size:11px">'+cidade+'</td>'+
      '<td><span class="badge active" style="font-size:9px">'+(c.regiao||'—')+'</span></td>'+
      '<td>'+gps+'</td>'+
      '<td style="font-size:11px">'+(c.telefone||'—')+'</td>'+
      '<td><span class="badge '+at+'">'+(c.ativo==='S'?'Ativo':'Inativo')+'</span></td>'+
      '</tr>';
  });
  tbody.innerHTML=rows;
  if(rodape) rodape.textContent=lista.length+' parceiros';
}

document.addEventListener('DOMContentLoaded', function(){ carregarBaseClientes(); });
</script>

</body>
</html>
'''

for line in fim_limpo.split('\n'):
    linhas_boas.append(line + '\n')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(linhas_boas)

print(f'Total final: {len(linhas_boas)} linhas')
print('Pronto! Ctrl+Shift+R.')
