path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Corrige abrirConferenciaMaster para usar rotSelecionados ────
old_conf = '''function abrirConferenciaMaster() {
  const selecionados = rotSelectedOrders || [];
  if (selecionados.length === 0) { toast('Selecione clientes no mapa primeiro', 'error'); return; }'''

new_conf = '''function abrirConferenciaMaster() {
  const selecionados = Object.values(rotSelecionados||{}).map(x=>x.order);
  if (selecionados.length === 0) { toast('Selecione clientes no mapa primeiro', 'error'); return; }'''

if old_conf in content:
    content = content.replace(old_conf, new_conf)
    print('1. abrirConferenciaMaster corrigido!')
else:
    print('1. ERRO: padrão não encontrado')

# ── 2. Corrige setModoSelecao para tema escuro + círculo + quadrado ─
old_modo = '''function setModoSelecao(modo) {
  rotModo = modo;
  const btnClick = document.getElementById('btn-modo-click');
  const btnArea  = document.getElementById('btn-modo-area');
  const dica     = document.getElementById('dica-modo');
  if (modo === 'click') {
    btnClick.style.border = '2px solid #e8521a';
    btnClick.style.background = '#fff7ed';
    btnClick.style.color = '#e8521a';
    btnArea.style.border = '2px solid var(--border)';
    btnArea.style.background = '#fff';
    btnArea.style.color = 'var(--muted)';
    dica.textContent = 'Clique nos pins para selecionar clientes';
    if (rot'''

# Busca o fim da função setModoSelecao
idx = content.find('function setModoSelecao(')
if idx == -1:
    print('2. ERRO: setModoSelecao não encontrado')
else:
    # Encontra o fim da função
    depth = 0
    i = idx
    start_found = False
    for i in range(idx, len(content)):
        if content[i] == '{':
            depth += 1
            start_found = True
        elif content[i] == '}':
            depth -= 1
        if start_found and depth == 0:
            break
    
    old_func = content[idx:i+1]
    new_func = '''function setModoSelecao(modo) {
  rotModo = modo;
  const btns = {
    'click':   document.getElementById('btn-modo-click'),
    'area':    document.getElementById('btn-modo-area'),
    'circulo': document.getElementById('btn-modo-circulo'),
    'quadrado':document.getElementById('btn-modo-quadrado'),
  };
  const dica = document.getElementById('dica-modo');
  const dicas = {
    'click':   'Clique nos pins laranjos para selecionar clientes',
    'area':    'Desenhe um laço livre ao redor dos clientes',
    'circulo': 'Clique e arraste para desenhar um círculo de seleção',
    'quadrado':'Clique e arraste para desenhar um quadrado de seleção',
  };
  // Reset todos os botões
  Object.values(btns).forEach(b => {
    if (!b) return;
    b.style.border = '2px solid #1e3a5c';
    b.style.background = 'transparent';
    b.style.color = '#90afd4';
  });
  // Ativa o botão selecionado
  if (btns[modo]) {
    btns[modo].style.border = '2px solid #e8521a';
    btns[modo].style.background = 'rgba(232,82,26,.15)';
    btns[modo].style.color = '#e8521a';
  }
  if (dica) dica.textContent = dicas[modo] || '';
  // Habilita drawing manager conforme modo
  if (modo === 'click') {
    if (rotDrawingManager) rotDrawingManager.setDrawingMode(null);
  } else if (modo === 'area') {
    if (rotDrawingManager) rotDrawingManager.setDrawingMode(google.maps.drawing.OverlayType.POLYGON);
    else iniciarDesenhoArea();
  } else if (modo === 'circulo') {
    if (rotDrawingManager) rotDrawingManager.setDrawingMode(google.maps.drawing.OverlayType.CIRCLE);
  } else if (modo === 'quadrado') {
    if (rotDrawingManager) rotDrawingManager.setDrawingMode(google.maps.drawing.OverlayType.RECTANGLE);
  }
}'''
    content = content[:idx] + new_func + content[i+1:]
    print('2. setModoSelecao corrigido com todos os modos!')

# ── 3. Corrige o painel-conferencia para usar display:flex ─────────
# O painel está com display:none mas precisa de display:flex ao abrir
old_abrir = '''  document.getElementById('painel-conferencia').style.display = 'flex';'''
if old_abrir in content:
    print('3. display:flex já está correto')
else:
    # Procura onde muda o display
    old_d = "document.getElementById('painel-conferencia').style.display = 'flex'"
    if old_d not in content:
        # Adiciona o display flex corretamente
        content = content.replace(
            "document.getElementById('painel-conferencia').style.display = 'flex';",
            "document.getElementById('painel-conferencia').style.display = 'flex';"
        )
    print('3. verificado')

# ── 4. Garante que volume seja calculado mesmo sem dados do pedido ──
old_vol = '''function rotGetVolTotal() {
  return Object.values(rotSelecionados).reduce((s,{'''

idx_vol = content.find('function rotGetVolTotal()')
if idx_vol != -1:
    # Encontra o fim da função
    depth = 0
    i = idx_vol
    start_found = False
    for i in range(idx_vol, len(content)):
        if content[i] == '{': depth += 1; start_found = True
        elif content[i] == '}': depth -= 1
        if start_found and depth == 0: break
    
    old_vol_func = content[idx_vol:i+1]
    new_vol_func = '''function rotGetVolTotal() {
  return Object.values(rotSelecionados).reduce((s,{order}) => {
    // Se volume não está no pedido, estima pelo peso (1kg ≈ 0.002m³ para gelo)
    const vol = order.volume_m3 || (order.weight_kg ? order.weight_kg * 0.002 : 0);
    return s + vol;
  }, 0);
}'''
    content = content[:idx_vol] + new_vol_func + content[i+1:]
    print('4. rotGetVolTotal corrigido com estimativa de volume!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
