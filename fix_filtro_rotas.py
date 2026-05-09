path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix o select de rotas no HTML — adiciona rotas fixas
old = '''        <select id="rot-filtro-rota" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">Todas as rotas</option>
        </select>'''

new = '''        <select id="rot-filtro-rota" onchange="filtrarRotMapa()" style="padding:6px 10px;border:1px solid #1e3a5c;border-radius:6px;font-size:12px;background:#0a1628;color:#e8f0fe">
          <option value="">Todas as rotas</option>
          <option value="801">Rota 801</option>
          <option value="802">Rota 802</option>
          <option value="803">Rota 803</option>
          <option value="804">Rota 804</option>
          <option value="805">Rota 805</option>
          <option value="811">Rota 811</option>
          <option value="821">Rota 821</option>
          <option value="822">Rota 822</option>
        </select>'''

if old in content:
    content = content.replace(old, new)
    print('Select de rotas atualizado!')
else:
    print('Padrão não encontrado!')

# 2. Corrige selecionarTodaRota para usar o valor do filtro
old2 = """function selecionarTodaRota(){
  var fr=document.getElementById('rot-filtro-rota');
  var filtro=fr?fr.value:'';
  if(!filtro){toast('Selecione uma rota!','warn');return;}"""

new2 = """function selecionarTodaRota(){
  var fr=document.getElementById('rot-filtro-rota');
  var filtro=fr?fr.value:'';
  if(!filtro){
    // Se não tem filtro, avisa para selecionar no dropdown
    fr.style.border='2px solid #e8521a';
    setTimeout(function(){if(fr)fr.style.border='1px solid #1e3a5c';},2000);
    toast('Selecione uma rota no filtro acima!','warn');
    return;
  }"""

if old2 in content:
    content = content.replace(old2, new2)
    print('selecionarTodaRota corrigido!')

# 3. Garante que renderRotMapMarkers usa window._rotOrdersCache
old3 = "function filtrarRotMapa(){ renderRotMapMarkers(_rotOrdersCache); }"
new3 = "function filtrarRotMapa(){ renderRotMapMarkers(window._rotOrdersCache||[]); }"
content = content.replace(old3, new3)

# 4. Também popula o select dinamicamente no loadRotMapData com as rotas reais
old4 = """    if(sel) sel.innerHTML='<option value="">Todas as rotas</option>'+
      Object.keys(regioes).sort().map(function(r){
        return '<option value="'+r+'">'+r+'</option>';
      }).join('');"""

new4 = """    if(sel){
      var rotasFixas=['801','802','803','804','805','811','821','822'];
      var rotasDinamicas=Object.keys(regioes).sort().filter(function(r){
        return rotasFixas.indexOf(r)<0;
      });
      var todasRotas=rotasFixas.concat(rotasDinamicas);
      sel.innerHTML='<option value="">Todas as rotas</option>'+
        todasRotas.map(function(r){
          var count=items.filter(function(o){return (o.regiao||'').indexOf(r)>=0;}).length;
          return count>0?'<option value="'+r+'">Rota '+r+' ('+count+' clientes)</option>':'';
        }).join('');
    }"""

if old4 in content:
    content = content.replace(old4, new4)
    print('Select populado com contagem de clientes!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto! Ctrl+Shift+R.')
