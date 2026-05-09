path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Adiciona pallets no passo 2 após as barras de peso/volume ──
old_barras = '''          <div id="rot-cap-info" style="display:none;margin-top:8px;display:none">
            <div style="margin-bottom:6px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">⚖️ Peso</span><span id="rot-peso-txt" style="font-weight:600;color:#e8f0fe">0 kg</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-peso" style="height:100%;background:#e8521a;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <div>
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">📦 Volume</span><span id="rot-vol-txt" style="font-weight:600;color:#e8f0fe">0 m³</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:8px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
          </div>'''

new_barras = '''          <div id="rot-cap-info" style="display:none;margin-top:8px">
            <div style="margin-bottom:6px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">⚖️ Peso</span><span id="rot-peso-txt" style="font-weight:600;color:#e8f0fe">0 kg</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:6px;overflow:hidden">
                <div id="rot-barra-peso" style="height:100%;background:#e8521a;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <div style="margin-bottom:6px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">📦 Volume</span><span id="rot-vol-txt" style="font-weight:600;color:#e8f0fe">0 m³</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:6px;overflow:hidden">
                <div id="rot-barra-vol" style="height:100%;background:#2563eb;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
            </div>
            <div style="border-top:1px solid #1e3a5c;padding-top:8px;margin-top:4px">
              <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px">
                <span style="color:#90afd4">🪵 Pallets na carga</span><span id="rot-pallets-txt" style="font-weight:600;color:#a78bfa">— pallets</span>
              </div>
              <div style="background:#1e3a5c;border-radius:4px;height:6px;overflow:hidden">
                <div id="rot-barra-pallets" style="height:100%;background:#a78bfa;border-radius:4px;transition:width .3s;width:0%"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:#90afd4;margin-top:4px">
                <span>Cap. veículo</span><span id="rot-cap-pallets-txt">— pallets</span>
              </div>
            </div>
          </div>'''

if old_barras in content:
    content = content.replace(old_barras, new_barras)
    print('Pallets adicionados no Passo 2!')
else:
    print('ERRO: padrão barras não encontrado')
    # Busca alternativa
    idx = content.find('rot-barra-vol')
    if idx != -1:
        print(content[max(0,idx-200):idx+200])

# ── 2. Atualiza rotVeiculoChanged para incluir pallets ─────────────
old_veiculo_changed = 'function rotVeiculoChanged() {'
idx = content.find(old_veiculo_changed)
if idx != -1:
    depth = 0; started = False; i = idx
    for i in range(idx, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break
    old_func = content[idx:i+1]
    new_func = '''function rotVeiculoChanged() {
  const sel  = document.getElementById('rot-veiculo-select');
  const opt  = sel?.options[sel?.selectedIndex];
  if (!opt?.value) return;
  rotVeiculo = {
    id:          opt.value,
    plate:       opt.dataset?.plate  || opt.text,
    model:       opt.dataset?.model  || '',
    capacity_kg: parseFloat(opt.dataset?.kg || 0),
    capacity_m3: parseFloat(opt.dataset?.m3 || 0),
    pallets:     parseInt(opt.dataset?.pallets || 0),
  };
  const capInfo = document.getElementById('rot-cap-info');
  if (capInfo) capInfo.style.display = 'block';

  // Atualiza capacidade de pallets
  const capPallets = document.getElementById('rot-cap-pallets-txt');
  if (capPallets) capPallets.textContent = rotVeiculo.pallets > 0 ? `${rotVeiculo.pallets} pallets` : '— pallets (configurar no cadastro)';

  rotAtualizarBarras();
}'''
    content = content[:idx] + new_func + content[i+1:]
    print('rotVeiculoChanged atualizado com pallets!')

# ── 3. Atualiza rotAtualizarBarras para incluir pallets ────────────
old_barras_func = 'function rotAtualizarBarras() {'
idx2 = content.find(old_barras_func)
if idx2 != -1:
    depth = 0; started = False; i = idx2
    for i in range(idx2, len(content)):
        if content[i] == '{': depth += 1; started = True
        elif content[i] == '}': depth -= 1
        if started and depth == 0: break
    new_barras_func = '''function rotAtualizarBarras() {
  if (!rotVeiculo) return;
  const peso   = rotGetPesoTotal();
  const vol    = rotGetVolTotal();
  const capKg  = rotVeiculo.capacity_kg || 1;
  const capM3  = rotVeiculo.capacity_m3 || 1;
  const capPal = rotVeiculo.pallets || 0;

  // Calcula pallets necessários baseado no peso médio por pallet
  const pesoMedioPallet = 900; // kg por pallet carregado (estimativa)
  const palletsNecessarios = Math.ceil(peso / pesoMedioPallet);

  const pctPeso = Math.min(100, Math.round(peso/capKg*100));
  const pctVol  = Math.min(100, Math.round(vol/capM3*100));
  const pctPal  = capPal > 0 ? Math.min(100, Math.round(palletsNecessarios/capPal*100)) : 0;

  const corPeso = pctPeso>90?'#f87171':pctPeso>70?'#f59e0b':'#e8521a';
  const corVol  = pctVol>90?'#f87171':pctVol>70?'#f59e0b':'#2563eb';
  const corPal  = pctPal>90?'#f87171':pctPal>70?'#f59e0b':'#a78bfa';

  const bp = document.getElementById('rot-barra-peso');
  const bv = document.getElementById('rot-barra-vol');
  const bpl= document.getElementById('rot-barra-pallets');
  if (bp)  { bp.style.width=pctPeso+'%'; bp.style.background=corPeso; }
  if (bv)  { bv.style.width=pctVol+'%';  bv.style.background=corVol; }
  if (bpl) { bpl.style.width=pctPal+'%'; bpl.style.background=corPal; }

  const tp = document.getElementById('rot-peso-txt');
  const tv = document.getElementById('rot-vol-txt');
  const tpl= document.getElementById('rot-pallets-txt');
  if (tp)  tp.textContent  = `${peso.toFixed(0)}kg / ${capKg}kg (${pctPeso}%)`;
  if (tv)  tv.textContent  = `${vol.toFixed(2)}m³ / ${capM3}m³ (${pctVol}%)`;
  if (tpl) tpl.textContent = `${palletsNecessarios} / ${capPal||'—'} pallets`;
}'''
    content = content[:idx2] + new_barras_func + content[i+1:]
    print('rotAtualizarBarras atualizado com pallets!')

# ── 4. Atualiza select de veículos para incluir campo pallets ──────
old_sel_veic = '''      sel.innerHTML += `<option value="${v.id}" data-kg="${v.capacity_kg}" data-m3="${v.capacity_m3}" data-plate="${v.plate}" data-model="${v.model}">
        ${v.plate} — ${v.model} (${v.capacity_kg}kg / ${v.capacity_m3}m3)
      </option>`;'''

new_sel_veic = '''      sel.innerHTML += `<option value="${v.id}" data-kg="${v.capacity_kg}" data-m3="${v.capacity_m3}" data-plate="${v.plate}" data-model="${v.model}" data-pallets="${v.pallets||0}">
        ${v.vda||v.plate} — ${v.model} (${v.capacity_kg}kg / ${v.capacity_m3}m³ / ${v.pallets||0} pallets)
      </option>`;'''

if old_sel_veic in content:
    content = content.replace(old_sel_veic, new_sel_veic)
    print('Select de veículos atualizado com pallets!')

# ── 5. Corrige popup do mapa na conferência com informações reais ──
old_popup = '''      const info = new google.maps.InfoWindow({
        content: `<b>${i+1}. ${o.recipient_name}</b><br>Peso: ${o.weight_kg||0}kg`
      });
      marker.addListener('click', () => info.open(confMap, marker));'''

new_popup = '''      const infoContent = `
        <div style="font-family:Arial,sans-serif;padding:4px;min-width:200px">
          <div style="font-weight:700;font-size:13px;margin-bottom:6px;color:#0a1628">
            ${i+1}. ${o.recipient_name}
          </div>
          <div style="font-size:11px;color:#444;margin-bottom:4px">📍 ${o.address||'Endereço não informado'}</div>
          <div style="display:flex;gap:12px;font-size:11px;margin-bottom:4px">
            <span>⚖️ <b>${o.weight_kg||0} kg</b></span>
            <span>📦 <b>${o.volume_m3||0} m³</b></span>
          </div>
          <div style="font-size:11px;color:#444;margin-bottom:4px">
            🕐 Janela: <b>${o.time_window_start||'—'} - ${o.time_window_end||'—'}</b>
          </div>
          <div style="font-size:11px;color:#444">
            💰 Valor: <b>${o.total_value ? 'R$ '+parseFloat(o.total_value).toFixed(2) : 'Não informado'}</b>
          </div>
          <div style="font-size:10px;color:#888;margin-top:4px">Pedido: ${o.external_id||'—'}</div>
        </div>`;
      const info = new google.maps.InfoWindow({ content: infoContent });
      marker.addListener('click', () => info.open(confMap, marker));'''

if old_popup in content:
    content = content.replace(old_popup, new_popup)
    print('Popup do mapa corrigido com informações completas!')
else:
    print('ERRO: popup não encontrado')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nPronto! Faca Ctrl+Shift+R.')
