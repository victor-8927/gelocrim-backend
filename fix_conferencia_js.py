path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_js = '''
// ── CONFERÊNCIA MASTER ────────────────────────────────────────────
let confMap = null;
let confOrdem = [];

function abrirConferenciaMaster() {
  const selecionados = rotSelectedOrders || [];
  if (selecionados.length === 0) { toast('Selecione clientes no mapa primeiro', 'error'); return; }

  const veiculo   = document.getElementById('rot-veiculo-select');
  const motorista = document.getElementById('sel-motorista');
  const aj1       = document.getElementById('sel-ajudante1');
  const aj2       = document.getElementById('sel-ajudante2');

  if (!veiculo?.value) { toast('Selecione um veículo antes de roteirizar', 'error'); return; }

  // Exibe o painel
  document.getElementById('painel-conferencia').style.display = 'flex';

  // Data padrão = hoje
  const hoje = new Date().toISOString().slice(0,10);
  document.getElementById('conf-data-saida').value = hoje;

  // Dados do veículo
  const veicOpt = veiculo.options[veiculo.selectedIndex];
  const capKg   = parseFloat(veicOpt?.dataset?.capKg || 5000);
  const kmL     = parseFloat(veicOpt?.dataset?.kmL || 4);
  const manutDia = parseFloat(veicOpt?.dataset?.manut || 50);

  // Equipe
  const motNome = motorista?.options[motorista?.selectedIndex]?.text || '—';
  const aj1Nome = aj1?.value ? aj1.options[aj1.selectedIndex].text : '—';
  const aj2Nome = aj2?.value ? aj2.options[aj2.selectedIndex].text : '—';
  const custoDia = 310 + (aj1?.value ? 220 : 0) + (aj2?.value ? 220 : 0);

  // Peso e volume totais
  const pesoTotal = selecionados.reduce((s,o) => s + (o.weight_kg||0), 0);
  const volTotal  = selecionados.reduce((s,o) => s + (o.volume_m3||0), 0);

  // Distância estimada (média 3km entre pontos)
  const kmEst = selecionados.length * 3;
  const custoDiesel = (kmEst / kmL) * 6.50;
  const custoManut  = manutDia;
  const custoTotal  = custoDia + custoDiesel + custoManut;

  // Faturamento estimado (virá do Sankhya)
  const fatEst = pesoTotal * 8; // R$8/kg estimado
  const lucro  = fatEst - custoTotal;
  const margem = fatEst > 0 ? (lucro / fatEst * 100) : 0;

  // Previsão de fim (20min por parada)
  const minTotal = selecionados.length * 20 + (kmEst / 40 * 60);
  const horaInicio = document.getElementById('conf-hora-inicio').value || '07:30';
  const [h, m] = horaInicio.split(':').map(Number);
  const fimMin = h * 60 + m + minTotal;
  const fimH   = Math.floor(fimMin / 60).toString().padStart(2,'0');
  const fimM   = Math.floor(fimMin % 60).toString().padStart(2,'0');

  // Preenche indicadores
  const el = (id, val) => { const e = document.getElementById(id); if(e) e.textContent = val; };
  el('conf-veiculo',      veicOpt?.text || '—');
  el('conf-motorista',    motNome);
  el('conf-capacidade',   capKg + ' kg');
  el('conf-peso',         pesoTotal.toFixed(0) + ' kg');
  el('conf-entregas',     selecionados.length + ' paradas');
  el('conf-distancia',    kmEst.toFixed(0) + ' km estimados');
  el('conf-hora-fim',     fimH + ':' + fimM);
  el('conf-custo-equipe', 'R$ ' + custoDia.toFixed(2));
  el('conf-custo-diesel', 'R$ ' + custoDiesel.toFixed(2));
  el('conf-custo-manut',  'R$ ' + custoManut.toFixed(2));
  el('conf-custo-total',  'R$ ' + custoTotal.toFixed(2));
  el('conf-top1000', 'Integração Sankhya');
  el('conf-top1007', '—');
  el('conf-top1008', '—');
  el('conf-top1009', '—');
  el('conf-top1010', '—');
  el('conf-total-pedidos', 'R$ ' + fatEst.toFixed(2) + ' est.');
  el('conf-subtitulo', `${selecionados.length} clientes · ${pesoTotal.toFixed(0)}kg · ${motNome}`);

  // Semáforo de margem
  const sem = document.getElementById('conf-semaforo');
  const emoji = margem >= 20 ? '🟢' : margem >= 10 ? '🟡' : '🔴';
  const cor   = margem >= 20 ? '#10b981' : margem >= 10 ? '#f59e0b' : '#f87171';
  el('conf-semaforo-emoji', emoji);
  el('conf-margem-valor', margem.toFixed(1) + '%');
  el('conf-margem-label', 'Margem Operacional Estimada');
  if (sem) sem.style.background = margem >= 20 ? 'rgba(16,185,129,.15)' : margem >= 10 ? 'rgba(245,158,11,.15)' : 'rgba(248,113,113,.15)';
  document.getElementById('conf-margem-valor').style.color = cor;

  // Lista de clientes com drag & drop
  confOrdem = [...selecionados];
  renderizarListaConf();

  // Mapa de verificação
  setTimeout(() => {
    if (!confMap) {
      confMap = initMap('conf-mapa');
    }
    // Desenha polyline da rota
    const coords = confOrdem.filter(o => o.lat && o.lng).map(o => [o.lat, o.lng]);
    if (confMap._confLine) confMap.removeLayer(confMap._confLine);
    if (coords.length > 1) {
      confMap._confLine = L.polyline(coords, {color:'#64B4FF', weight:3, opacity:.8}).addTo(confMap);
      confMap.fitBounds(confMap._confLine.getBounds(), {padding:[20,20]});
    }
    confOrdem.forEach((o, i) => {
      if (o.lat && o.lng) {
        L.marker([o.lat, o.lng], {icon: L.divIcon({
          className:'',
          html:`<div style="background:#e8521a;color:#fff;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,.3)">${i+1}</div>`,
          iconSize:[22,22], iconAnchor:[11,11]
        })}).addTo(confMap).bindPopup(`<b>${i+1}. ${o.recipient_name}</b>`);
      }
    });
  }, 300);
}

function renderizarListaConf() {
  const lista = document.getElementById('conf-lista-clientes');
  if (!lista) return;
  lista.innerHTML = confOrdem.map((o, i) => `
    <div draggable="true" ondragstart="confDragStart(event,${i})" ondragover="confDragOver(event)" ondrop="confDrop(event,${i})"
      style="background:#0f2040;border:1px solid #1e3a5c;border-radius:6px;padding:8px 10px;margin-bottom:4px;cursor:grab;display:flex;align-items:center;gap:8px">
      <span style="font-size:11px;font-weight:700;color:#64B4FF;min-width:18px">${i+1}</span>
      <div style="flex:1;overflow:hidden">
        <div style="font-size:12px;font-weight:600;color:#e8f0fe;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${o.recipient_name}</div>
        <div style="font-size:10px;color:#90afd4">${o.weight_kg||0}kg${o.lat ? '' : ' · ⚠️ Sem GPS'}</div>
      </div>
      <button onclick="removerDaConf(${i})" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:12px;padding:0">✕</button>
    </div>`).join('');
}

let _confDragIdx = null;
function confDragStart(e, i) { _confDragIdx = i; }
function confDragOver(e) { e.preventDefault(); }
function confDrop(e, i) {
  e.preventDefault();
  if (_confDragIdx === null || _confDragIdx === i) return;
  const item = confOrdem.splice(_confDragIdx, 1)[0];
  confOrdem.splice(i, 0, item);
  _confDragIdx = null;
  renderizarListaConf();
}

function removerDaConf(i) {
  confOrdem.splice(i, 1);
  renderizarListaConf();
}

function inverterOrdemConf() {
  confOrdem.reverse();
  renderizarListaConf();
  toast('Ordem invertida!', 'success');
}

function reprocessarSequencia() {
  toast('Reprocessando sequência...', 'info');
  // Ordena por latitude (norte para sul)
  confOrdem.sort((a,b) => (b.lat||0) - (a.lat||0));
  renderizarListaConf();
  toast('Sequência reprocessada!', 'success');
}

function fecharConferencia() {
  document.getElementById('painel-conferencia').style.display = 'none';
}

async function gravarCarga() {
  const btn = event.target;
  btn.disabled = true;
  btn.textContent = '⏳ Gravando...';

  try {
    const veiculo   = document.getElementById('rot-veiculo-select').value;
    const motorista = document.getElementById('sel-motorista').value;
    const aj1       = document.getElementById('sel-ajudante1').value;
    const aj2       = document.getElementById('sel-ajudante2').value;
    const dataSaida = document.getElementById('conf-data-saida').value;

    if (!veiculo || !motorista) {
      toast('Selecione veículo e motorista!', 'error');
      return;
    }

    const body = {
      vehicle_id:    veiculo,
      driver_id:     motorista,
      ajudante1_id:  aj1 || null,
      ajudante2_id:  aj2 || null,
      route_date:    dataSaida,
      order_ids:     confOrdem.map(o => o.id),
      planned_start: document.getElementById('conf-hora-inicio').value
    };

    const result = await api('POST', '/routes/optimize', body);
    toast(`✅ Carga gravada! Viagem #${result.route_id || '—'} gerada.`, 'success');
    fecharConferencia();
    rotLimparTudo();
    loadRotMapData();

  } catch(e) {
    toast('Erro ao gravar: ' + e.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = '💾 GRAVAR CARGA';
  }
}

'''

if 'function abrirConferenciaMaster' not in content:
    content = content.replace('// ── ORDERS ──', new_js + '// ── ORDERS ──')
    print('Funções da Conferência Master adicionadas!')
else:
    print('Funções já existem!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
