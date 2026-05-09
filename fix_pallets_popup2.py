path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Adiciona pallets após rot-barra-vol ────────────────────────
old_vol_end = '''              <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>'''

new_vol_end = '''              <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <!-- Pallets -->
            <div style="border-top:1px solid #1e3a5c;padding-top:8px;margin-top:6px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">🪵 Pallets</span><span id="rot-pallets-txt" style="font-weight:600;color:#a78bfa">—</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:6px;overflow:hidden">
                <div id="rot-barra-pallets" style="height:100%;background:#a78bfa;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
              <div style="font-size:10px;color:#90afd4;margin-top:3px">Cap. veículo: <span id="rot-cap-pallets-txt">—</span></div>
            </div>
          </div>
        </div>
      </div>'''

if old_vol_end in content:
    content = content.replace(old_vol_end, new_vol_end)
    print('Pallets adicionados no Passo 2!')
else:
    print('ERRO vol: buscando variação...')
    idx = content.find('rot-barra-vol')
    print(repr(content[idx:idx+300]))

# ── 2. Corrige popup do mapa da conferência ────────────────────────
# Busca o padrão exato atual
idx_popup = content.find("content: `<b>${i+1}. ${o.recipient_name}</b>")
if idx_popup != -1:
    # Pega a linha completa
    start = content.rfind('\n', 0, idx_popup) + 1
    end   = content.find('\n', idx_popup + 200) + 1
    old_info = content[start:end]
    print(f'Popup encontrado: {repr(old_info[:100])}')

    new_info = '''      const infoContent = `<div style="font-family:Arial,sans-serif;padding:4px;min-width:180px"><b style="font-size:13px">${i+1}. ${o.recipient_name}</b><br><span style="font-size:11px;color:#555">📍 ${o.address||'—'}</span><br><span style="font-size:11px">⚖️ ${o.weight_kg||0}kg &nbsp; 📦 ${o.volume_m3||0}m³</span><br><span style="font-size:11px">🕐 ${o.time_window_start||'—'} - ${o.time_window_end||'—'}</span><br><span style="font-size:10px;color:#888">Pedido: ${o.external_id||'—'}</span></div>`;
      const info = new google.maps.InfoWindow({ content: infoContent });
      marker.addListener('click', () => info.open(confMap, marker));
'''
    content = content[:start] + new_info + content[end:]
    print('Popup corrigido!')
else:
    print('Popup não encontrado, buscando...')
    idx2 = content.find('InfoWindow')
    print(content[max(0,idx2-100):idx2+200])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Ctrl+Shift+R.')
