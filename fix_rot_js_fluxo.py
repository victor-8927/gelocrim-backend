path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a funcao rotTogglePedido para nao verificar capacidade do veiculo
old_toggle = '''function rotTogglePedido(order, marker) {
  if (rotModo !== 'click') return;
  if (rotSelecionados[order.id]) {
    // Deselecionar
    delete rotSelecionados[order.id];
    marker.setIcon(rotIcone('#e8521a'));
  } else {
    // Verificar capacidade
    if (!rotVeiculo) { toast('Selecione um veiculo primeiro!','warn'); return; }
    const totPeso = rotGetPesoTotal() + (order.weight_kg||0);
    const totVol  = rotGetVolTotal() + (order.volume_m3||0);
    if (totPeso > rotVeiculo.capKg) {
      toast(`Peso excede capacidade! (${totPeso.toFixed(0)} / ${rotVeiculo.capKg} kg)`,'warn');
      return;
    }
    rotSelecionados[order.id] = {order, marker};
    marker.setIcon(rotIcone('#16a34a', 12));
  }
  rotAtualizarSidebar();
  rotAtualizarBarras();
}'''

new_toggle = '''function rotTogglePedido(order, marker) {
  if (rotModo !== 'click') return;
  if (rotSelecionados[order.id]) {
    delete rotSelecionados[order.id];
    marker.setIcon(rotIcone('#e8521a'));
  } else {
    rotSelecionados[order.id] = {order, marker};
    marker.setIcon(rotIcone('#16a34a', 12));
  }
  rotAtualizarSidebar();
  rotAtualizarTotais();
  rotAtualizarBarras();
  // Mostra selecao de veiculo quando tiver pelo menos 1 selecionado
  const cardVei = document.getElementById('card-sel-veiculo');
  if (cardVei) cardVei.style.display = Object.keys(rotSelecionados).length > 0 ? 'block' : 'none';
}'''

content = content.replace(old_toggle, new_toggle)

# Adiciona funcao rotAtualizarTotais
new_func = '''
function rotAtualizarTotais() {
  const peso = rotGetPesoTotal();
  const vol  = rotGetVolTotal();
  const elPeso = document.getElementById('rot-total-peso');
  const elVol  = document.getElementById('rot-total-vol');
  if (elPeso) elPeso.textContent = peso.toFixed(0) + ' kg';
  if (elVol)  elVol.textContent  = vol.toFixed(2) + ' m3';
}
'''

# Injeta antes da funcao rotAtualizarBarras
content = content.replace(
    'function rotAtualizarBarras()',
    new_func + 'function rotAtualizarBarras()'
)

# Atualiza rotLimparTudo para esconder card veiculo
old_limpar = '''function rotLimparTudo() {
  Object.values(rotSelecionados).forEach(({marker}) => marker.setIcon(rotIcone('#e8521a')));
  rotSelecionados = {};
  rotAtualizarSidebar();
  rotAtualizarBarras();
}'''

new_limpar = '''function rotLimparTudo() {
  Object.values(rotSelecionados).forEach(({marker}) => { if(marker) marker.setIcon(rotIcone('#e8521a')); });
  rotSelecionados = {};
  rotVeiculo = null;
  const sel = document.getElementById('rot-veiculo-select');
  if (sel) sel.value = '';
  const cardVei = document.getElementById('card-sel-veiculo');
  if (cardVei) cardVei.style.display = 'none';
  const capInfo = document.getElementById('rot-cap-info');
  if (capInfo) capInfo.style.display = 'none';
  rotAtualizarSidebar();
  rotAtualizarTotais();
  rotAtualizarBarras();
}'''

content = content.replace(old_limpar, new_limpar)

# Atualiza rotVeiculoChanged para mostrar barras com base na selecao atual
old_veiculo = '''function rotVeiculoChanged() {
  const sel = document.getElementById('rot-veiculo-select');
  const opt = sel.options[sel.selectedIndex];
  if (!opt.value) { rotVeiculo = null; return; }
  rotVeiculo = {
    id: opt.value,
    plate: opt.dataset.plate,
    model: opt.dataset.model,
    capKg: parseFloat(opt.dataset.kg),
    capM3: parseFloat(opt.dataset.m3),
  };
  document.getElementById('rot-barras').style.display = 'block';
  document.getElementById('rot-cap-info').style.display = 'none';
  rotAtualizarBarras();
}'''

new_veiculo = '''function rotVeiculoChanged() {
  const sel = document.getElementById('rot-veiculo-select');
  const opt = sel.options[sel.selectedIndex];
  if (!opt.value) { rotVeiculo = null; return; }
  rotVeiculo = {
    id: opt.value,
    plate: opt.dataset.plate,
    model: opt.dataset.model,
    capKg: parseFloat(opt.dataset.kg),
    capM3: parseFloat(opt.dataset.m3),
  };
  const capInfo = document.getElementById('rot-cap-info');
  if (capInfo) capInfo.style.display = 'block';
  rotAtualizarBarras();
  // Habilita botao roteirizar
  const btn = document.getElementById('btn-rot-map');
  if (btn && Object.keys(rotSelecionados).length > 0) {
    btn.disabled = false;
    btn.style.opacity = '1';
  }
}'''

content = content.replace(old_veiculo, new_veiculo)

# Atualiza rotSelecionarDentroDoPoligono para nao verificar capacidade
old_poligono = '''function rotSelecionarDentroDoPoligono(polygon) {
  if (!rotVeiculo) { toast('Selecione um veiculo primeiro!','warn'); return; }
  let adicionados = 0;
  rotPedidosTodos.forEach(o => {
    if (rotSelecionados[o.id]) return;
    const lat = parseFloat(o.lat), lng = parseFloat(o.lng);
    const pt = new google.maps.LatLng(lat, lng);
    if (google.maps.geometry.poly.containsLocation(pt, polygon)) {
      const totPeso = rotGetPesoTotal() + (o.weight_kg||0);
      if (totPeso <= rotVeiculo.capKg) {
        rotSelecionados[o.id] = {order: o, marker: rotMarkers[o.id]};
        if (rotMarkers[o.id]) rotMarkers[o.id].setIcon(rotIcone('#16a34a', 12));
        adicionados++;
      }
    }
  });
  rotAtualizarSidebar();
  rotAtualizarBarras();
  toast(`${adicionados} clientes selecionados na area!`);
}'''

new_poligono = '''function rotSelecionarDentroDoPoligono(polygon) {
  let adicionados = 0;
  rotPedidosTodos.forEach(o => {
    if (rotSelecionados[o.id]) return;
    if (!o.lat || !o.lng) return;
    const lat = parseFloat(o.lat), lng = parseFloat(o.lng);
    const pt = new google.maps.LatLng(lat, lng);
    if (google.maps.geometry.poly.containsLocation(pt, polygon)) {
      rotSelecionados[o.id] = {order: o, marker: rotMarkers[o.id]};
      if (rotMarkers[o.id]) rotMarkers[o.id].setIcon(rotIcone('#16a34a', 12));
      adicionados++;
    }
  });
  rotAtualizarSidebar();
  rotAtualizarTotais();
  rotAtualizarBarras();
  const cardVei = document.getElementById('card-sel-veiculo');
  if (cardVei && adicionados > 0) cardVei.style.display = 'block';
  toast(`${adicionados} clientes selecionados na area!`);
}'''

content = content.replace(old_poligono, new_poligono)

# Atualiza rotAtualizarSidebar para mostrar botao roteirizar só após veiculo selecionado
old_sidebar_btn = '''  document.getElementById('btn-rot-map').disabled = false;
  document.getElementById('btn-rot-map').style.opacity = '1';'''

new_sidebar_btn = '''  const btnRot = document.getElementById('btn-rot-map');
  if (btnRot) {
    const habilitado = rotVeiculo !== null;
    btnRot.disabled = !habilitado;
    btnRot.style.opacity = habilitado ? '1' : '0.5';
  }'''

content = content.replace(old_sidebar_btn, new_sidebar_btn)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('JavaScript atualizado com novo fluxo!')
print('Faca Ctrl+Shift+R no navegador.')
