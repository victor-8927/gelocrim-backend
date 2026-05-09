path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza as funções existentes
import re

# Encontra loadMonitoring e loadTorreControle e substitui ambas
idx1 = content.find('async function loadMonitoring()')
idx2 = content.find('async function loadTorreControle()')

# Encontra o fim do bloco loadTorreControle
i = idx2
depth = 0
started = False
while i < len(content):
    if content[i] == '{': depth += 1; started = True
    elif content[i] == '}':
        depth -= 1
        if started and depth == 0:
            idx_end = i + 1
            break
    i += 1

print(f'loadMonitoring: linha {content[:idx1].count(chr(10))+1}')
print(f'loadTorreControle: linha {content[:idx2].count(chr(10))+1}')
print(f'Fim do bloco: linha {content[:idx_end].count(chr(10))+1}')
print(f'Trecho atual: {repr(content[idx1:idx1+80])}')

# Substitui desde loadMonitoring até o fim do loadTorreControle
nova = """async function loadMonitoring(){await loadTorreControle();}

async function loadTorreControle(){
  var dateEl=document.getElementById('mon-date');
  var date=dateEl?dateEl.value:new Date().toISOString().slice(0,10);
  try{
    var rotas=await api('GET','/routes?date='+date);
    var exec=rotas.filter(function(r){return r.status==='executing';}).length;
    var done=rotas.filter(function(r){return r.status==='done';}).length;
    var lib=rotas.filter(function(r){return r.status==='released';}).length;
    var totP=rotas.reduce(function(s,r){return s+(r.total_stops||0);},0);
    var totE=rotas.reduce(function(s,r){return s+(r.delivered_stops||0);},0);
    var pct=totP>0?Math.round(totE/totP*100):0;
    var kpisEl=document.getElementById('mon-kpis');
    if(kpisEl) kpisEl.innerHTML=[
      ['🚛','Em Rota',exec,'#00BFFF'],
      ['✅','Concluídas',done,'#00FF88'],
      ['🟢','Liberadas',lib,'#FFD700'],
      ['📦','Entregas',totE+'/'+totP,'#a78bfa'],
      ['📊','Progresso',pct+'%',pct>=80?'#00FF88':pct>=50?'#FFD700':'#FF3355'],
    ].map(function(k){
      return '<div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:12px;text-align:center">'+
        '<div style="font-size:18px">'+k[0]+'</div>'+
        '<div style="font-size:22px;font-weight:800;color:'+k[3]+'">'+k[2]+'</div>'+
        '<div style="font-size:10px;color:#90afd4;margin-top:2px">'+k[1]+'</div></div>';
    }).join('');
    var lista=document.getElementById('mon-rotas-lista');
    if(lista){
      if(!rotas.length){lista.innerHTML='<div style="color:#90afd4;font-size:12px;text-align:center;padding:20px">Nenhuma rota hoje</div>';}
      else{
        var corS={optimized:'#90afd4',released:'#FFD700',executing:'#00BFFF',done:'#00FF88'};
        var lblS={optimized:'Conferida',released:'Liberada',executing:'Em Rota',done:'Concluída'};
        lista.innerHTML=rotas.map(function(r){
          var p=r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;
          var cor=corS[r.status]||'#90afd4';
          var sel=window._monRotaSel===r.route_id;
          return '<div onclick="selecionarRotaMon(\''+r.route_id+'\')" style="background:'+(sel?'rgba(0,191,255,0.1)':'#0a1628')+';border:1px solid '+(sel?'#00BFFF':'#1e3a5c')+';border-radius:10px;padding:10px;cursor:pointer;margin-bottom:6px">'+
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'+
              '<b style="font-size:11px;color:#e8f0fe;font-family:monospace">'+(r.trip_number||'—')+'</b>'+
              '<span style="font-size:9px;font-weight:700;color:'+cor+'">● '+(lblS[r.status]||r.status)+'</span>'+
            '</div>'+
            '<div style="font-size:11px;color:#64B4FF;margin-bottom:4px">'+(r.vehicle_plate||'—')+' · '+(r.driver_name||'—')+'</div>'+
            '<div style="background:#1e3a5c;border-radius:3px;height:4px;overflow:hidden"><div style="height:100%;background:'+cor+';width:'+p+'%"></div></div>'+
            '<div style="font-size:10px;color:#90afd4;margin-top:3px">'+(r.delivered_stops||0)+'/'+r.total_stops+' · '+p+'%</div></div>';
        }).join('');
      }
    }
    if(!window._monMap) window._monMap=initMap('mon-map',-3.093544,-60.075812,11);
    if(window._monMap){
      if(!window._monMarkers) window._monMarkers=[];
      window._monMarkers.forEach(function(m){m.setMap(null);}); window._monMarkers=[];
      var dep=new google.maps.Marker({position:{lat:-3.093544,lng:-60.075812},map:window._monMap,
        icon:{path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2},title:'Depósito'});
      window._monMarkers.push(dep);
      var cores=['#00BFFF','#00FF88','#FFD700','#a78bfa','#f97316','#f43f5e'];
      for(var ri=0;ri<rotas.length;ri++){
        var rota=rotas[ri];
        if(rota.status==='optimized') continue;
        try{
          var stops=await api('GET','/routes/'+rota.route_id+'/stops');
          var cr=cores[ri%6];
          stops.forEach(function(s){
            var lat=parseFloat(s.lat),lng=parseFloat(s.lng);
            if(!lat||!lng) return;
            var sc=s.status==='completed'?'#00FF88':s.status==='failed'?'#FF3355':s.status==='reentrega'?'#FFD700':cr;
            var mk=new google.maps.Marker({
              position:{lat:lat,lng:lng},map:window._monMap,
              icon:{path:google.maps.SymbolPath.CIRCLE,scale:10,fillColor:sc,fillOpacity:1,strokeColor:'#001020',strokeWeight:2},
              title:s.recipient_name
            });
            var iw=new google.maps.InfoWindow({content:'<div style="background:#0a1628;color:#e8f0fe;padding:8px;border-radius:6px;font-size:12px"><b>'+(s.recipient_name||'')+'</b><br>'+s.status+'</div>'});
            mk.addListener('click',function(){iw.open(window._monMap,mk);});
            window._monMarkers.push(mk);
          });
        }catch(e){}
      }
    }
  }catch(e){toast('Erro Torre: '+e.message,'error');}
}"""

content = content[:idx1] + nova + content[idx_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Adiciona funções auxiliares se não existirem
funcs_aux = """
async function selecionarRotaMon(routeId){
  window._monRotaSel=routeId;
  var tl=document.getElementById('mon-timeline');
  if(!tl) return;
  tl.innerHTML='<div style="color:#90afd4;font-size:11px">Carregando...</div>';
  try{
    var stops=await api('GET','/routes/'+routeId+'/stops');
    var rotas=await api('GET','/routes');
    var rota=rotas.find(function(r){return r.route_id===routeId;})||{};
    var comp=stops.filter(function(s){return s.status==='completed';}).length;
    var reet=stops.filter(function(s){return s.status==='reentrega';}).length;
    var fail=stops.filter(function(s){return s.status==='failed';}).length;
    var corS={pending:'#90afd4',completed:'#00FF88',failed:'#FF3355',reentrega:'#FFD700'};
    var icoS={pending:'⏳',completed:'✅',failed:'❌',reentrega:'🟡'};
    tl.innerHTML=
      '<div style="font-size:11px;color:#64B4FF;font-weight:700;margin-bottom:8px">'+(rota.trip_number||'Rota')+' — '+(rota.driver_name||'—')+'</div>'+
      '<div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap">'+
        '<span style="font-size:10px;background:rgba(0,255,136,.15);color:#00FF88;padding:2px 6px;border-radius:4px">✅ '+comp+'</span>'+
        (reet?'<span style="font-size:10px;background:rgba(255,215,0,.15);color:#FFD700;padding:2px 6px;border-radius:4px">🟡 '+reet+'</span>':'')+
        (fail?'<span style="font-size:10px;background:rgba(255,51,85,.15);color:#FF3355;padding:2px 6px;border-radius:4px">❌ '+fail+'</span>':'')+
      '</div>'+
      stops.map(function(s){
        var cor=corS[s.status]||'#90afd4';
        var ico=icoS[s.status]||'⏳';
        var hora=s.ata?new Date(s.ata).toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'}):(s.eta||'—');
        var btnR=s.status==='reentrega'?
          '<div style="margin-top:4px;display:flex;gap:4px">'+
            '<button onclick="aprovarReentrega(\''+routeId+'\',\''+s.stop_id+'\')" style="font-size:9px;padding:2px 8px;background:#FFD700;border:none;color:#001020;border-radius:4px;cursor:pointer">✅ Autorizar</button>'+
            '<button onclick="rejeitarReentrega(\''+routeId+'\',\''+s.stop_id+'\')" style="font-size:9px;padding:2px 8px;background:#FF3355;border:none;color:#fff;border-radius:4px;cursor:pointer">❌ Rejeitar</button>'+
          '</div>':'';
        return '<div style="display:flex;gap:8px;padding:7px 0;border-bottom:1px solid #1e3a5c;align-items:flex-start">'+
          '<div style="width:20px;height:20px;border-radius:50%;background:'+cor+';display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:10px;font-weight:700;color:#001020">'+(s.sequence+1)+'</div>'+
          '<div style="flex:1"><div style="font-size:11px;font-weight:600;color:#e8f0fe">'+ico+' '+(s.recipient_name||'—')+'</div>'+
          '<div style="font-size:10px;color:#90afd4">'+hora+(s.failure_reason?' · '+s.failure_reason:'')+'</div>'+btnR+'</div></div>';
      }).join('');
    loadTorreControle();
  }catch(e){tl.innerHTML='<div style="color:#f87171">Erro: '+e.message+'</div>';}
}

async function aprovarReentrega(routeId,stopId){
  if(!confirm('Autorizar reentrega?')) return;
  try{await api('PATCH','/routes/'+routeId+'/stops/'+stopId,{status:'pending',failure_reason:''});toast('✅ Reentrega autorizada!','success');selecionarRotaMon(routeId);}
  catch(e){toast('Erro: '+e.message,'error');}
}

async function rejeitarReentrega(routeId,stopId){
  if(!confirm('Rejeitar reentrega?')) return;
  try{await api('PATCH','/routes/'+routeId+'/stops/'+stopId,{status:'failed',failure_reason:'Rejeitada pela Torre'});toast('❌ Rejeitada.','warn');selecionarRotaMon(routeId);}
  catch(e){toast('Erro: '+e.message,'error');}
}

function toggleMapaTipo(){
  if(!window._monMap) return;
  var t=window._monMap.getMapTypeId();
  window._monMap.setMapTypeId(t==='roadmap'?'satellite':'roadmap');
  var b=document.getElementById('btn-mapa-tipo');
  if(b) b.textContent=t==='roadmap'?'🗺️ Mapa':'🛰️ Satélite';
}

function toggleTrafegoMon(){
  if(!window._monMap) return;
  if(!window._monMap._tc){window._monMap._tc=new google.maps.TrafficLayer();window._monMap._tc.setMap(window._monMap);}
  else{window._monMap._tc.setMap(null);window._monMap._tc=null;}
}
"""

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'selecionarRotaMon' not in content:
    content = content.replace('</script>', funcs_aux + '\n</script>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Funções auxiliares adicionadas!')
else:
    print('Funções auxiliares já existem!')

import subprocess, re
scripts = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))
js = scripts[1].group(1)
stub = 'var google={maps:{Map:function(){this.getMapTypeId=function(){return"roadmap";};this.setMapTypeId=function(){};this.fitBounds=function(){};},Marker:function(){this.addListener=function(){};this.setMap=function(){};},SymbolPath:{CIRCLE:0},LatLngBounds:function(){this.extend=function(){};this.isEmpty=function(){return true;};},LatLng:function(){return{};},DirectionsService:function(){this.route=function(){};},DirectionsRenderer:function(){this.setMap=function(){};this.setDirections=function(){};},TrafficLayer:function(){this.setMap=function(){};},TravelMode:{DRIVING:"DRIVING"},Polyline:function(){this.setMap=function(){};},InfoWindow:function(){this.open=function(){};},event:{trigger:function(){}}}};var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};function fetch(){return Promise.resolve({json:function(){return Promise.resolve({});}});}function alert(){}function confirm(){return true;}'
with open(r'C:\fleet-cloud\test_s2.js','w',encoding='utf-8') as f:
    f.write(stub+'\n'+js)
r=subprocess.run(['node','--check',r'C:\fleet-cloud\test_s2.js'],capture_output=True)
stderr=r.stderr.decode('utf-8',errors='replace')
if r.returncode==0: print('VÁLIDO! Ctrl+Shift+R → Monitoramento')
else: print('ERRO:',stderr[:300])
