path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pesos unitários por código de item
# 370=GELO 05KG, 371=GELO 10KG, 372=GELO 20KG, 373=GELO 40KG
# Pesos reais com embalagem: 5kg→6kg, 10kg→11kg, 20kg→23kg, 40kg→45kg

# 1. Adiciona botão na toolbar de Pedidos
old_btn = '''<button class="btn btn-primary btn-sm" onclick="abrirModalItens()">📦 Importar Itens</button>'''
new_btn = '''<button class="btn btn-primary btn-sm" onclick="abrirModalItens()">📦 Importar Itens</button>
              <button class="btn btn-sm" style="background:rgba(100,180,255,.15);border:1px solid #64B4FF;color:#64B4FF" onclick="abrirModalPlanilha()">📋 Importar Planilha TI</button>'''

if old_btn in content:
    content = content.replace(old_btn, new_btn)
    print('Botão importar planilha adicionado!')
else:
    print('Botão não encontrado!')

# 2. Adiciona modal de importação
modal_html = '''
<!-- MODAL IMPORTAÇÃO PLANILHA TI -->
<div id="modal-planilha-ti" onclick="if(event.target===this)this.style.display='none'" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;align-items:center;justify-content:center;padding:20px">
  <div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:620px;max-height:90vh;overflow-y:auto">
    <div style="padding:20px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center">
      <div>
        <div style="font-size:16px;font-weight:700;color:#e8f0fe">📋 Importar Planilha TI</div>
        <div style="font-size:11px;color:#90afd4;margin-top:2px">Pedidos + Itens em um único arquivo</div>
      </div>
      <button onclick="document.getElementById('modal-planilha-ti').style.display='none'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>
    </div>
    <div style="padding:20px">
      <!-- Colunas esperadas -->
      <div style="background:#0a1628;border-radius:8px;padding:12px;margin-bottom:16px;font-size:11px;color:#90afd4">
        <b style="color:#64B4FF">Colunas esperadas:</b> NUMERO ÚNICO · NUMERO DOCUMENTO · CODPAR-NOME PARCEIROS · DATA · ITEM · Q NEGOCIADA · ORDEM DE CARGA
        <div style="margin-top:6px;color:#f59e0b">⚡ Apenas linhas com ORDEM DE CARGA = 0 serão importadas</div>
      </div>
      <!-- Upload -->
      <div id="planilha-drop" onclick="document.getElementById('planilha-file').click()"
        style="border:2px dashed #1e3a5c;border-radius:12px;padding:32px;text-align:center;cursor:pointer;margin-bottom:16px;transition:border-color .2s"
        onmouseover="this.style.borderColor='#64B4FF'" onmouseout="this.style.borderColor='#1e3a5c'">
        <div style="font-size:32px;margin-bottom:8px">📊</div>
        <div style="color:#e8f0fe;font-weight:600">Clique para selecionar o arquivo .xlsx</div>
        <div style="font-size:11px;color:#90afd4;margin-top:4px" id="planilha-nome">Nenhum arquivo selecionado</div>
      </div>
      <input type="file" id="planilha-file" accept=".xlsx,.xls" style="display:none" onchange="planilhaFileChanged(this)">
      <!-- Preview -->
      <div id="planilha-preview" style="display:none;margin-bottom:16px">
        <div style="font-size:12px;font-weight:700;color:#64B4FF;margin-bottom:8px">PREVIEW</div>
        <div id="planilha-preview-body" style="background:#0a1628;border-radius:8px;padding:12px;font-size:11px;color:#90afd4;max-height:200px;overflow-y:auto"></div>
      </div>
      <!-- Botão -->
      <button id="btn-importar-planilha" onclick="importarPlanilhaTI()" disabled
        style="width:100%;padding:14px;background:#1e3a5c;color:#90afd4;border:none;border-radius:10px;font-weight:700;font-size:14px;cursor:not-allowed">
        📥 Importar Pedidos
      </button>
      <div id="planilha-resultado" style="margin-top:12px;font-size:12px;text-align:center"></div>
    </div>
  </div>
</div>
'''

# Insere antes do </body>
if 'modal-planilha-ti' not in content:
    content = content.replace('</body>', modal_html + '\n</body>')
    print('Modal adicionado!')

# 3. Adiciona funções JS
js_func = r"""
// ── IMPORTADOR PLANILHA TI ────────────────────────────────────────
var _planilhaDados = [];

var PESOS_ITEM = {
  '370': 6,   // GELO 05KG (com embalagem)
  '371': 11,  // GELO 10KG
  '372': 23,  // GELO 20KG
  '373': 45   // GELO 40KG
};

var NOMES_ITEM = {
  '370': 'GELO 05KG',
  '371': 'GELO 10KG',
  '372': 'GELO 20KG',
  '373': 'GELO 40KG'
};

function abrirModalPlanilha() {
  document.getElementById('modal-planilha-ti').style.display = 'flex';
  _planilhaDados = [];
  document.getElementById('planilha-nome').textContent = 'Nenhum arquivo selecionado';
  document.getElementById('planilha-preview').style.display = 'none';
  document.getElementById('planilha-resultado').textContent = '';
  var btn = document.getElementById('btn-importar-planilha');
  btn.disabled = true;
  btn.style.background = '#1e3a5c';
  btn.style.color = '#90afd4';
  btn.style.cursor = 'not-allowed';
}

function planilhaFileChanged(input) {
  var file = input.files[0];
  if (!file) return;
  document.getElementById('planilha-nome').textContent = file.name;

  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var wb = XLSX.read(e.target.result, { type: 'array' });
      var ws = wb.Sheets[wb.SheetNames[0]];
      var rows = XLSX.utils.sheet_to_json(ws, { defval: '' });

      // Filtra ORDEM DE CARGA = 0
      var filtradas = rows.filter(function(r) {
        var oc = r['ORDEM DE CARGA'] || r['ORDEMCARGA'] || 0;
        return parseInt(oc) === 0;
      });

      // Agrupa por NUMERO ÚNICO
      var pedidos = {};
      filtradas.forEach(function(r) {
        var numUnico = String(r['NUMERO ÚNICO'] || r['NUMERO UNICO'] || '').trim();
        var numDoc   = String(r['NUMERO DOCUMENTO'] || '').trim();
        var codNome  = String(r['CODPAR-NOME PARCEIROS'] || '').trim();
        var data     = String(r['DATA'] || '').trim();
        var itemStr  = String(r['ITEM'] || '').trim();
        var qtd      = parseInt(r['Q NEGOCIADA'] || 0);

        if (!numUnico || !codNome) return;

        // Extrai codparc e nome
        var partes = codNome.split(' - ');
        var codparc = parseInt(partes[0]) || 0;
        var nome = partes.slice(1).join(' - ').trim();

        // Extrai código do item
        var codItem = itemStr.split(' - ')[0].trim();
        var pesoUnit = PESOS_ITEM[codItem] || 0;
        var nomeItem = NOMES_ITEM[codItem] || itemStr;

        if (!pedidos[numUnico]) {
          pedidos[numUnico] = {
            external_id: numUnico,
            num_doc: numDoc,
            codparc: codparc,
            recipient_name: nome,
            data: data,
            itens: [],
            weight_kg: 0
          };
        }
        pedidos[numUnico].itens.push({ cod: codItem, nome: nomeItem, qtd: qtd, peso_unit: pesoUnit });
        pedidos[numUnico].weight_kg += qtd * pesoUnit;
      });

      _planilhaDados = Object.values(pedidos);

      // Preview
      var prev = document.getElementById('planilha-preview-body');
      var totalItens = _planilhaDados.reduce(function(s,p){return s+p.itens.length;},0);
      var totalKg = _planilhaDados.reduce(function(s,p){return s+p.weight_kg;},0);

      prev.innerHTML =
        '<div style="color:#10b981;font-weight:700;margin-bottom:8px">' +
        '✅ ' + _planilhaDados.length + ' pedidos · ' + totalItens + ' linhas de item · ' + totalKg.toFixed(0) + ' kg total</div>' +
        _planilhaDados.slice(0,5).map(function(p) {
          return '<div style="padding:4px 0;border-bottom:1px solid #1e3a5c">' +
            '<b style="color:#e8f0fe">' + p.recipient_name + '</b> (cod:'+p.codparc+') — ' +
            p.itens.map(function(i){return i.qtd+'x '+i.nome;}).join(', ') +
            ' = <b style="color:#64B4FF">' + p.weight_kg.toFixed(0) + 'kg</b></div>';
        }).join('') +
        (_planilhaDados.length > 5 ? '<div style="color:#90afd4;margin-top:4px">... e mais ' + (_planilhaDados.length-5) + ' pedidos</div>' : '');

      document.getElementById('planilha-preview').style.display = 'block';
      var btn = document.getElementById('btn-importar-planilha');
      btn.disabled = false;
      btn.style.background = '#64B4FF';
      btn.style.color = '#002855';
      btn.style.cursor = 'pointer';
    } catch(e) {
      toast('Erro ao ler planilha: ' + e.message, 'error');
    }
  };
  reader.readAsArrayBuffer(file);
}

async function importarPlanilhaTI() {
  if (!_planilhaDados.length) return;
  var btn = document.getElementById('btn-importar-planilha');
  btn.disabled = true;
  btn.textContent = '⏳ Importando...';
  var res_el = document.getElementById('planilha-resultado');

  try {
    var payload = _planilhaDados.map(function(p) {
      return {
        external_id: p.external_id,
        num_doc: p.num_doc,
        codparc: p.codparc,
        recipient_name: p.recipient_name,
        weight_kg: p.weight_kg,
        itens: p.itens,
        data: p.data
      };
    });

    var res = await api('POST', '/orders/bulk_planilha', { pedidos: payload });
    res_el.innerHTML = '<span style="color:#10b981">✅ ' + res.importados + ' pedidos importados! ' + (res.atualizados||0) + ' atualizados.</span>';
    toast('Planilha importada! ' + res.importados + ' pedidos.', 'success');
    setTimeout(function(){ loadOrders(); }, 1000);
  } catch(e) {
    res_el.innerHTML = '<span style="color:#f87171">❌ Erro: ' + e.message + '</span>';
  } finally {
    btn.disabled = false;
    btn.textContent = '📥 Importar Pedidos';
  }
}
"""

# Insere antes do </script> final
scripts_pos = [m.end() for m in __import__('re').finditer(r'<script>', content)]
last_script_end = content.rfind('</script>')
content = content[:last_script_end] + js_func + '\n' + content[last_script_end:]
print('Funções JS adicionadas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('HTML atualizado!')
