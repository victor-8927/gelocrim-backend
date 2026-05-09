path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Atualiza o rodapé da lista de clientes com botões de fluxo ──
old_rodape = '''          <div style="padding:8px;border-top:1px solid #1e3a5c;flex-shrink:0">
            <button onclick="reprocessarSequencia()" style="width:100%;padding:8px;background:#1e3a5c;border:none;color:#64B4FF;border-radius:6px;font-size:11px;cursor:pointer;font-weight:600">&#x1F504; Reprocessar Sequência</button>
          </div>'''

new_rodape = '''          <div style="padding:8px;border-top:1px solid #1e3a5c;flex-shrink:0;display:grid;gap:6px">
            <button onclick="reprocessarSequencia()" style="width:100%;padding:7px;background:#1e3a5c;border:none;color:#64B4FF;border-radius:6px;font-size:11px;cursor:pointer;font-weight:600">
              🔄 Reprocessar Sequência
            </button>
            <button id="btn-atualizar-rota" onclick="atualizarRotaMapa()" style="width:100%;padding:9px;background:#e8521a;border:none;color:#fff;border-radius:6px;font-size:12px;cursor:pointer;font-weight:700">
              🗺️ Atualizar Rota no Mapa
            </button>
            <button id="btn-confirmar-rota" onclick="confirmarRota()" disabled style="width:100%;padding:9px;background:#1e3a5c;border:1px solid #1e3a5c;color:#90afd4;border-radius:6px;font-size:12px;cursor:not-allowed;font-weight:700;opacity:0.5">
              ✅ Confirmar Rota
            </button>
          </div>'''

if old_rodape in content:
    content = content.replace(old_rodape, new_rodape)
    print('Rodapé com botões de fluxo adicionado!')
else:
    print('ERRO: padrão rodapé não encontrado')

# ── 2. Atualiza o botão GRAVAR para iniciar desabilitado ───────────
old_gravar = '''              <button id="btn-gravar-carga" onclick="gravarCarga()" style="padding:7px 20px;background:#10b981;border:none;color:#fff;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer">💾 GRAVAR CARGA</button>'''

new_gravar = '''              <button id="btn-gravar-carga" onclick="gravarCarga()" disabled style="padding:7px 20px;background:#1e3a5c;border:none;color:#90afd4;border-radius:6px;font-size:14px;font-weight:700;cursor:not-allowed;opacity:0.5" title="Confirme a rota antes de gravar">💾 GRAVAR CARGA</button>'''

if old_gravar in content:
    content = content.replace(old_gravar, new_gravar)
    print('Botão GRAVAR inicia desabilitado!')
else:
    # Tenta sem id
    old_gravar2 = '''              <button onclick="gravarCarga()" style="padding:7px 20px;background:#10b981;border:none;color:#fff;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer">&#x1F4BE; GRAVAR CARGA</button>'''
    new_gravar2 = '''              <button id="btn-gravar-carga" onclick="gravarCarga()" disabled style="padding:7px 20px;background:#1e3a5c;border:none;color:#90afd4;border-radius:6px;font-size:14px;font-weight:700;cursor:not-allowed;opacity:0.5" title="Confirme a rota antes de gravar">💾 GRAVAR CARGA</button>'''
    if old_gravar2 in content:
        content = content.replace(old_gravar2, new_gravar2)
        print('Botão GRAVAR (v2) inicia desabilitado!')
    else:
        print('ERRO: botão GRAVAR não encontrado')

# ── 3. Adiciona funções JS do fluxo ───────────────────────────────
new_funcs = '''
// ── FLUXO CONFERÊNCIA: Atualizar → Confirmar → Gravar ────────────
let rotaConfirmada = false;

function atualizarRotaMapa() {
  if (confOrdem.length === 0) { toast('Nenhum cliente na lista!', 'error'); return; }

  const btn = document.getElementById('btn-atualizar-rota');
  if (btn) { btn.textContent = '⏳ Atualizando...'; btn.disabled = true; }

  // Reset confirmação ao atualizar
  rotaConfirmada = false;
  const btnConf  = document.getElementById('btn-confirmar-rota');
  const btnGravar= document.getElementById('btn-gravar-carga');
  if (btnConf) {
    btnConf.disabled = true;
    btnConf.style.background = '#1e3a5c';
    btnConf.style.color = '#90afd4';
    btnConf.style.cursor = 'not-allowed';
    btnConf.style.opacity = '0.5';
    btnConf.textContent = '✅ Confirmar Rota';
  }
  if (btnGravar) {
    btnGravar.disabled = true;
    btnGravar.style.background = '#1e3a5c';
    btnGravar.style.color = '#90afd4';
    btnGravar.style.cursor = 'not-allowed';
    btnGravar.style.opacity = '0.5';
    btnGravar.title = 'Confirme a rota antes de gravar';
  }

  // Limpa mapa
  if (confMap) {
    confMap.eachLayer ? confMap.eachLayer(l => { if (l instanceof L?.Marker || l instanceof L?.Polyline) confMap.removeLayer(l); }) : null;
    if (confMap._confMarkers) confMap._confMarkers.forEach(m => m.setMap && m.setMap(null));
    if (confMap._confLine) { confMap._confLine.setMap ? confMap._confLine.setMap(null) : null; confMap._confLine = null; }
    confMap._confMarkers = [];
  }

  // Redesenha o mapa com a nova ordem
  const bounds = new google.maps.LatLngBounds();
  const coords = [];
  const deposito = {lat: -3.093544, lng: -60.075812};

  // Marcador do depósito
  new google.maps.Marker({
    position: deposito, map: confMap,
    icon: {path: google.maps.SymbolPath.CIRCLE, scale:10, fillColor:'#64B4FF', fillOpacity:1, strokeColor:'#fff', strokeWeight:2},
    title: 'Depósito Gelocrim'
  });
  bounds.extend(deposito);
  coords.push(deposito);

  // Marcadores na nova ordem
  confOrdem.forEach((o, i) => {
    const lat = parseFloat(o.lat);
    const lng = parseFloat(o.lng);
    if (!isNaN(lat) && !isNaN(lng) && Math.abs(lat) > 0.01) {
      const pos = {lat, lng};
      coords.push(pos);
      bounds.extend(pos);
      const marker = new google.maps.Marker({
        position: pos, map: confMap,
        label: {text: String(i+1), color:'#fff', fontWeight:'bold', fontSize:'11px'},
        icon: {path: google.maps.SymbolPath.CIRCLE, scale:14, fillColor:'#e8521a', fillOpacity:1, strokeColor:'#fff', strokeWeight:2},
        title: o.recipient_name
      });
      const info = new google.maps.InfoWindow({
        content: `<b>${i+1}. ${o.recipient_name}</b><br>${o.weight_kg||0}kg`
      });
      marker.addListener('click', () => info.open(confMap, marker));
      confMap._confMarkers.push(marker);
    }
  });

  coords.push(deposito);

  // Redesenha trajeto real
  if (coords.length > 2) {
    const directionsService  = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
      map: confMap, suppressMarkers: true,
      polylineOptions: {strokeColor:'#e8521a', strokeOpacity:0.9, strokeWeight:4}
    });
    confMap._confLine = directionsRenderer;

    directionsService.route({
      origin:      new google.maps.LatLng(coords[0].lat, coords[0].lng),
      destination: new google.maps.LatLng(deposito.lat, deposito.lng),
      waypoints:   coords.slice(1, coords.length-1).slice(0,23).map(c => ({location: new google.maps.LatLng(c.lat, c.lng), stopover:true})),
      travelMode:  google.maps.TravelMode.DRIVING,
      optimizeWaypoints: false
    }, (result, status) => {
      if (status === 'OK') {
        directionsRenderer.setDirections(result);
        let kmReal = 0;
        result.routes[0].legs.forEach(leg => { kmReal += leg.distance.value / 1000; });
        const el = document.getElementById('conf-distancia');
        if (el) el.textContent = kmReal.toFixed(1) + ' km (atualizado)';
        toast('Rota atualizada no mapa!', 'success');
      }
      confMap.fitBounds(bounds);
    });
  }

  // Habilita botão Confirmar
  setTimeout(() => {
    if (btn) { btn.textContent = '🗺️ Atualizar Rota no Mapa'; btn.disabled = false; }
    const btnC = document.getElementById('btn-confirmar-rota');
    if (btnC) {
      btnC.disabled = false;
      btnC.style.background = '#f59e0b';
      btnC.style.color = '#fff';
      btnC.style.cursor = 'pointer';
      btnC.style.opacity = '1';
      btnC.textContent = '✅ Confirmar Rota';
    }
  }, 1500);
}

function confirmarRota() {
  if (confOrdem.length === 0) { toast('Nenhum cliente na lista!', 'error'); return; }
  rotaConfirmada = true;

  const btnConf  = document.getElementById('btn-confirmar-rota');
  const btnGravar= document.getElementById('btn-gravar-carga');
  const btnAtual = document.getElementById('btn-atualizar-rota');

  if (btnConf) {
    btnConf.textContent = '✅ Rota Confirmada!';
    btnConf.style.background = '#10b981';
    btnConf.style.color = '#fff';
    btnConf.disabled = true;
    btnConf.style.cursor = 'default';
  }
  if (btnGravar) {
    btnGravar.disabled = false;
    btnGravar.style.background = '#10b981';
    btnGravar.style.color = '#fff';
    btnGravar.style.cursor = 'pointer';
    btnGravar.style.opacity = '1';
    btnGravar.title = '';
    btnGravar.textContent = '💾 GRAVAR CARGA';
  }
  // Bloqueia edição após confirmação
  const lista = document.getElementById('conf-lista-clientes');
  if (lista) lista.style.opacity = '0.7';
  if (btnAtual) { btnAtual.disabled = true; btnAtual.style.opacity = '0.4'; }

  toast('✅ Rota confirmada! Clique em GRAVAR CARGA para finalizar.', 'success');
}

'''

if 'function atualizarRotaMapa' not in content:
    content = content.replace('// ── FLUXO CONFERÊNCIA', '// ── PLACEHOLDER\n')
    content = content.replace('function renderizarListaConf()', new_funcs + 'function renderizarListaConf()')
    print('Funções de fluxo adicionadas!')
else:
    print('Funções já existem!')

# ── 4. Atualiza gravarCarga para verificar confirmação ─────────────
old_gravar_start = '''  const itens = Object.values(rotSelecionados || {});
  if (itens.length === 0) {
    toast('Selecione clientes no mapa primeiro', 'error');
    return;
  }'''

# Adiciona verificação de rota confirmada no gravarCarga
old_check_veiculo = '''  if (!veiculo || !motorista) {
    toast('Selecione veículo e motorista!', 'error');
    return;
  }
  // Verifica margem negativa'''

new_check_veiculo = '''  if (!veiculo || !motorista) {
    toast('Selecione veículo e motorista!', 'error');
    return;
  }
  // Verifica se rota foi confirmada
  if (!rotaConfirmada) {
    toast('Atualize e confirme a rota antes de gravar!', 'error');
    return;
  }
  // Verifica margem negativa'''

if old_check_veiculo in content:
    content = content.replace(old_check_veiculo, new_check_veiculo)
    print('gravarCarga com verificação de confirmação!')

# ── 5. Reset da confirmação ao abrir conferência ───────────────────
old_abre = "  document.getElementById('painel-conferencia').style.display = 'flex';"
new_abre = """  // Reset fluxo
  rotaConfirmada = false;
  const bG = document.getElementById('btn-gravar-carga');
  const bC = document.getElementById('btn-confirmar-rota');
  const bA = document.getElementById('btn-atualizar-rota');
  if (bG) { bG.disabled=true; bG.style.background='#1e3a5c'; bG.style.color='#90afd4'; bG.style.cursor='not-allowed'; bG.style.opacity='0.5'; bG.textContent='💾 GRAVAR CARGA'; }
  if (bC) { bC.disabled=true; bC.style.background='#1e3a5c'; bC.style.color='#90afd4'; bC.style.cursor='not-allowed'; bC.style.opacity='0.5'; bC.textContent='✅ Confirmar Rota'; }
  if (bA) { bA.disabled=false; bA.style.opacity='1'; }
  const lista = document.getElementById('conf-lista-clientes');
  if (lista) lista.style.opacity='1';
  document.getElementById('painel-conferencia').style.display = 'flex';"""

if old_abre in content:
    content = content.replace(old_abre, new_abre, 1)
    print('Reset do fluxo ao abrir conferência!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
