path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui a função completa abrirConferenciaMaster
idx_start = content.find('function abrirConferenciaMaster()')
if idx_start == -1:
    print('Função não encontrada!')
else:
    # Encontra o fim da função
    depth = 0
    start_found = False
    i = idx_start
    for i in range(idx_start, len(content)):
        if content[i] == '{': depth += 1; start_found = True
        elif content[i] == '}': depth -= 1
        if start_found and depth == 0: break

    new_func = '''function abrirConferenciaMaster() {
  // Pega pedidos selecionados do objeto rotSelecionados
  const itens = Object.values(rotSelecionados || {});
  if (itens.length === 0) {
    toast('Selecione clientes no mapa primeiro', 'error');
    return;
  }

  const selecionados = itens.map(x => x.order);

  // Dados do veículo
  const veicSelect  = document.getElementById('rot-veiculo-select');
  const motSelect   = document.getElementById('sel-motorista');
  const aj1Select   = document.getElementById('sel-ajudante1');
  const aj2Select   = document.getElementById('sel-ajudante2');

  if (!veicSelect?.value) {
    toast('Selecione um veículo antes de roteirizar', 'error');
    return;
  }

  const veicOpt  = veicSelect.options[veicSelect.selectedIndex];
  const veicNome = veicOpt?.text || '—';
  const capKg    = parseFloat(veicOpt?.dataset?.capKg || rotVeiculo?.capacity_kg || 5000);
  const kmL      = parseFloat(veicOpt?.dataset?.kmL   || 4);
  const manutDia = parseFloat(veicOpt?.dataset?.manut  || 50);
  const ipvaDia  = parseFloat(veicOpt?.dataset?.ipva   || 10);

  const motNome  = motSelect?.options[motSelect?.selectedIndex]?.text  || '—';
  const aj1Nome  = aj1Select?.value ? aj1Select.options[aj1Select.selectedIndex].text : null;
  const aj2Nome  = aj2Select?.value ? aj2Select.options[aj2Select.selectedIndex].text : null;

  // Custo da equipe
  const custoDia = 310 + (aj1Select?.value ? 220 : 0) + (aj2Select?.value ? 220 : 0);

  // Peso e volume totais REAIS dos pedidos selecionados
  const pesoTotal = selecionados.reduce((s,o) => s + (parseFloat(o.weight_kg)||0), 0);
  const volTotal  = selecionados.reduce((s,o) => {
    const vol = parseFloat(o.volume_m3) || (parseFloat(o.weight_kg)||0) * 0.002;
    return s + vol;
  }, 0);

  // Distância estimada: 3km entre paradas + 15km depósito
  const kmEst = 15 + (selecionados.length * 3);
  const custoDiesel = (kmEst / kmL) * 6.50;
  const custoManut  = manutDia + ipvaDia;
  const custoTotal  = custoDia + custoDiesel + custoManut;

  // Faturamento estimado pelo peso (virá do Sankhya com TOPs)
  const fatEst = pesoTotal * 8;
  const lucro  = fatEst - custoTotal;
  const margem = fatEst > 0 ? (lucro / fatEst * 100) : 0;

  // Previsão de fim: 20min por parada + tempo de deslocamento
  const minTotal   = selecionados.length * 20 + Math.round(kmEst / 40 * 60);
  const horaInicio = document.getElementById('conf-hora-inicio')?.value || '07:30';
  const [h, m]     = horaInicio.split(':').map(Number);
  const fimMin     = h * 60 + m + minTotal;
  const fimH       = Math.floor(fimMin / 60).toString().padStart(2,'0');
  const fimM       = Math.floor(fimMin % 60).toString().padStart(2,'0');

  // Exibe o painel
  document.getElementById('painel-conferencia').style.display = 'flex';

  // Data padrão = hoje
  const hoje = new Date().toISOString().slice(0,10);
  if (document.getElementById('conf-data-saida').value === '')
    document.getElementById('conf-data-saida').value = hoje;

  // Preenche todos os indicadores
  const el = (id, val) => { const e = document.getElementById(id); if(e) e.textContent = val; };

  el('conf-subtitulo',  `${selecionados.length} clientes · ${pesoTotal.toFixed(0)}kg · ${motNome}`);
  el('conf-veiculo',    veicNome);
  el('conf-motorista',  motNome + (aj1Nome ? ` · ${aj1Nome}` : '') + (aj2Nome ? ` · ${aj2Nome}` : ''));
  el('conf-capacidade', capKg.toLocaleString('pt-BR') + ' kg');
  el('conf-peso',       pesoTotal.toFixed(1) + ' kg  (' + Math.round(pesoTotal/capKg*100) + '% da cap.)');
  el('conf-entregas',   selecionados.length + ' paradas · ' + selecionados.filter(o=>o.lat&&o.lng).length + ' geolocalizadas');
  el('conf-distancia',  kmEst.toFixed(0) + ' km estimados');
  el('conf-hora-fim',   fimH + ':' + fimM);

  // Financeiro por TOP (estimativa até integração Sankhya)
  el('conf-top1000', 'R$ ' + (fatEst * 0.80).toFixed(2) + ' est.');
  el('conf-top1009', 'R$ ' + (fatEst * 0.08).toFixed(2) + ' est.');
  el('conf-top1007', 'R$ ' + (fatEst * 0.06).toFixed(2) + ' est.');
  el('conf-top1010', 'R$ ' + (fatEst * 0.04).toFixed(2) + ' est.');
  el('conf-top1008', 'R$ ' + (fatEst * 0.02).toFixed(2) + ' est.');
  el('conf-total-pedidos', 'R$ ' + fatEst.toFixed(2) + ' est.');

  // Custos
  el('conf-custo-equipe', 'R$ ' + custoDia.toFixed(2));
  el('conf-custo-diesel', 'R$ ' + custoDiesel.toFixed(2) + ' (' + (kmEst/kmL).toFixed(0) + 'L)');
  el('conf-custo-manut',  'R$ ' + custoManut.toFixed(2));
  el('conf-custo-total',  'R$ ' + custoTotal.toFixed(2));

  // Semáforo de margem
  const emoji = margem >= 20 ? '🟢' : margem >= 10 ? '🟡' : '🔴';
  const cor   = margem >= 20 ? '#10b981' : margem >= 10 ? '#f59e0b' : '#f87171';
  const bg    = margem >= 20 ? 'rgba(16,185,129,.15)' : margem >= 10 ? 'rgba(245,158,11,.15)' : 'rgba(248,113,113,.15)';
  el('conf-semaforo-emoji', emoji);
  el('conf-margem-valor',   margem.toFixed(1) + '%');
  el('conf-margem-label',   'Margem Operacional Estimada');
  const sem = document.getElementById('conf-semaforo');
  if (sem) { sem.style.background = bg; sem.style.borderColor = cor; }
  const mv = document.getElementById('conf-margem-valor');
  if (mv) mv.style.color = cor;

  // Lista de clientes com drag & drop
  confOrdem = [...selecionados];
  renderizarListaConf();

  // Mapa de verificação com os clientes selecionados
  setTimeout(() => {
    if (!confMap) confMap = initMap('conf-mapa');
    else {
      // Limpa marcadores e linha anteriores
      if (confMap._confMarkers) confMap._confMarkers.forEach(m => m.remove ? m.remove() : confMap.removeLayer(m));
      if (confMap._confLine) confMap.removeLayer(confMap._confLine);
    }
    confMap._confMarkers = [];

    const coords = [];
    confOrdem.forEach((o, i) => {
      if (o.lat && o.lng && Math.abs(o.lat) > 0.01) {
        coords.push([o.lat, o.lng]);
        const marker = L.marker([o.lat, o.lng], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#e8521a;color:#fff;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4)">${i+1}</div>`,
            iconSize: [24,24], iconAnchor: [12,12]
          })
        }).addTo(confMap);
        marker.bindPopup(`<b>${i+1}. ${o.recipient_name}</b><br>${o.weight_kg||0}kg`);
        confMap._confMarkers.push(marker);
      }
    });

    // Desenha polyline da rota
    if (coords.length > 1) {
      confMap._confLine = L.polyline(coords, {
        color: '#64B4FF', weight: 3, opacity: .8, dashArray: '6,4'
      }).addTo(confMap);
      confMap.fitBounds(confMap._confLine.getBounds(), {padding: [30,30]});
    } else if (coords.length === 1) {
      confMap.setView(coords[0], 13);
    }
  }, 400);
}'''

    content = content[:idx_start] + new_func + content[i+1:]
    print('abrirConferenciaMaster corrigido!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
