path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove o último bloco <script> que está corrompido
# e substitui por versão limpa
import re

# Encontra o último bloco script
scripts = list(re.finditer(r'<script>\s*(?:let _todosClientes|function loadClientes|function uploadParceiros|function renderClientes).*?</script>', content, re.DOTALL))
print(f'Blocos de clientes encontrados: {len(scripts)}')

# Remove todos
for s in reversed(scripts):
    content = content[:s.start()] + content[s.end():]
    print(f'Removido bloco na pos {s.start()}')

# Adiciona bloco limpo antes do </body>
bloco_limpo = """
<script>
var _todosClientes = [];

function uploadParceiros() { abrirImportacaoBaseClientes(); }

async function loadClientes() {
  try {
    var lista = await api('GET', '/clientes');
    _todosClientes = lista;
    var comGps = lista.filter(function(c){return c.lat && c.lng;}).length;
    var ativos = lista.filter(function(c){return c.ativo==='S';}).length;
    var regsSet = {};
    lista.forEach(function(c){if(c.regiao) regsSet[c.regiao]=1;});
    var regioes = Object.keys(regsSet).length;
    var el = function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
    el('cli-total', lista.length);
    el('cli-gps', comGps);
    el('cli-ativos', ativos);
    el('cli-regioes', regioes);
    el('clientes-sub', lista.length + ' parceiros cadastrados');
    var sel = document.getElementById('cli-regiao');
    if (sel) {
      var regs = Object.keys(regsSet).sort();
      var opts = '<option value="">Todas as regioes</option>';
      regs.forEach(function(r){ opts += '<option value="'+r+'">'+r+'</option>'; });
      sel.innerHTML = opts;
    }
    renderClientes(lista);
  } catch(e) { toast('Erro: '+e.message, 'error'); }
}

function filtrarClientes() {
  var busca = (document.getElementById('cli-busca') ? document.getElementById('cli-busca').value : '').toLowerCase();
  var regiao = document.getElementById('cli-regiao') ? document.getElementById('cli-regiao').value : '';
  var gps = document.getElementById('cli-gps-filtro') ? document.getElementById('cli-gps-filtro').value : '';
  var filtrados = _todosClientes.filter(function(c) {
    var mb = !busca || (c.nome||'').toLowerCase().indexOf(busca)>=0 || (c.endereco||'').toLowerCase().indexOf(busca)>=0 || String(c.codparc||'').indexOf(busca)>=0;
    var mr = !regiao || c.regiao === regiao;
    var mg = !gps || (gps==='sim' ? (c.lat&&c.lng) : !(c.lat&&c.lng));
    return mb && mr && mg;
  });
  renderClientes(filtrados);
}

function limparFiltrosClientes() {
  ['cli-busca','cli-regiao','cli-gps-filtro'].forEach(function(id){
    var e = document.getElementById(id); if(e) e.value='';
  });
  renderClientes(_todosClientes);
}

function renderClientes(lista) {
  var tbody = document.getElementById('clientes-tbody');
  var rodape = document.getElementById('clientes-rodape');
  if (!tbody) return;
  if (!lista.length) {
    tbody.innerHTML = '<tr><td colspan="9" class="loading-state">Nenhum parceiro encontrado</td></tr>';
    return;
  }
  var rows = '';
  lista.forEach(function(c) {
    var gps = (c.lat && c.lng) ? '<span style="color:#10b981">&#10003; GPS</span>' : '<span style="color:#f87171">Sem GPS</span>';
    var ativo = c.ativo === 'S' ? 'active' : 'inactive';
    var aLabel = c.ativo === 'S' ? 'Ativo' : 'Inativo';
    var cidade = (c.cidade || '').replace(' - AM','');
    rows += '<tr>' +
      '<td style="font-family:monospace;color:#64B4FF;font-weight:700">' + (c.codparc||'—') + '</td>' +
      '<td><b>' + (c.nome||'—') + '</b></td>' +
      '<td style="font-size:11px;color:#90afd4;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + (c.endereco||'—') + '</td>' +
      '<td style="font-size:11px">' + (c.bairro||'—') + '</td>' +
      '<td style="font-size:11px">' + cidade + '</td>' +
      '<td><span class="badge active" style="font-size:9px">' + (c.regiao||'—') + '</span></td>' +
      '<td style="text-align:center">' + gps + '</td>' +
      '<td style="font-size:11px">' + (c.telefone||'—') + '</td>' +
      '<td><span class="badge ' + ativo + '">' + aLabel + '</span></td>' +
      '</tr>';
  });
  tbody.innerHTML = rows;
  if (rodape) rodape.textContent = lista.length + ' parceiros exibidos';
}
</script>
"""

last_body = content.rfind('</body>')
content = content[:last_body] + bloco_limpo + '\n</body>\n</html>'

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica
body_count = content.count('</body>')
print(f'\nResultado: {body_count} </body>')
print('Pronto! Ctrl+Shift+R.')
