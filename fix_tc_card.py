path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui o bloco do card da rota na Torre de Controle
# Localiza o inicio e fim do card
marker_start = '<span style="background:${cor};color:#fff;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>'

if marker_start not in content:
    print('Marcador nao encontrado!')
    exit(1)

# Encontra a posicao do inicio do card (procura "const card = " antes do marcador)
pos = content.find(marker_start)
card_start = content.rfind('const card = document.createElement', 0, pos)
# Encontra o fim do card (lista.appendChild)
card_end = content.find('lista.appendChild(card);', pos) + len('lista.appendChild(card);')

old_card = content[card_start:card_end]
print(f'Card encontrado: {len(old_card)} chars')

new_card = """const card = document.createElement('div');
        card.style.cssText = 'border:2px solid ' + cor + '40;border-radius:8px;margin-bottom:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06)';

        // Lista de paradas sequenciada
        const stopsOrdenados = [...stops].sort((a,b) => (a.sequence||0)-(b.sequence||0));
        const listaHTML = stopsOrdenados.map(s => {
          const lat = parseFloat(s.lat)||0, lng = parseFloat(s.lng)||0;
          let bg = cor, statusTxt = 'Pendente';
          if (s.status === 'completed') { bg = '#16a34a'; statusTxt = 'Entregue'; }
          else if (s.status === 'failed') { bg = '#dc2626'; statusTxt = 'Falhou'; }
          else if (s.eta) {
            const [h,m] = s.eta.split(':').map(Number);
            if (agoraMins > h*60+m+30) { bg = '#dc2626'; statusTxt = 'Atrasado'; }
            else statusTxt = 'Em rota';
          }
          return `<div onclick="tcFocarPonto(${lat},${lng})" style="display:flex;align-items:center;gap:7px;padding:6px 10px;border-bottom:1px solid #f0f0f0;cursor:pointer">
            <span style="background:${bg};color:#fff;min-width:20px;height:20px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">${(s.sequence||0)+1}</span>
            <div style="flex:1;min-width:0">
              <div style="font-size:11px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${s.recipient_name||''}</div>
              <div style="font-size:10px;color:#888">${s.eta||'--:--'} &middot; ${(s.weight_kg||0).toFixed(0)}kg &middot; <span style="color:${bg}">${statusTxt}</span></div>
            </div>
          </div>`;
        }).join('');

        card.innerHTML = `
          <div style="background:${cor}18;padding:10px 14px;cursor:pointer" onclick="tcFocarRota(null,${JSON.stringify(stopsLatLng)})">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap">
              <span style="background:${cor};color:#fff;padding:3px 12px;border-radius:5px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>
              <span style="font-size:11px;color:var(--muted)">${statusRota}</span>
              <span style="margin-left:auto;font-size:11px;color:var(--muted)">${r.planned_start||'07:30'} → ${r.planned_end||'--:--'}</span>
            </div>
            <div style="display:flex;gap:10px;font-size:11px;margin-bottom:7px;flex-wrap:wrap">
              <span>📍 ${stops.length} paradas</span>
              <span>🛣️ ${r.total_distance_km||0} km</span>
              <span style="color:#16a34a">✅ ${completadas}</span>
              <span style="color:#d97706">⏳ ${pendentes}</span>
              ${atrasadas > 0 ? '<span style="color:#dc2626">⚠️ ' + atrasadas + '</span>' : ''}
            </div>
            <div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-bottom:3px">
                <span>Progresso</span><span>${completadas}/${stops.length} (${pctConcluido}%)</span>
              </div>
              <div style="background:#e5e7eb;border-radius:4px;height:5px;overflow:hidden">
                <div style="width:${pctConcluido}%;height:100%;background:${pctConcluido===100?'#16a34a':cor};border-radius:4px"></div>
              </div>
            </div>
          </div>
          <div>
            <div style="padding:4px 10px;font-size:10px;font-weight:700;color:var(--muted);background:#f8fafc;border-top:1px solid ${cor}20;letter-spacing:.5px">
              SEQUÊNCIA DE ENTREGAS
            </div>
            <div style="max-height:200px;overflow-y:auto">${listaHTML}</div>
          </div>`;
        lista.appendChild(card);"""

content = content[:card_start] + new_card + content[card_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Card da Torre de Controle reescrito!')
print('Faca Ctrl+Shift+R no navegador.')
