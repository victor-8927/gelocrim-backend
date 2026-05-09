path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
idx = content.find('function atualizarSelecaoRot()')
depth=0; i=idx
while i < len(content):
    if content[i]=='{': depth+=1
    elif content[i]=='}':
        depth-=1
        if depth==0: end=i+1; break
    i+=1

new_fn = """function atualizarSelecaoRot(){
  var itens = Object.values(window.rotSelecionados);
  var count    = document.getElementById('rot-count');
  var pesoEl   = document.getElementById('rot-total-peso');
  var volEl    = document.getElementById('rot-total-vol');
  var btnRot   = document.getElementById('btn-rot-map');
  var cardVeic = document.getElementById('card-sel-veiculo');

  var pesoTotal = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).weight_kg)||0); }, 0);
  var volTotal  = itens.reduce(function(s,x){ return s+(parseFloat((x.order||{}).volume_m3)||0); }, 0);
  var tempoTotal= itens.reduce(function(s,x){ return s+(parseInt((x.order||{}).tempo_entrega)||15); }, 0);

  // Pallets estimados: peso_pallet_max = 700kg (gelo 20kg*35un=700kg p/ pallet)
  var PESO_PALLET = 700;
  var palletsEst = Math.ceil(pesoTotal / PESO_PALLET) || 0;

  // Tempo estimado em horas e minutos
  var totalMin = tempoTotal + (itens.length * 10); // +10min deslocamento médio por cliente
  var horas = Math.floor(totalMin/60);
  var mins  = totalMin % 60;
  var tempoStr = horas>0 ? horas+'h '+mins+'min' : mins+'min';

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
    if(el('sug-tempo'))      el('sug-tempo').textContent      = tempoStr;
  }

  if(cardVeic) cardVeic.style.display = itens.length>0 ? 'block' : 'none';
  if(btnRot){ btnRot.disabled=itens.length===0; btnRot.style.opacity=itens.length>0?'1':'0.5'; }
  renderListaSel(itens);
}"""

content = content[:idx] + new_fn + content[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('atualizarSelecaoRot reescrita com pallets e tempo!')

# Agora insere o painel HTML se não existir
if 'rot-sugestao-veiculo' not in content:
    print('Painel rot-sugestao-veiculo NAO encontrado no HTML!')
else:
    print('Painel rot-sugestao-veiculo JA existe no HTML!')
    idx2 = content.find('rot-sugestao-veiculo')
    ln = content[:idx2].count('\n')+1
    print(f'  linha {ln}')
print('Pronto! Ctrl+Shift+R.')
