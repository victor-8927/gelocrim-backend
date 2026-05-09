path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. JS para carregar motoristas e ajudantes separados ──────────
new_js = '''
// ── FROTA (MOTORISTAS E AJUDANTES) ───────────────────────────────
let _motoristas = [];
let _ajudantes  = [];

async function carregarFrota() {
  try {
    const drivers = await api('GET', '/drivers');
    _motoristas = (drivers || []).filter(d => d.tipo === 'motorista' || !d.tipo);
    _ajudantes  = (drivers || []).filter(d => d.tipo === 'ajudante');

    // Popula seletor de motorista
    const selMot = document.getElementById('sel-motorista');
    if (selMot) {
      selMot.innerHTML = '<option value="">-- Motorista --</option>';
      _motoristas.forEach(d => {
        selMot.innerHTML += `<option value="${d.id}">${d.name}</option>`;
      });
    }

    // Popula seletores de ajudantes
    ['sel-ajudante1','sel-ajudante2'].forEach(id => {
      const sel = document.getElementById(id);
      if (sel) {
        sel.innerHTML = '<option value="">-- Nenhum --</option>';
        _ajudantes.forEach(a => {
          sel.innerHTML += `<option value="${a.id}">${a.name}</option>`;
        });
      }
    });
  } catch(e) { console.log('Erro frota:', e); }
}
'''

if 'carregarFrota' not in content:
    last_script = content.rfind('</script>')
    content = content[:last_script] + new_js + '\n' + content[last_script:]
    print('JS carregarFrota adicionado!')

# ── 2. Adiciona campos motorista e ajudantes no painel de roteirização ──
old_veiculo_label = '''<label style="font-size:12px;font-weight:600;color:var(--muted);display:block;margin-bottom:6px">VEÍCULO</label>'''

new_campos = '''<label style="font-size:12px;font-weight:600;color:var(--muted);display:block;margin-bottom:6px">VEÍCULO</label>'''

# Procura o seletor de veiculo e adiciona campos abaixo
old_sel_veiculo = '''<select id="sel-veiculo"'''
idx = content.find(old_sel_veiculo)

if idx != -1:
    # Encontra o fim do select de veiculo
    fim_sel = content.find('</select>', idx) + len('</select>')

    campos_equipe = '''
              <div style="margin-top:10px">
                <label style="font-size:12px;font-weight:600;color:var(--muted);display:block;margin-bottom:6px">MOTORISTA</label>
                <select id="sel-motorista" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:8px;font-size:13px;background:var(--bg)">
                  <option value="">-- Selecione o Motorista --</option>
                </select>
              </div>
              <div style="margin-top:10px">
                <label style="font-size:12px;font-weight:600;color:var(--muted);display:block;margin-bottom:6px">AJUDANTE 1</label>
                <select id="sel-ajudante1" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:8px;font-size:13px;background:var(--bg)">
                  <option value="">-- Nenhum --</option>
                </select>
              </div>
              <div style="margin-top:10px">
                <label style="font-size:12px;font-weight:600;color:var(--muted);display:block;margin-bottom:6px">AJUDANTE 2</label>
                <select id="sel-ajudante2" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:8px;font-size:13px;background:var(--bg)">
                  <option value="">-- Nenhum --</option>
                </select>
              </div>'''

    # Verifica se ja existe
    if 'sel-motorista' not in content[idx:idx+2000]:
        content = content[:fim_sel] + campos_equipe + content[fim_sel:]
        print('Campos motorista e ajudantes adicionados!')
    else:
        print('Campos ja existem!')

# ── 3. Chama carregarFrota ao abrir roteirizacao ──────────────────
if 'carregarFrota()' not in content:
    content = content.replace(
        "if(page==='roteirizacao')",
        "if(page==='roteirizacao') { carregarFrota(); } if(page==='_rot_x')"
    )
    print('carregarFrota chamado ao abrir roteirizacao!')

# ── 4. Passa motorista e ajudantes no payload de otimizacao ──────
old_vehicle = '"vehicle_id": veiculoId,'
new_vehicle = '''"vehicle_id": veiculoId,
        "driver_id": document.getElementById("sel-motorista")?.value || null,
        "ajudante1_id": document.getElementById("sel-ajudante1")?.value || null,
        "ajudante2_id": document.getElementById("sel-ajudante2")?.value || null,'''

if old_vehicle in content and 'driver_id' not in content[content.find(old_vehicle)-10:content.find(old_vehicle)+200]:
    content = content.replace(old_vehicle, new_vehicle)
    print('Motorista e ajudantes adicionados no payload!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nHTML atualizado! Faca Ctrl+Shift+R no navegador.')
