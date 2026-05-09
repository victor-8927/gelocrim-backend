path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Injeta CSS para pins numerados
css_inject = '''
<style>
.tc-seq-badge {
  display:inline-flex;align-items:center;justify-content:center;
  width:22px;height:22px;border-radius:50%;
  font-size:11px;font-weight:700;color:#fff;flex-shrink:0;
}
.tc-stop-item {
  display:flex;align-items:center;gap:6px;padding:5px 8px;
  border-bottom:1px solid #f0f0f0;cursor:pointer;
  transition:background .15s;
}
.tc-stop-item:hover { background:#f8fafc; }
</style>
'''

# Adiciona CSS antes do </head>
if '</head>' in content and 'tc-seq-badge' not in content:
    content = content.replace('</head>', css_inject + '</head>')
    print('CSS adicionado!')

# Substitui a funcao tcFocarRota para aceitar objeto
old_focar = '''function tcFocarRota(rota, pontos) {
  if (!tcMap || !pontos.length) return;
  const bounds = new google.maps.LatLngBounds();
  pontos.forEach(p => bounds.extend(p));
  tcMap.fitBounds(bounds);
}'''

new_focar = '''function tcFocarRota(rota, pontos) {
  if (!tcMap) return;
  try {
    const pts = typeof pontos === 'string' ? JSON.parse(pontos) : pontos;
    if (!pts || !pts.length) return;
    const bounds = new google.maps.LatLngBounds();
    pts.forEach(p => { if(p && p.lat && p.lng) bounds.extend({lat:parseFloat(p.lat),lng:parseFloat(p.lng)}); });
    tcMap.fitBounds(bounds);
  } catch(e) { console.warn('tcFocarRota erro:', e); }
}

function tcFocarPonto(lat, lng) {
  if (!tcMap || !lat || !lng) return;
  tcMap.panTo({lat: parseFloat(lat), lng: parseFloat(lng)});
  tcMap.setZoom(16);
}'''

if 'tcFocarPonto' not in content:
    content = content.replace(old_focar, new_focar)
    print('tcFocarRota/tcFocarPonto atualizados!')

# Adiciona JS para lista de sequencia na Torre de Controle
new_js = '''
// ── LISTA DE SEQUENCIA NA TORRE ───────────────────────────────────
function tcRenderListaParadas(stops, cor, routeId) {
  if (!stops || !stops.length) return '<div style="color:var(--muted);font-size:11px;padding:8px">Sem paradas</div>';

  const sorted = [...stops].sort((a,b) => (a.sequence||0) - (b.sequence||0));
  const agora = new Date();
  const agoraMins = agora.getHours()*60 + agora.getMinutes();

  return sorted.map(s => {
    let corBadge = cor;
    let statusTxt = 'Pendente';
    if (s.status === 'completed') { corBadge = '#16a34a'; statusTxt = 'Entregue'; }
    else if (s.status === 'failed') { corBadge = '#dc2626'; statusTxt = 'Falhou'; }
    else if (s.eta) {
      const [h,m] = s.eta.split(':').map(Number);
      if (agoraMins > h*60+m+30) { corBadge = '#dc2626'; statusTxt = 'Atrasado'; }
      else { statusTxt = 'Em rota'; }
    }

    const lat = parseFloat(s.lat)||0;
    const lng = parseFloat(s.lng)||0;

    return `<div class="tc-stop-item" onclick="tcFocarPonto(${lat},${lng})">
      <span class="tc-seq-badge" style="background:${corBadge}">${(s.sequence||0)+1}</span>
      <div style="flex:1;min-width:0">
        <div style="font-size:11px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${s.recipient_name||'Cliente'}</div>
        <div style="font-size:10px;color:#888">${s.eta||'--:--'} &middot; ${(s.weight_kg||0).toFixed(0)}kg &middot; <span style="color:${corBadge}">${statusTxt}</span></div>
      </div>
    </div>`;
  }).join('');
}
'''

# Injeta antes do ultimo </script>
last_script = content.rfind('</script>')
if last_script != -1 and 'tcRenderListaParadas' not in content:
    content = content[:last_script] + new_js + '\n' + content[last_script:]
    print('tcRenderListaParadas injetado!')

# Agora substitui o card da rota para incluir lista de paradas
# Procura o padrao do card na Torre de Controle
old_card_simple = "card.style.cssText = `border:2px solid ${cor}30;border-radius:8px;padding:10px;margin-bottom:8px;cursor:pointer`;"

new_card_full = """card.style.cssText = `border:2px solid ${cor}40;border-radius:8px;margin-bottom:8px;overflow:hidden`;"""

if old_card_simple in content:
    content = content.replace(old_card_simple, new_card_full)
    print('Card style atualizado!')

# Substitui o innerHTML do card para incluir lista
old_inner = """card.onclick = () => tcFocarRota(r, stopsLatLng);
        card.innerHTML = `
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
          <span style="background:${cor};color:#fff;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>
          <span style="font-size:11px;color:var(--muted)">${statusRota}</span>
        </div>
        <div style="display:flex;gap:8px;font-size:11px;margin-bottom:8px;flex-wrap:wrap">
          <span>&#x1F4CD; ${stops.length} paradas</span>
          <span>&#x1F6E3;&#xFE0F; ${r.total_distance_km||0} km</span>
          <span>&#x1F550; ${r.planned_start||'07:30'}</span>
        </div>
        <!-- Barra de progresso -->
        <div style="margin-bottom:4px">
          <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-bottom:3px">
            <span>Progresso</span>
            <span>${completadas}/${stops.length} (${pctConcluido}%)</span>
          </div>
          <div style="background:#e5e7eb;border-radius:4px;height:6px;overflow:hidden">
            <div style="width:${pctConcluido}%;height:100%;background:${pctConcluido===100?'#16a34a':cor};border-radius:4px;transition:width .3s"></div>
          </div>
        </div>
        <div style="display:flex;gap:6px;font-size:10px;margin-top:6px">
          <span style="background:#f0fdf4;color:#16a34a;padding:2px 6px;border-radius:3px">&#x2705; ${completadas}</span>
          <span style="background:#fff7ed;color:#d97706;padding:2px 6px;border-radius:3px">&#x1F550; ${pendentes}</span>
          ${atrasadas > 0 ? `<span style="background:#fef2f2;color:#dc2626;padding:2px 6px;border-radius:3px">&#x26A0; ${atrasadas}</span>` : ''}
        </div>`;"""

new_inner = """card.innerHTML = `
        <div style="background:${cor}15;padding:10px 12px;cursor:pointer" onclick="tcFocarRota(null, ${JSON.stringify(stopsLatLng)})">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
            <span style="background:${cor};color:#fff;padding:2px 10px;border-radius:4px;font-size:12px;font-weight:700">${r.vehicle_plate}</span>
            <span style="font-size:11px;color:var(--muted)">${statusRota}</span>
          </div>
          <div style="display:flex;gap:8px;font-size:11px;flex-wrap:wrap;margin-bottom:6px">
            <span>&#x1F4CD; ${stops.length} paradas</span>
            <span>&#x1F6E3;&#xFE0F; ${r.total_distance_km||0} km</span>
            <span>&#x1F550; ${r.planned_start||'07:30'}</span>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--muted);margin-bottom:3px">
              <span>Progresso</span>
              <span>${completadas}/${stops.length} (${pctConcluido}%)</span>
            </div>
            <div style="background:#e5e7eb;border-radius:4px;height:5px;overflow:hidden">
              <div style="width:${pctConcluido}%;height:100%;background:${pctConcluido===100?'#16a34a':cor};border-radius:4px"></div>
            </div>
          </div>
        </div>
        <div style="background:#fff;border-top:1px solid ${cor}20">
          <div style="padding:5px 10px;font-size:10px;font-weight:600;color:var(--muted);background:#f8fafc">
            SEQUENCIA DE ENTREGAS
          </div>
          <div style="max-height:180px;overflow-y:auto">
            ${tcRenderListaParadas(stops, cor, '${r.route_id}')}
          </div>
        </div>`;"""

if old_inner in content:
    content = content.replace(old_inner, new_inner)
    print('Card da rota atualizado com lista de sequencia!')
else:
    print('Padrao do card nao encontrado - verificando alternativa...')
    # Tenta encontrar pelo innerHTML
    if "card.innerHTML = `" in content and "SEQUENCIA DE ENTREGAS" not in content:
        print('Card ja tem estrutura diferente')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nAtualizado! Faca Ctrl+Shift+R no navegador.')
