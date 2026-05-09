path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Atualiza renderClientes para adicionar botão Detalhar
old = '''function renderClientes(lista) {
  var tbody  = document.getElementById('clientes-tbody');
  var rodape = document.getElementById('clientes-rodape');
  if(!tbody) return;
  if(!lista.length){tbody.innerHTML='<tr><td colspan="9" class="loading-state">Nenhum parceiro</td></tr>';return;}
  var rows = '';
  lista.forEach(function(c){
    var gps = (c.lat&&c.lng)?'<span style="color:#10b981">GPS</span>':'<span style="color:#f87171">Sem GPS</span>';
    var at  = c.ativo==='S'?'active':'inactive';
    var cidade = (c.cidade||'').replace(' - AM','');
    rows += '<tr>'+
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
  tbody.innerHTML = rows;
  if(rodape) rodape.textContent = lista.length+' parceiros';
}'''

new = '''function renderClientes(lista) {
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
  var mapa = c.lat && c.lng
    ? '<a href="https://www.google.com/maps?q='+c.lat+','+c.lng+'" target="_blank" style="color:#64B4FF;font-size:11px">📍 Ver no Google Maps</a>'
    : '<span style="color:#f87171;font-size:11px">Sem coordenadas GPS</span>';
  var html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+
    campo('Código ERP', c.codparc) +
    campo('Nome Fantasia', c.nome) +
    campo('Razão Social', c.razao_social) +
    campo('CPF/CNPJ', c.cpf_cnpj) +
    campo('Telefone', c.telefone) +
    campo('Segmento', c.segmento) +
    campo('Região/Rota', c.regiao) +
    campo('Zona Geo', c.zona_geo) +
    '<div style="grid-column:1/-1">'+campoFull('Endereço', c.endereco)+'</div>'+
    campo('Bairro', c.bairro) +
    campo('CEP', c.cep) +
    campo('Cidade', c.cidade) +
    campo('Latitude', c.lat) +
    campo('Longitude', c.lng) +
    '<div style="grid-column:1/-1;margin-top:4px">'+mapa+'</div>'+
    campo('Comodatos', c.comodatos) +
    campo('Tempo Médio Entrega', c.tempo_entrega) +
    campo('Rota', c.rota) +
    campo('Status', c.ativo==='S'?'Ativo':'Inativo') +
    '</div>';

  // Abre modal genérico ou cria um simples
  var existing = document.getElementById('modal-parceiro-detalhe');
  if(!existing){
    var div = document.createElement('div');
    div.id = 'modal-parceiro-detalhe';
    div.onclick = function(e){if(e.target===div)div.style.display='none';};
    div.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:3000;align-items:center;justify-content:center;padding:20px';
    div.innerHTML = '<div style="background:#0f2040;border:1px solid #1e3a5c;border-radius:16px;width:680px;max-height:85vh;overflow-y:auto">'+
      '<div style="padding:16px 24px;border-bottom:1px solid #1e3a5c;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:#0f2040;border-radius:16px 16px 0 0">'+
      '<span style="font-size:15px;font-weight:700;color:#e8f0fe" id="modal-parc-titulo">Parceiro</span>'+
      '<button onclick="document.getElementById(\'modal-parceiro-detalhe\').style.display=\'none\'" style="background:none;border:none;color:#90afd4;font-size:20px;cursor:pointer">✕</button>'+
      '</div><div id="modal-parc-body" style="padding:20px 24px"></div></div>';
    document.body.appendChild(div);
    existing = div;
  }
  document.getElementById('modal-parc-titulo').textContent = '🤝 '+( c.nome||'Parceiro');
  document.getElementById('modal-parc-body').innerHTML = html;
  existing.style.display = 'flex';
}

function campo(label, valor) {
  return '<div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px">'+
    '<div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px;margin-bottom:3px">'+label+'</div>'+
    '<div style="font-size:13px;color:#e8f0fe;font-weight:500">'+(valor||'—')+'</div>'+
    '</div>';
}
function campoFull(label, valor) {
  return '<div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px">'+
    '<div style="font-size:10px;color:#90afd4;text-transform:uppercase;letter-spacing:.8px;margin-bottom:3px">'+label+'</div>'+
    '<div style="font-size:13px;color:#e8f0fe;font-weight:500">'+(valor||'—')+'</div>'+
    '</div>';
}'''

if old in content:
    content = content.replace(old, new)
    print('renderClientes atualizado com botão detalhar!')
else:
    print('PADRAO NAO ENCONTRADO!')

# 2. Atualiza cabeçalho da tabela de parceiros para ter coluna Ações
old_th = '''<th>Cód.</th>
                <th>Nome</th>
                <th>Endereço</th>
                <th>Bairro</th>
                <th>Cidade</th>
                <th>Região</th>
                <th>GPS</th>
                <th>Telefone</th>
                <th>Status</th>'''
new_th = '''<th>Cód.</th>
                <th>Nome</th>
                <th>Endereço</th>
                <th>Bairro</th>
                <th>Cidade</th>
                <th>Região</th>
                <th>GPS / Coords</th>
                <th>Telefone</th>
                <th>Status</th>
                <th>Ações</th>'''
if old_th in content:
    content = content.replace(old_th, new_th)
    print('Cabeçalho da tabela atualizado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
