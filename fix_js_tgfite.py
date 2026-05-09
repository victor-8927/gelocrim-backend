path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica o botão de importar CSV na toolbar
idx = content.find("'modal-importacao-csv'")
while idx != -1:
    ln = content[:idx].count('\n')+1
    ctx = content[max(0,idx-100):idx+60]
    if 'btn' in ctx or 'button' in ctx:
        print(f'linha {ln}: {repr(ctx)}')
    idx = content.find("'modal-importacao-csv'", idx+1)

# Adiciona JS das funções TGFITE antes do </script> do script 4
js_tgfite = """
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
    reader.onload = function(e){ processarTGFITE(e.target.result.split('\\n').map(function(r){return r.split(';');})); };
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
    var norm = rows[r].map(function(h){ return String(h||'').toUpperCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').trim(); });
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
"""

# Insere antes do </script> final do script 4
last_script_close = content.rfind('</script>')
content = content[:last_script_close] + js_tgfite + '\n' + content[last_script_close:]
print('JS TGFITE adicionado!')

# Adiciona botão Importar Itens na toolbar de pedidos
# Busca padrão exato
import re
m = re.search(r"<button[^>]+onclick=\"document\.getElementById\('modal-importacao-csv'\)\.style\.display='flex'\"[^>]*>📥 Importar CSV</button>", content)
if m:
    old = m.group(0)
    new = old + "\n      <button class=\"btn\" onclick=\"abrirModalItens()\" style=\"background:rgba(16,185,129,.15);border:1px solid #10b981;color:#10b981;padding:8px 16px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer\">📦 Importar Itens</button>"
    content = content.replace(old, new, 1)
    print('Botão Importar Itens adicionado!')
else:
    print('Botão CSV não encontrado pelo regex!')
    idx = content.find("modal-importacao-csv")
    while idx != -1:
        ln = content[:idx].count('\n')+1
        ctx = content[max(0,idx-60):idx+80]
        if 'button' in ctx.lower():
            print(f'  linha {ln}: {repr(ctx)}')
        idx = content.find("modal-importacao-csv", idx+1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R e reinicie o servidor.')
