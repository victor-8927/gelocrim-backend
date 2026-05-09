path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corrige initMap para scroll sem Ctrl
old_map = """  const m = new google.maps.Map(el, {
    center: {lat, lng},
    zoom,
    mapTypeId: 'roadmap',"""

new_map = """  const m = new google.maps.Map(el, {
    center: {lat, lng},
    zoom,
    mapTypeId: 'roadmap',
    gestureHandling: 'greedy',"""

if old_map in content:
    content = content.replace(old_map, new_map)
    print('Scroll sem Ctrl ativado!')
else:
    print('initMap padrão não encontrado')

# 2. Substitui painel esquerdo completo — adiciona Passo 3 e melhora lista
old_painel = """<div id="rot-lista-sel" style="flex:1;overflow-y:auto;padding:8px">
          <div style="color:#90afd4;font-size:12px;text-align:center;padding:20px">
            Clique nos pins laranjos no mapa para selecionar clientes.
          </div>
        </div>
      </div>
      <button id="btn-rot-map" onclick="abrirConferenciaMaster()" disabled
        style="padding:14px;background:#e8521a;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;opacity:0.5">
        &#x26A1; Roteirizar &#x2014; Conferência Master
      </button>"""

new_painel = """<!-- PASSO 3: RESUMO -->
        <div style="background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;padding:10px;margin-bottom:8px">
          <div style="font-size:10px;font-weight:700;color:#e8521a;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px">📊 Passo 3 — Carga Estimada</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
            <div style="background:#0f2040;border-radius:6px;padding:6px;text-align:center">
              <div id="rot-total-peso" style="font-size:16px;font-weight:700;color:#f59e0b">0 kg</div>
              <div style="font-size:9px;color:#90afd4">PESO TOTAL</div>
            </div>
            <div style="background:#0f2040;border-radius:6px;padding:6px;text-align:center">
              <div id="rot-total-vol" style="font-size:16px;font-weight:700;color:#64B4FF">0 m³</div>
              <div style="font-size:9px;color:#90afd4">CUBAGEM</div>
            </div>
            <div style="background:#0f2040;border-radius:6px;padding:6px;text-align:center">
              <div id="sug-pallets" style="font-size:16px;font-weight:700;color:#a78bfa">—</div>
              <div style="font-size:9px;color:#90afd4">PALLETS EST.</div>
            </div>
            <div style="background:#0f2040;border-radius:6px;padding:6px;text-align:center">
              <div id="sug-tempo" style="font-size:16px;font-weight:700;color:#10b981">—</div>
              <div style="font-size:9px;color:#90afd4">TEMPO EST.</div>
            </div>
          </div>
        </div>
        <!-- LISTA DE CLIENTES SELECIONADOS -->
        <div style="font-size:10px;font-weight:700;color:#90afd4;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px">
          Clientes selecionados (<span id="rot-count">0</span>)
        </div>
        <div id="rot-lista-sel" style="flex:1;overflow-y:auto;max-height:200px;padding:4px;border:1px solid #1e3a5c;border-radius:6px;background:#060f1e">
          <div style="color:#90afd4;font-size:12px;text-align:center;padding:20px">
            Clique nos pins no mapa para selecionar clientes.
          </div>
        </div>
      </div>
      <button id="btn-rot-map" onclick="abrirConferenciaMaster()" disabled
        style="padding:14px;background:#e8521a;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;opacity:0.5">
        &#x26A1; Roteirizar &#x2014; Conferência Master
      </button>"""

if old_painel in content:
    content = content.replace(old_painel, new_painel)
    print('Painel com Passo 3 e lista atualizado!')
else:
    print('Painel padrão não encontrado!')

# 3. Remove rot-count duplicado que estava no HTML antigo
# (agora está dentro do novo painel)
old_count = '''\n          </div>\n          <div style="font-size:11px;color:#90afd4;text-align:center">\n            <span id="rot-count">0</span> cliente(s) selecionado(s)\n          </div>'''
if old_count in content:
    content = content.replace(old_count, '')
    print('rot-count duplicado removido!')

# 4. Melhora os pins com SVG customizado (ícone de localização)
# Substitui o icon circle por SVG path de location pin
old_icon = """        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: cor,
          fillOpacity: 0.95,
          strokeColor: '#ffffff',
          strokeWeight: 2.5,
          scale: sel ? 16 : 12
        }"""

new_icon = """        icon: {
          path: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',
          fillColor: cor,
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 1,
          scale: sel ? 2.2 : 1.7,
          anchor: new google.maps.Point(12, 22),
          rotation: 0
        }"""

if old_icon in content:
    content = content.replace(old_icon, new_icon)
    print('Pins trocados para ícone de localização!')

    # Também atualiza os setIcon inline (selecionado/deseleccionado)
    content = content.replace(
        "mk.setIcon({path:google.maps.SymbolPath.CIRCLE,fillColor:getCorRota(o.rota||o.regiao),fillOpacity:0.95,strokeColor:'#fff',strokeWeight:2.5,scale:12});",
        "mk.setIcon({path:'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',fillColor:getCorRota(o.rota||o.regiao),fillOpacity:1,strokeColor:'#fff',strokeWeight:1,scale:1.7,anchor:new google.maps.Point(12,22)});"
    )
    content = content.replace(
        "mk.setIcon({path:google.maps.SymbolPath.CIRCLE,fillColor:'#10b981',fillOpacity:0.95,strokeColor:'#fff',strokeWeight:2.5,scale:16});",
        "mk.setIcon({path:'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',fillColor:'#10b981',fillOpacity:1,strokeColor:'#fff',strokeWeight:1,scale:2.2,anchor:new google.maps.Point(12,22)});"
    )
    print('setIcon inline atualizado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('\nPronto! Ctrl+Shift+R.')
