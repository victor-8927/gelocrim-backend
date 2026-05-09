path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = '''
async function salvarVeiculoCompleto() {
  const editId = document.getElementById('modal-veiculo-completo').dataset.editId;
  const ipva   = parseFloat(document.getElementById('v-ipva').value||0);
  const manut  = parseFloat(document.getElementById('v-manut').value||0);
  const body = {
    vda:          document.getElementById('v-vda').value,
    plate:        document.getElementById('v-plate').value,
    model:        document.getElementById('v-model').value,
    type:         document.getElementById('v-type').value,
    status:       document.getElementById('v-status').value,
    capacity_kg:  parseFloat(document.getElementById('v-kg').value)||0,
    capacity_m3:  parseFloat(document.getElementById('v-m3').value)||0,
    pallets:      parseInt(document.getElementById('v-pallets').value)||0,
    bau_comp:     parseFloat(document.getElementById('v-comp').value)||0,
    bau_larg:     parseFloat(document.getElementById('v-larg').value)||0,
    bau_alt:      parseFloat(document.getElementById('v-alt').value)||0,
    fuel_type:    document.getElementById('v-combustivel').value,
    km_per_liter: parseFloat(document.getElementById('v-kml').value)||4,
    fuel_price:   parseFloat(document.getElementById('v-preco-comb').value)||6.50,
    ipva_anual:   ipva,
    manut_mes:    manut,
    daily_cost:   parseFloat(((ipva/365)+(manut/30)).toFixed(2)),
    oleo_ult_data:  document.getElementById('v-ult-oleo').value||null,
    oleo_prox_data: document.getElementById('v-prox-oleo').value||null,
    oleo_custo:     parseFloat(document.getElementById('v-custo-oleo').value)||0,
  };
  if (!body.vda)   { toast('VDA é obrigatório!', 'error'); return; }
  if (!body.plate) { toast('Placa é obrigatória!', 'error'); return; }
  if (!body.model) { toast('Modelo é obrigatório!', 'error'); return; }
  try {
    if (editId) {
      await api('PATCH', `/vehicles/${editId}`, body);
      toast('Veículo atualizado!', 'success');
    } else {
      await api('POST', '/vehicles', body);
      toast('Veículo cadastrado!', 'success');
    }
    document.getElementById('modal-veiculo-completo').style.display = 'none';
    loadVehicles();
  } catch(e) { toast(e.message, 'error'); }
}

'''

# Injeta antes de loadVehicles ou em VEHICLES
if 'function salvarVeiculoCompleto' not in content:
    if '// ── VEHICLES ──' in content:
        content = content.replace('// ── VEHICLES ──', '// ── VEHICLES ──\n' + new_func)
        print('salvarVeiculoCompleto adicionada!')
    else:
        # Adiciona antes de loadVehicles
        content = content.replace('async function loadVehicles()', new_func + 'async function loadVehicles()')
        print('salvarVeiculoCompleto adicionada antes de loadVehicles!')
else:
    print('Já existe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Ctrl+Shift+R.')
