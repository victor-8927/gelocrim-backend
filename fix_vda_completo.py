path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Adiciona data-pallets e data-baucomp no select
old_frota = "return '<option value=\"'+v.id+'\" data-kg=\"'+v.capacity_kg+'\" data-m3=\"'+v.capacity_m3+'\">'+v.vda+' — '+v.plate+'</option>';"
new_frota = "return '<option value=\"'+v.id+'\" data-kg=\"'+(v.capacity_kg||0)+'\" data-m3=\"'+(v.capacity_m3||0)+'\" data-pallets=\"'+(v.pallets||0)+'\" data-bcomp=\"'+(v.bau_comp||0)+'\" data-blarg=\"'+(v.bau_larg||0)+'\" data-balt=\"'+(v.bau_alt||0)+'\">'+v.vda+' — '+v.plate+'</option>';"

if old_frota in content:
    content = content.replace(old_frota, new_frota)
    print('carregarFrota atualizado com pallets/baú!')
else:
    print('carregarFrota padrão não encontrado!')

# 2. Implementa rotVeiculoChanged completo
old_fn = "function rotVeiculoChanged(){}"
new_fn = """function rotVeiculoChanged(){
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
}"""

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print('rotVeiculoChanged implementado!')
else:
    print('rotVeiculoChanged padrão não encontrado!')

# 3. Chama rotVeiculoChanged ao selecionar veículo via onchange
old_sel = 'id="rot-veiculo-select" onchange="rotVeiculoChanged()"'
if old_sel not in content:
    content = content.replace(
        'id="rot-veiculo-select"',
        'id="rot-veiculo-select" onchange="rotVeiculoChanged()"'
    )
    print('onchange adicionado no select de veículo!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
