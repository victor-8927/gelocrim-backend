path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Corrige função abrirConferenciaMaster completa ──────────────
idx_start = content.find('function abrirConferenciaMaster()')
depth = 0; start_found = False; i = idx_start
for i in range(idx_start, len(content)):
    if content[i] == '{': depth += 1; start_found = True
    elif content[i] == '}': depth -= 1
    if start_found and depth == 0: break

new_func = '''function abrirConferenciaMaster() {
  const itens = Object.values(rotSelecionados || {});
  if (itens.length === 0) { toast('Selecione clientes no mapa primeiro', 'error'); return; }

  const selecionados = itens.map(x => x.order);

  // Veículo
  const veicSelect = document.getElementById('rot-veiculo-select');
  const motSelect  = document.getElementById('sel-motorista');
  const aj1Select  = document.getElementById('sel-ajudante1');
  const aj2Select  = document.getElementById('sel-ajudante2');

  if (!veicSelect?.value) { toast('Selecione um veículo antes de roteirizar', 'error'); return; }

  const veicOpt  = veicSelect.options[veicSelect.selectedIndex];
  const veicNome = veicOpt?.text || '—';
  const capKg    = parseFloat(veicOpt?.dataset?.kg || 5000);
  const capM3    = parseFloat(veicOpt?.dataset?.m3 || 20);

  const motNome  = motSelect?.options[motSelect?.selectedIndex]?.text || '—';
  const aj1Nome  = aj1Select?.value ? aj1Select.options[aj1Select.selectedIndex].text : null;
  const aj2Nome  = aj2Select?.value ? aj2Select.options[aj2Select.selectedIndex].text : null;
  const equipeStr = [motNome, aj1Nome, aj2Nome].filter(Boolean).join(' · ');

  // Totais reais dos pedidos
  const pesoTotal = selecionados.reduce((s,o) => s + (parseFloat(o.weight_kg)||0), 0);
  const volTotal  = selecionados.reduce((s,o) => s + (parseFloat(o.volume_m3) || (parseFloat(o.weight_kg)||0)*0.002), 0);
  const fatTotal  = selecionados.reduce((s,o) => s + (parseFloat(o.total_value)||parseFloat(o.value)||0), 0);

  // Distância estimada (3km entre paradas + 15km depósito/retorno)
  const kmEst = 15 + selecionados.length * 3;

  // Custos — virão do cadastro futuramente
  const custoDia   = 0; // a configurar no cadastro de motoristas
  const custoDiesel= 0; // a configurar no cadastro de veículos
  const custoManut = 0; // a configurar no cadastro de veículos
  const custoTotal = custoDia + custoDiesel + custoManut;

  // Margem
  const lucro  = fatTotal - custoTotal;
  const margem = fatTotal > 0 ? (lucro / fatTotal * 100) : 0;

  // Previsão de fim
  const minTotal = selecionados.length * 20 + Math.round(kmEst / 40 * 60);
  const horaInicio = document.getElementById('conf-hora-inicio')?.value || '07:30';
  const [h, m] = horaInicio.split(':').map(Number);
  const fimMin = h*60 + m + minTotal;
  const fimH = Math.floor(fimMin/60).toString().padStart(2,'0');
  const fimM = Math.floor(fimMin%60).toString().padStart(2,'0');

  // Abre o painel
  document.getElementById('painel-conferencia').style.display = 'flex';
  if (!document.getElementById('conf-data-saida').value)
    document.getElementById('conf-data-saida').value = new Date().toISOString().slice(0,10);

  const el = (id, val) => { const e = document.getElementById(id); if(e) e.textContent = val; };

  el('conf-subtitulo',  `${selecionados.length} clientes · ${pesoTotal.toFixed(0)}kg · ${motNome}`);
  el('conf-veiculo',    veicNome);
  el('conf-motorista',  equipeStr);
  el('conf-capacidade', capKg.toLocaleString('pt-BR') + ' kg / ' + capM3 + ' m³');
  el('conf-peso',       pesoTotal.toFixed(1) + ' kg (' + Math.round(pesoTotal/capKg*100) + '% cap.)');
  el('conf-entregas',   selecionados.length + ' paradas · ' + selecionados.filter(o=>o.lat&&o.lng).length + ' com GPS');
  el('conf-distancia',  kmEst + ' km estimados');
  el('conf-hora-fim',   fimH + ':' + fimM);

  // Financeiro
  if (fatTotal > 0) {
    el('conf-top1000', 'R$ ' + fatTotal.toFixed(2));
    el('conf-top1009', '—');
    el('conf-top1007', '—');
    el('conf-top1010', '—');
    el('conf-top1008', '—');
    el('conf-total-pedidos', 'R$ ' + fatTotal.toFixed(2));
  } else {
    el('conf-top1000', 'Integrar Sankhya');
    el('conf-top1009', '—'); el('conf-top1007', '—');
    el('conf-top1010', '—'); el('conf-top1008', '—');
    el('conf-total-pedidos', '⚠️ Sem valor cadastrado');
  }

  el('conf-custo-equipe', custoDia > 0 ? 'R$ '+custoDia.toFixed(2) : '⚙️ Configurar no cadastro');
  el('conf-custo-diesel',  custoDiesel > 0 ? 'R$ '+custoDiesel.toFixed(2) : '⚙️ Configurar no veículo');
  el('conf-custo-manut',   custoManut > 0 ? 'R$ '+custoManut.toFixed(2) : '⚙️ Configurar no veículo');
  el('conf-custo-total',   custoTotal > 0 ? 'R$ '+custoTotal.toFixed(2) : '⚙️ Preencher cadastros');

  // Semáforo
  const emoji = fatTotal === 0 ? '⚠️' : margem >= 20 ? '🟢' : margem >= 10 ? '🟡' : '🔴';
  const cor   = fatTotal === 0 ? '#f59e0b' : margem >= 20 ? '#10b981' : margem >= 10 ? '#f59e0b' : '#f87171';
  const bg    = fatTotal === 0 ? 'rgba(245,158,11,.15)' : margem >= 20 ? 'rgba(16,185,129,.15)' : margem >= 10 ? 'rgba(245,158,11,.15)' : 'rgba(248,113,113,.15)';
  el('conf-semaforo-emoji', emoji);
  el('conf-margem-valor', fatTotal > 0 ? margem.toFixed(1)+'%' : '—');
  el('conf-margem-label', fatTotal > 0 ? 'Margem Operacional' : 'Complete os cadastros para calcular');
  const sem = document.getElementById('conf-semaforo');
  if (sem) { sem.style.background = bg; sem.style.borderColor = cor; }
  const mv = document.getElementById('conf-margem-valor');
  if (mv) mv.style.color = cor;

  // Lista drag & drop
  confOrdem = [...selecionados];
  renderizarListaConf();

  // Mapa de verificação
  setTimeout(() => {
    const mapEl = document.getElementById('conf-mapa');
    if (!mapEl) return;

    if (!confMap) {
      confMap = L.map('conf-mapa').setView([-3.093544, -60.075812], 12);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OSM', maxZoom: 18
      }).addTo(confMap);
    } else {
      // Limpa camadas anteriores
      confMap.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
          confMap.removeLayer(layer);
        }
      });
    }

    const coords = [];

    // Marcador do depósito
    L.marker([-3.093544, -60.075812], {
      icon: L.divIcon({
        className: '',
        html: '<div style="background:#0a1628;color:#64B4FF;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;border:2px solid #64B4FF;box-shadow:0 2px 6px rgba(0,0,0,.4)">🏭</div>',
        iconSize: [28,28], iconAnchor: [14,14]
      })
    }).addTo(confMap).bindPopup('<b>Depósito Gelocrim</b>');
    coords.push([-3.093544, -60.075812]);

    // Marcadores dos clientes
    confOrdem.forEach((o, i) => {
      if (o.lat && o.lng && Math.abs(parseFloat(o.lat)) > 0.01) {
        const lat = parseFloat(o.lat);
        const lng = parseFloat(o.lng);
        coords.push([lat, lng]);
        L.marker([lat, lng], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#e8521a;color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4)">${i+1}</div>`,
            iconSize: [26,26], iconAnchor: [13,13]
          })
        }).addTo(confMap).bindPopup(`<b>${i+1}. ${o.recipient_name}</b><br>Peso: ${o.weight_kg||0}kg`);
      }
    });

    // Volta ao depósito
    if (coords.length > 1) coords.push([-3.093544, -60.075812]);

    // Desenha polyline do trajeto
    if (coords.length > 2) {
      L.polyline(coords, {color:'#64B4FF', weight:3, opacity:.85, dashArray:'8,4'}).addTo(confMap);
      const bounds = L.latLngBounds(coords);
      confMap.fitBounds(bounds, {padding:[30,30]});
    } else if (coords.length === 2) {
      confMap.setView(coords[1], 13);
    }

    // Invalida tamanho para forçar renderização correta
    setTimeout(() => confMap.invalidateSize(), 100);
  }, 300);
}'''

content = content[:idx_start] + new_func + content[i+1:]
print('abrirConferenciaMaster corrigida!')

# ── 2. Adiciona campo total_value no formulário de pedido ──────────
old_notes = '''notes: document.getElementById('o-notes').value||null,'''
new_notes = '''total_value: +document.getElementById('o-value').value||0,
      notes: document.getElementById('o-notes').value||null,'''

if old_notes in content:
    content = content.replace(old_notes, new_notes)
    print('Campo total_value adicionado no saveOrder!')

# Adiciona o campo no modal de pedido
old_modal_kg = '''<label class="form-label">Peso (kg)</label>
              <input class="form-control" id="o-kg" type="number" step="0.1" placeholder="0.0">'''
new_modal_kg = '''<label class="form-label">Peso (kg)</label>
              <input class="form-control" id="o-kg" type="number" step="0.1" placeholder="0.0">'''

# Busca onde está o campo de notas no modal de pedido
idx_notes_modal = content.find('id="o-notes"')
if idx_notes_modal != -1:
    # Insere campo valor antes das notas
    old_notes_field = content[max(0,idx_notes_modal-150):idx_notes_modal+100]
    print('\nCampo notas encontrado, verificando contexto...')
    # Adiciona campo valor logo antes do textarea de notas
    old_textarea = '<label class="form-label">Observações</label>'
    new_textarea = '''<label class="form-label">Valor do Pedido (R$)</label>
              <input class="form-control" id="o-value" type="number" step="0.01" placeholder="0.00" style="margin-bottom:12px">
              <label class="form-label">Observações</label>'''
    if old_textarea in content:
        content = content.replace(old_textarea, new_textarea)
        print('Campo valor adicionado no modal de pedido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
