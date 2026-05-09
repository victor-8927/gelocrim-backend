path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Remove todas as versões antigas das funções de roteirização no script 3
funcoes = ['getCorRota','filtrarRotMapa','selecionarTodaRota','buscarFiltrados','renderRotMapMarkers']

for fn in funcoes:
    pattern = r'function ' + fn + r'\s*\([^)]*\)\s*\{'
    matches = list(re.finditer(pattern, content))
    for m in reversed(matches):
        # Encontra fim da função
        depth = 0
        i = m.start()
        while i < len(content):
            if content[i] == '{': depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
            i += 1
        antes = content[:m.start()]
        opens = antes.count('<script')
        closes = antes.count('</script>')
        ln = antes.count('\n')+1
        print(f'Removendo {fn} linha {ln} script {opens}')
        content = content[:m.start()] + content[end:]

# Agora adiciona versão nova e correta no script 3 (antes do </script>)
primeiro_close = content.find('</script>\n  <!-- MODAL IMPORTA')
if primeiro_close == -1:
    primeiro_close = content.find('\n// ── VEÍCULOS EDIÇÃO')
    if primeiro_close == -1:
        # Acha o fechamento do script 3
        scripts = list(re.finditer(r'<script[^>]*>', content))
        closes_list = list(re.finditer(r'</script>', content))
        primeiro_close = closes_list[2].start()

ln = content[:primeiro_close].count('\n')+1
print(f'\nInserindo funções antes da linha {ln}')

novo = '''
// ── ROTEIRIZAÇÃO VISUAL ───────────────────────────────────────────
var COR_ROTAS = {'801':'#FF6B35','802':'#4FC3F7','803':'#66BB6A','804':'#FFA726','805':'#AB47BC','811':'#EF5350','821':'#26C6DA','822':'#26C6DA'};

function getCorRota(val){
  if(!val) return '#90afd4';
  for(var k in COR_ROTAS){ if(val.toString().indexOf(k)>=0) return COR_ROTAS[k]; }
  return '#90afd4';
}

function filtrarRotMapa(){
  var cache = window._rotOrdersCache||[];
  if(!cache.length){ toast('Clique em Atualizar primeiro!','warn'); return; }
  renderRotMapMarkers(cache);
}

function buscarFiltrados(){
  var cache = window._rotOrdersCache||[];
  var fr  = document.getElementById('rot-filtro-rota');
  var freg= document.getElementById('rot-filtro-regiao');
  var fb  = document.getElementById('rot-filtro-bairro');
  var fs  = document.getElementById('rot-filtro-busca');
  var vr  = fr  ? fr.value  : '';
  var vreg= freg? freg.value: '';
  var vb  = fb  ? fb.value  : '';
  var vs  = fs  ? fs.value.toLowerCase() : '';
  if(!vr&&!vreg&&!vb&&!vs){ toast('Selecione ao menos um filtro!','warn'); return; }
  var candidatos = cache.filter(function(o){
    if(!o.lat||!o.lng) return false;
    if(vr   && (o.rota||o.regiao||'').indexOf(vr)<0)   return false;
    if(vreg && (o.regiao||'').indexOf(vreg)<0)          return false;
    if(vb   && (o.bairro||'').toLowerCase().indexOf(vb.toLowerCase())<0) return false;
    if(vs   && (o.recipient_name||'').toLowerCase().indexOf(vs)<0) return false;
    return true;
  });
  var novos=0;
  candidatos.forEach(function(o){
    if(!window.rotSelecionados[o.id]){ window.rotSelecionados[o.id]={order:o,marker:null}; novos++; }
  });
  renderRotMapMarkers(cache);
  atualizarSelecaoRot();
  toast(novos+' clientes selecionados!','success');
}

function renderRotMapMarkers(orders){
  setTimeout(function(){
    var m = initMap('rot-map');
    if(!m) return;
    (window._rotMapMarkers||[]).forEach(function(mk){ mk.setMap(null); });
    window._rotMapMarkers = [];

    var fr  = document.getElementById('rot-filtro-rota');
    var freg= document.getElementById('rot-filtro-regiao');
    var fb  = document.getElementById('rot-filtro-bairro');
    var fs  = document.getElementById('rot-filtro-busca');
    var vr  = fr  ? fr.value  : '';
    var vreg= freg? freg.value: '';
    var vb  = fb  ? fb.value  : '';
    var vs  = fs  ? fs.value.toLowerCase() : '';

    var filtrados = (orders||[]).filter(function(o){
      if(!o.lat||!o.lng) return false;
      if(vr   && (o.rota||o.regiao||'').indexOf(vr)<0)   return false;
      if(vreg && (o.regiao||'').indexOf(vreg)<0)          return false;
      if(vb   && (o.bairro||'').toLowerCase().indexOf(vb.toLowerCase())<0) return false;
      if(vs   && (o.recipient_name||'').toLowerCase().indexOf(vs)<0) return false;
      return true;
    });

    var st = document.getElementById('rot-map-status');
    if(st) st.textContent = filtrados.length+' clientes no mapa';

    var bounds = new google.maps.LatLngBounds();

    filtrados.forEach(function(o){
      var sel = !!window.rotSelecionados[o.id];
      var cor = sel ? '#10b981' : getCorRota(o.rota||o.regiao);

      var mk = new google.maps.Marker({
        position: {lat:parseFloat(o.lat), lng:parseFloat(o.lng)},
        map: m,
        title: (o.recipient_name||'')+'|'+(o.rota||o.regiao||''),
        animation: sel ? google.maps.Animation.BOUNCE : null,
        icon: {
          path: google.maps.SymbolPath.MAP_PIN,
          fillColor: cor,
          fillOpacity: 1,
          strokeColor: '#fff',
          strokeWeight: 1.5,
          scale: sel ? 6 : 4,
          anchor: new google.maps.Point(0, 22)
        }
      });

      if(sel) setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);

      var tempoMin = parseInt(o.tempo_entrega)||0;
      var iw = new google.maps.InfoWindow({content:
        '<div style="font-family:Arial;font-size:12px;padding:6px;min-width:200px">'+
        '<b style="font-size:13px">'+(o.recipient_name||'—')+'</b><br>'+
        '<span style="color:#e8521a;font-weight:700">Rota '+(o.rota||o.regiao||'—')+'</span><br>'+
        (o.bairro?'<span style="color:#666">🏘️ '+o.bairro+'</span><br>':'')+
        '<span style="color:#666">⏱️ '+(tempoMin>0?tempoMin+' min':'—')+'</span>'+
        '</div>'
      });

      mk.addListener('click', function(){
        if(window.rotSelecionados[o.id]){
          delete window.rotSelecionados[o.id];
          mk.setAnimation(null);
          mk.setIcon({path:google.maps.SymbolPath.MAP_PIN,fillColor:getCorRota(o.rota||o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:1.5,scale:4,anchor:new google.maps.Point(0,22)});
        } else {
          window.rotSelecionados[o.id] = {order:o, marker:mk};
          mk.setAnimation(google.maps.Animation.BOUNCE);
          setTimeout(function(){ try{mk.setAnimation(null);}catch(e){} }, 2100);
          mk.setIcon({path:google.maps.SymbolPath.MAP_PIN,fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:1.5,scale:6,anchor:new google.maps.Point(0,22)});
          iw.open(m, mk);
        }
        atualizarSelecaoRot();
      });

      window._rotMapMarkers.push(mk);
      bounds.extend({lat:parseFloat(o.lat), lng:parseFloat(o.lng)});
    });

    if(filtrados.length>0 && !bounds.isEmpty()) m.fitBounds(bounds);
  }, 200);
}
'''

content = content[:primeiro_close] + novo + content[primeiro_close:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Valida
import subprocess
scripts_list = list(re.finditer(r'<script[^>]*>', content))
closes_list  = list(re.finditer(r'</script>', content))
script3_start = scripts_list[2].end()
script3_end   = closes_list[2].start()
script3 = content[script3_start:script3_end]
with open(r'C:\fleet-cloud\test_s3.js','w',encoding='utf-8') as f:
    f.write('var google={maps:{Map:function(){},Marker:function(){this.addListener=function(){this.setMap=function(){};};this.setMap=function(){};this.setIcon=function(){};this.setAnimation=function(){};this.getTitle=function(){return "";};this.getAnimation=function(){return null;};},SymbolPath:{CIRCLE:0,MAP_PIN:1},InfoWindow:function(){this.open=function(){};},Animation:{BOUNCE:1},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return false;};},LatLng:function(){},event:{trigger:function(){}}}};\nfunction api(){}function toast(){}function initMap(){return new google.maps.Map();}function addMarker(){}function atualizarSelecaoRot(){}\nwindow.rotSelecionados={};\nwindow._rotMapMarkers=[];\nwindow._rotOrdersCache=[];\n')
    f.write(script3)
r = subprocess.run(['node','--check',r'C:\fleet-cloud\test_s3.js'],capture_output=True,text=True)
if r.returncode==0:
    print('Script 3 VALIDO!')
else:
    print('ERRO:',r.stderr[:500])
