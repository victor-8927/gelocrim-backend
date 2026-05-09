path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a funcao loadTorreControle para adicionar pins numerados
old_markers = '''        stops.forEach(s => {
        const lat = parseFloat(s.lat), lng = parseFloat(s.lng);
        if (!lat || !lng) return;

        stopsLatLng.push({lat, lng});

        // Determina status e cor do pin
        let corPin = \'#2563eb\'; // pendente
        let iconeSize = 9;

        if (s.status === \'completed\') {
          corPin = \'#16a34a\';
          completadas++;
          iconeSize = 8;
        } else if (s.status === \'failed\') {
          corPin = \'#dc2626\';
          atrasadas++;
          iconeSize = 10;
        } else {
          // Verifica se está atrasado
          if (s.eta) {
            const [h, m] = s.eta.split(\':\').map(Number);
            const etaMins = h * 60 + m;
            if (agoraMins > etaMins + 30) {
              corPin = \'#dc2626\';
              atrasadas++;
              alertas.push(`${r.vehicle_plate}: ${s.recipient_name} atrasado (ETA ${s.eta})`);
            } else {
              corPin = \'#d97706\';
              pendentes++;
            }
          } else {
            pendentes++;
          }
        }

        if (tcMap) {
          const marker = new google.maps.Marker({
            position: {lat, lng},
            map: tcMap,
            title: s.recipient_name,
            icon: {
              path: google.maps.SymbolPath.CIRCLE,
              scale: iconeSize,
              fillColor: corPin,
              fillOpacity: 1,
              strokeColor: \'#fff\',
              strokeWeight: 2
            }
          });

          const iw = new google.maps.InfoWindow({
            content: `<div style="font-family:Arial;font-size:12px;min-width:180px">
              <b style="color:${cor}">${r.vehicle_plate}</b> — Parada ${s.sequence+1}<br>
              <b>${s.recipient_name}</b><br>
              ${s.address||\'\'}<br>
              ETA: <b>${s.eta||\'—\'}</b> | Status: <b>${s.status||\'pendente\'}</b><br>
              Peso: ${(s.weight_kg||0).toFixed(0)} kg
            </div>`
          });
          marker.addListener(\'click\', () => iw.open(tcMap, marker));
          tcMarkers.push(marker);
        }
      });'''

new_markers = '''        stops.forEach((s, stopIdx) => {
        const lat = parseFloat(s.lat), lng = parseFloat(s.lng);
        if (!lat || !lng) return;

        stopsLatLng.push({lat, lng});

        // Determina status e cor do pin
        let corPin = cor; // usa cor da rota
        let statusLabel = 'Pendente';

        if (s.status === 'completed') {
          corPin = '#16a34a';
          completadas++;
          statusLabel = 'Entregue';
        } else if (s.status === 'failed') {
          corPin = '#dc2626';
          atrasadas++;
          statusLabel = 'Falhou';
        } else {
          if (s.eta) {
            const [h, m] = s.eta.split(':').map(Number);
            const etaMins = h * 60 + m;
            if (agoraMins > etaMins + 30) {
              corPin = '#dc2626';
              atrasadas++;
              statusLabel = 'Atrasado';
              alertas.push(`${r.vehicle_plate}: ${s.recipient_name} atrasado (ETA ${s.eta})`);
            } else {
              pendentes++;
              statusLabel = 'Em rota';
            }
          } else {
            pendentes++;
          }
        }

        if (tcMap) {
          // Pin numerado com label
          const seqNum = s.sequence + 1;
          const marker = new google.maps.Marker({
            position: {lat, lng},
            map: tcMap,
            title: `${seqNum}. ${s.recipient_name}`,
            label: {
              text: String(seqNum),
              color: '#ffffff',
              fontSize: '11px',
              fontWeight: 'bold'
            },
            icon: {
              path: google.maps.SymbolPath.CIRCLE,
              scale: 14,
              fillColor: corPin,
              fillOpacity: 1,
              strokeColor: '#fff',
              strokeWeight: 2
            },
            zIndex: seqNum
          });

          const iw = new google.maps.InfoWindow({
            content: `<div style="font-family:Arial;font-size:12px;min-width:200px;padding:4px">
              <div style="background:${cor};color:#fff;padding:4px 8px;border-radius:4px;margin-bottom:6px;font-weight:700">
                ${r.vehicle_plate} — Parada ${seqNum}
              </div>
              <b>${s.recipient_name}</b><br>
              <span style="color:#666;font-size:11px">${s.address||''}</span><br><br>
              <span style="background:${corPin};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">${statusLabel}</span>
              <span style="margin-left:8px;font-size:11px">ETA: <b>${s.eta||'—'}</b></span><br>
              <span style="font-size:11px;color:#666">Peso: ${(s.weight_kg||0).toFixed(0)} kg</span>
            </div>`
          });
          marker.addListener('click', () => {
            // Fecha outros infowindows
            if (window.tcActiveIW) window.tcActiveIW.close();
            iw.open(tcMap, marker);
            window.tcActiveIW = iw;
          });
          tcMarkers.push(marker);
        }
      });'''

content = content.replace(old_markers, new_markers)

# Adiciona lista de sequencia no card de cada rota
old_card_stops = '''        const card = document.createElement(\'div\');
        card.style.cssText = `border:2px solid ${cor}30;border-radius:8px;padding:10px;margin-bottom:8px;cursor:pointer`;
        card.onclick = () => tcFocarRota(r, stopsLatLng);
        card.innerHTML = `
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
          <span style="background:${cor};color:#fff;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>
          <span style="font-size:11px;color:var(--muted)">${statusRota}</span>
        </div>
        <div style="display:flex;gap:8px;font-size:11px;margin-bottom:8px;flex-wrap:wrap">
          <span>&#x1F4CD; ${stops.length} paradas</span>
          <span>&#x1F6E3;&#xFE0F; ${r.total_distance_km||0} km</span>
          <span>&#x1F550; ${r.planned_start||\'07:30\'}</span>
        </div>
        <!-- Barra de progresso -->
        <div style="margin-bottom:4px">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-bottom:3px">
            <span>Progresso</span>
            <span>${completadas}/${stops.length} (${pctConcluido}%)</span>
          </div>
          <div style="background:#e5e7eb;border-radius:4px;height:6px;overflow:hidden">
            <div style="width:${pctConcluido}%;height:100%;background:${pctConcluido===100?\'#16a34a\':cor};border-radius:4px;transition:width .3s"></div>
          </div>
        </div>
        <div style="display:flex;gap:6px;font-size:10px;margin-top:6px">
          <span style="background:#f0fdf4;color:#16a34a;padding:2px 6px;border-radius:3px">&#x2705; ${completadas}</span>
          <span style="background:#fff7ed;color:#d97706;padding:2px 6px;border-radius:3px">&#x1F550; ${pendentes}</span>
          ${atrasadas > 0 ? `<span style="background:#fef2f2;color:#dc2626;padding:2px 6px;border-radius:3px">&#x26A0; ${atrasadas}</span>` : \'\'}
        </div>`;
      lista.appendChild(card);'''

new_card_stops = '''        // Monta lista de paradas sequenciada
        const stopsOrdenados = [...stops].sort((a,b) => a.sequence - b.sequence);
        const listaParadas = stopsOrdenados.map(s => {
          const corStatus = s.status === 'completed' ? '#16a34a' :
                           s.status === 'failed' ? '#dc2626' :
                           agoraMins > (()=>{const [h,m]=(s.eta||'23:59').split(':').map(Number); return h*60+m;})() + 30 ? '#dc2626' : cor;
          return `<div style="display:flex;align-items:center;gap:6px;padding:4px 0;border-bottom:1px solid #f0f0f0;cursor:pointer"
                       onclick="tcFocarPonto(${parseFloat(s.lat)||0}, ${parseFloat(s.lng)||0})">
            <span style="background:${corStatus};color:#fff;width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">${s.sequence+1}</span>
            <div style="flex:1;min-width:0">
              <div style="font-size:11px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${s.recipient_name}</div>
              <div style="font-size:10px;color:#888">${s.eta||'—'} · ${(s.weight_kg||0).toFixed(0)}kg</div>
            </div>
          </div>`;
        }).join('');

        const card = document.createElement('div');
        card.style.cssText = `border:2px solid ${cor}40;border-radius:8px;margin-bottom:8px;overflow:hidden`;
        card.innerHTML = `
        <div style="background:${cor}15;padding:10px 12px;cursor:pointer" onclick="tcFocarRota(${JSON.stringify(r)}, ${JSON.stringify(stopsLatLng)})">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
            <span style="background:${cor};color:#fff;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>
            <span style="font-size:11px;color:var(--muted)">${statusRota}</span>
          </div>
          <div style="display:flex;gap:8px;font-size:11px;flex-wrap:wrap">
            <span>&#x1F4CD; ${stops.length} paradas</span>
            <span>&#x1F6E3;&#xFE0F; ${r.total_distance_km||0} km</span>
            <span>&#x1F550; ${r.planned_start||'07:30'} → ${r.planned_end||'—'}</span>
          </div>
          <div style="margin-top:8px">
            <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-bottom:3px">
              <span>Progresso</span>
              <span>${completadas}/${stops.length} (${pctConcluido}%)</span>
            </div>
            <div style="background:#e5e7eb;border-radius:4px;height:5px;overflow:hidden">
              <div style="width:${pctConcluido}%;height:100%;background:${pctConcluido===100?'#16a34a':cor};border-radius:4px"></div>
            </div>
          </div>
        </div>
        <!-- Lista de paradas sequenciada -->
        <div style="padding:6px 10px;max-height:200px;overflow-y:auto;background:#fff">
          <div style="font-size:10px;font-weight:600;color:var(--muted);margin-bottom:4px">SEQUENCIA DE ENTREGAS:</div>
          ${listaParadas}
        </div>`;
      lista.appendChild(card);'''

content = content.replace(old_card_stops, new_card_stops)

# Adiciona funcao tcFocarPonto
new_func = '''
function tcFocarPonto(lat, lng) {
  if (!tcMap || !lat || !lng) return;
  tcMap.setCenter({lat, lng});
  tcMap.setZoom(16);
}
'''

last_script = content.rfind('</script>')
if last_script != -1:
    content = content[:last_script] + new_func + '\n' + content[last_script:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Torre de Controle atualizada com:')
print('  Pins numerados no mapa (1, 2, 3...)')
print('  Lista lateral com sequencia de entregas')
print('  Clique no cliente para focar no mapa')
print('Faca Ctrl+Shift+R no navegador!')
