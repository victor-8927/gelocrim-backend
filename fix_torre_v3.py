path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui loadMonitoring + loadTorreControle
idx1 = content.find('async function loadMonitoring()')
idx2 = content.find('async function loadTorreControle()')
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

print(f'Substituindo linhas {content[:idx1].count(chr(10))+1} a {content[:idx_end].count(chr(10))+1}')

nova = (
    "async function loadMonitoring(){await loadTorreControle();}\n"
    "async function loadTorreControle(){\n"
    "  var dateEl=document.getElementById('mon-date');\n"
    "  var date=dateEl?dateEl.value:new Date().toISOString().slice(0,10);\n"
    "  try{\n"
    "    var rotas=await api('GET','/routes?date='+date);\n"
    "    var exec=rotas.filter(function(r){return r.status==='executing';}).length;\n"
    "    var done2=rotas.filter(function(r){return r.status==='done';}).length;\n"
    "    var lib=rotas.filter(function(r){return r.status==='released';}).length;\n"
    "    var totP=rotas.reduce(function(s,r){return s+(r.total_stops||0);},0);\n"
    "    var totE=rotas.reduce(function(s,r){return s+(r.delivered_stops||0);},0);\n"
    "    var pct=totP>0?Math.round(totE/totP*100):0;\n"
    "    var kpisEl=document.getElementById('mon-kpis');\n"
    "    if(kpisEl) kpisEl.innerHTML=[\n"
    "      ['🚛','Em Rota',exec,'#00BFFF'],['✅','Concluídas',done2,'#00FF88'],\n"
    "      ['🟢','Liberadas',lib,'#FFD700'],['📦','Entregas',totE+'/'+totP,'#a78bfa'],\n"
    "      ['📊','Progresso',pct+'%',pct>=80?'#00FF88':pct>=50?'#FFD700':'#FF3355'],\n"
    "    ].map(function(k){\n"
    "      return '<div style=\"background:#0a1628;border:1px solid #1e3a5c;border-radius:10px;padding:12px;text-align:center\">'+\n"
    "        '<div style=\"font-size:18px\">'+k[0]+'</div>'+\n"
    "        '<div style=\"font-size:22px;font-weight:800;color:'+k[3]+'\">'+k[2]+'</div>'+\n"
    "        '<div style=\"font-size:10px;color:#90afd4\">'+k[1]+'</div></div>';\n"
    "    }).join('');\n"
    "    var lista=document.getElementById('mon-rotas-lista');\n"
    "    if(lista){\n"
    "      if(!rotas.length){lista.innerHTML='<div style=\"color:#90afd4;font-size:12px;text-align:center;padding:20px\">Nenhuma rota hoje</div>';}\n"
    "      else{\n"
    "        var corS={optimized:'#90afd4',released:'#FFD700',executing:'#00BFFF',done:'#00FF88'};\n"
    "        var lblS={optimized:'Conferida',released:'Liberada',executing:'Em Rota',done:'Concluída'};\n"
    "        lista.innerHTML=rotas.map(function(r){\n"
    "          var p=r.total_stops>0?Math.round((r.delivered_stops||0)/r.total_stops*100):0;\n"
    "          var cor=corS[r.status]||'#90afd4';\n"
    "          var sel=window._monRotaSel===r.route_id;\n"
    "          return '<div onclick=\"selecionarRotaMon(\\''+r.route_id+'\\')\" style=\"background:'+(sel?'rgba(0,191,255,0.1)':'#0a1628')+';border:1px solid '+(sel?'#00BFFF':'#1e3a5c')+';border-radius:10px;padding:10px;cursor:pointer;margin-bottom:6px\">'+\n"
    "            '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:4px\">'+\n"
    "              '<b style=\"font-size:11px;color:#e8f0fe;font-family:monospace\">'+(r.trip_number||'—')+'</b>'+\n"
    "              '<span style=\"font-size:9px;font-weight:700;color:'+cor+'\">● '+(lblS[r.status]||r.status)+'</span>'+\n"
    "            '</div>'+\n"
    "            '<div style=\"font-size:11px;color:#64B4FF;margin-bottom:4px\">'+(r.vehicle_plate||'—')+' · '+(r.driver_name||'—')+'</div>'+\n"
    "            '<div style=\"background:#1e3a5c;border-radius:3px;height:4px;overflow:hidden\"><div style=\"height:100%;background:'+cor+';width:'+p+'%\"></div></div>'+\n"
    "            '<div style=\"font-size:10px;color:#90afd4;margin-top:3px\">'+(r.delivered_stops||0)+'/'+r.total_stops+' · '+p+'%</div></div>';\n"
    "        }).join('');\n"
    "      }\n"
    "    }\n"
    "    if(!window._monMap) window._monMap=initMap('mon-map',-3.093544,-60.075812,11);\n"
    "    if(window._monMap){\n"
    "      if(!window._monMarkers) window._monMarkers=[];\n"
    "      window._monMarkers.forEach(function(m){m.setMap(null);}); window._monMarkers=[];\n"
    "      var mkDep=new google.maps.Marker({position:{lat:-3.093544,lng:-60.075812},map:window._monMap,\n"
    "        icon:{path:google.maps.SymbolPath.CIRCLE,scale:12,fillColor:'#e8521a',fillOpacity:1,strokeColor:'#fff',strokeWeight:2},title:'Depósito'});\n"
    "      window._monMarkers.push(mkDep);\n"
    "      var cores=['#00BFFF','#00FF88','#FFD700','#a78bfa','#f97316','#f43f5e'];\n"
    "      for(var ri=0;ri<rotas.length;ri++){\n"
    "        var rot=rotas[ri]; if(rot.status==='optimized') continue;\n"
    "        try{\n"
    "          var stops=await api('GET','/routes/'+rot.route_id+'/stops');\n"
    "          var cr=cores[ri%6];\n"
    "          stops.forEach(function(s){\n"
    "            var lat=parseFloat(s.lat),lng=parseFloat(s.lng); if(!lat||!lng) return;\n"
    "            var sc=s.status==='completed'?'#00FF88':s.status==='failed'?'#FF3355':s.status==='reentrega'?'#FFD700':cr;\n"
    "            var mk=new google.maps.Marker({position:{lat:lat,lng:lng},map:window._monMap,\n"
    "              icon:{path:google.maps.SymbolPath.CIRCLE,scale:10,fillColor:sc,fillOpacity:1,strokeColor:'#001020',strokeWeight:2},\n"
    "              title:s.recipient_name});\n"
    "            var iw=new google.maps.InfoWindow({content:'<div style=\"background:#0a1628;color:#e8f0fe;padding:8px;border-radius:6px;font-size:12px\"><b>'+(s.recipient_name||'')+'</b><br>'+s.status+'</div>'});\n"
    "            mk.addListener('click',function(){iw.open(window._monMap,mk);});\n"
    "            window._monMarkers.push(mk);\n"
    "          });\n"
    "        }catch(e){}\n"
    "      }\n"
    "    }\n"
    "  }catch(e){toast('Erro Torre: '+e.message,'error');}\n"
    "}\n"
    "\n"
    "async function selecionarRotaMon(routeId){\n"
    "  window._monRotaSel=routeId;\n"
    "  var tl=document.getElementById('mon-timeline');\n"
    "  if(!tl) return;\n"
    "  tl.innerHTML='<div style=\"color:#90afd4\">Carregando...</div>';\n"
    "  try{\n"
    "    var stops=await api('GET','/routes/'+routeId+'/stops');\n"
    "    var rotas=await api('GET','/routes');\n"
    "    var rota=rotas.find(function(r){return r.route_id===routeId;})||{};\n"
    "    var corS={pending:'#90afd4',completed:'#00FF88',failed:'#FF3355',reentrega:'#FFD700'};\n"
    "    var icoS={pending:'⏳',completed:'✅',failed:'❌',reentrega:'🟡'};\n"
    "    tl.innerHTML='<div style=\"font-size:11px;color:#64B4FF;font-weight:700;margin-bottom:8px\">'+(rota.trip_number||'Rota')+' — '+(rota.driver_name||'—')+'</div>'+\n"
    "      stops.map(function(s){\n"
    "        var cor=corS[s.status]||'#90afd4'; var ico=icoS[s.status]||'⏳';\n"
    "        var hora=s.ata?new Date(s.ata).toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'}):(s.eta||'—');\n"
    "        var btnR=s.status==='reentrega'?\n"
    "          '<div style=\"margin-top:4px;display:flex;gap:4px\">'+\n"
    "            '<button onclick=\"aprovarReentrega(\\''+routeId+'\\',\\''+s.stop_id+'\\')\" style=\"font-size:9px;padding:2px 8px;background:#FFD700;border:none;color:#001020;border-radius:4px;cursor:pointer\">✅ Autorizar</button>'+\n"
    "            '<button onclick=\"rejeitarReentrega(\\''+routeId+'\\',\\''+s.stop_id+'\\')\" style=\"font-size:9px;padding:2px 8px;background:#FF3355;border:none;color:#fff;border-radius:4px;cursor:pointer\">❌ Rejeitar</button>'+\n"
    "          '</div>':'';\n"
    "        return '<div style=\"display:flex;gap:8px;padding:7px 0;border-bottom:1px solid #1e3a5c;align-items:flex-start\">'+\n"
    "          '<div style=\"width:20px;height:20px;border-radius:50%;background:'+cor+';display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:10px;font-weight:700;color:#001020\">'+(s.sequence+1)+'</div>'+\n"
    "          '<div style=\"flex:1\"><div style=\"font-size:11px;font-weight:600;color:#e8f0fe\">'+ico+' '+(s.recipient_name||'—')+'</div>'+\n"
    "          '<div style=\"font-size:10px;color:#90afd4\">'+hora+(s.failure_reason?' · '+s.failure_reason:'')+'</div>'+btnR+'</div></div>';\n"
    "      }).join('');\n"
    "    loadTorreControle();\n"
    "  }catch(e){tl.innerHTML='<div style=\"color:#f87171\">Erro: '+e.message+'</div>';}\n"
    "}\n"
    "\n"
    "async function aprovarReentrega(routeId,stopId){\n"
    "  if(!confirm('Autorizar reentrega?')) return;\n"
    "  try{await api('PATCH','/routes/'+routeId+'/stops/'+stopId,{status:'pending',failure_reason:''});toast('✅ Autorizado!','success');selecionarRotaMon(routeId);}\n"
    "  catch(e){toast('Erro','error');}\n"
    "}\n"
    "async function rejeitarReentrega(routeId,stopId){\n"
    "  if(!confirm('Rejeitar?')) return;\n"
    "  try{await api('PATCH','/routes/'+routeId+'/stops/'+stopId,{status:'failed',failure_reason:'Rejeitada pela Torre'});toast('❌ Rejeitada','warn');selecionarRotaMon(routeId);}\n"
    "  catch(e){toast('Erro','error');}\n"
    "}\n"
    "function toggleMapaTipo(){if(!window._monMap) return;var t=window._monMap.getMapTypeId();window._monMap.setMapTypeId(t==='roadmap'?'satellite':'roadmap');var b=document.getElementById('btn-mapa-tipo');if(b) b.textContent=t==='roadmap'?'🗺️ Mapa':'🛰️ Satélite';}\n"
    "function toggleTrafegoMon(){if(!window._monMap) return;if(!window._monMap._tc){window._monMap._tc=new google.maps.TrafficLayer();window._monMap._tc.setMap(window._monMap);}else{window._monMap._tc.setMap(null);window._monMap._tc=null;}}\n"
)

content = content[:idx1] + nova + content[idx_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Torre de Controle implementada! Ctrl+Shift+R -> Monitoramento')
