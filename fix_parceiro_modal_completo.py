path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a função detalharParceiro completa
old_func = 'function detalharParceiro(codparc) {'
idx = content.find(old_func)

# Encontra o fim da função
depth = 0
i = idx
while i < len(content):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end_func = i + 1
            break
    i += 1

old = content[idx:end_func]

new = '''function detalharParceiro(codparc) {
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
}'''

if old in content:
    content = content.replace(old, new)
    print('detalharParceiro atualizado!')
else:
    print('FUNCAO NAO ENCONTRADA - substituindo por posicao')
    content = content[:idx] + new + content[end_func:]
    print('Substituído por posição!')

# Remove funções campo/campoFull antigas que podem estar duplicadas
old_campo = '''\nfunction campo(label, valor) {
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
if old_campo in content:
    content = content.replace(old_campo, '')
    print('Funções campo duplicadas removidas!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
import subprocess
start = content.find('<script>\nvar _clientesCache')
end   = content.find('</script>', start)
script2 = content[start+8:end]
with open(r'C:\fleet-cloud\test_script2.js', 'w', encoding='utf-8') as f:
    f.write('var XLSX={};var google={maps:{Marker:function(){this.addListener=function(){};this.setIcon=function(){};},SymbolPath:{CIRCLE:0},event:{trigger:function(){}}}};function api(){}function toast(){}function initMap(){return null;}function addMarker(){}function closeModal(){}function openModal(){}function loadRoutes(){}\n')
    f.write(script2)
result = subprocess.run(['node','--check',r'C:\fleet-cloud\test_script2.js'],capture_output=True,text=True)
if result.returncode==0:
    print('Script VALIDO!')
else:
    print('ERRO:', result.stderr[:500])
