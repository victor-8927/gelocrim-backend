HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Corrigir abrirConferenciaMaster para usar dados reais do veiculo
OLD_CUSTO = """  const custoDia   = 0; // a configurar no cadastro de motoristas
  const custoDiesel= 0; // a configurar no cadastro de veículos
  const custoManut = 0; // a configurar no cadastro de veículos"""

NEW_CUSTO = """  // Buscar dados reais do veiculo selecionado
  const veicId = veicSelect?.value;
  const veicData = (window._veiculosCache||[]).find(function(v){ return v.id === veicId; }) || {};
  window._confVeiculoSel = veicData;

  const kmPerLiter  = parseFloat(veicData.km_per_liter || 4);
  const fuelPrice   = parseFloat(veicData.fuel_price || 6.50);
  const custoManut  = parseFloat(veicData.manut_mes || 0) / 22; // por dia
  const ipvaDia     = parseFloat(veicData.ipva_anual || 0) / 365;

  // Custo equipe (motorista + ajudantes)
  const motId = motSelect?.value;
  const motData = (window._driversCache||[]).find(function(d){ return d.id === motId; }) || {};
  const custoDia = parseFloat(motData.daily_cost || 0);

  // Diesel estimado pela distancia
  const custoDiesel = (kmEst / kmPerLiter) * fuelPrice;
  const custoTotal = custoDia + custoDiesel + custoManut + ipvaDia;"""

# 2. Adicionar alerta de jornada após conf-hora-fim
OLD_HORA_FIM = """  el('conf-hora-fim',   fimH + ':' + fimM);"""
NEW_HORA_FIM = """  el('conf-hora-fim',   fimH + ':' + fimM);

  // Alerta de jornada inicial
  var alertaEl = document.getElementById('conf-alerta-jornada');
  if (alertaEl) {
    var fimMinTotal = fimMin;
    if (fimMinTotal <= 18*60) {
      alertaEl.textContent = '✅ Previsão dentro da jornada normal (até 18:00)';
      alertaEl.style.color = '#00FF88';
    } else if (fimMinTotal <= 20*60) {
      alertaEl.textContent = '🕐 Previsão em banco de horas (até 20:00)';
      alertaEl.style.color = '#FFD700';
    } else {
      alertaEl.textContent = '⚠️ Previsão em hora extra! Revisar rota.';
      alertaEl.style.color = '#FF3355';
    }
    alertaEl.style.display = 'block';
  }"""

# 3. Adicionar elemento HTML do alerta após o campo de hora fim no painel
OLD_PANEL = """id="conf-hora-fim\""""
# Nao editar HTML estrutural aqui, apenas o JS

changes = 0

if OLD_CUSTO in content:
    content = content.replace(OLD_CUSTO, NEW_CUSTO)
    changes += 1
    print("✅ Custos reais do veículo/motorista integrados")
else:
    print("⚠️ Bloco de custos não encontrado - verificar manualmente")

if OLD_HORA_FIM in content:
    content = content.replace(OLD_HORA_FIM, NEW_HORA_FIM)
    changes += 1
    print("✅ Alerta de jornada adicionado")
else:
    print("⚠️ Bloco hora-fim não encontrado - verificar manualmente")

# 4. Corrigir hora inicio de 07:30 para 08:00 no HTML
content = content.replace("value='07:30'", "value='08:00'")
content = content.replace('value="07:30"', 'value="08:00"')
content = content.replace("|| '07:30'", "|| '08:00'")
content = content.replace('|| "07:30"', '|| "08:00"')
print("✅ Hora início corrigida para 08:00")

# 5. Salvar veiculo no cache quando carrega frota
OLD_FROTA = "async function carregarFrota(){"
NEW_FROTA = """async function carregarFrota(){
  // Salvar cache de veiculos para uso no motor de planejamento
  try {
    var vData = await api('GET', '/vehicles');
    window._veiculosCache = vData;
  } catch(e) {}"""

if OLD_FROTA in content:
    content = content.replace(OLD_FROTA, NEW_FROTA, 1)
    changes += 1
    print("✅ Cache de veículos para motor de planejamento")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {changes} correções aplicadas com sucesso!")
print("   Recarregue o dashboard no navegador (Ctrl+Shift+R)")
