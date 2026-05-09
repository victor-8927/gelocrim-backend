import re

HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

NOVO_MOTOR = r'''
function atualizarEtaConf() {
  // ── Jornada real ─────────────────────────────────────────
  var INICIO_MIN   = 8 * 60;          // 08:00
  var ALMOCO_MIN   = 12 * 60;         // 12:00
  var ALMOCO_DUR   = 72;              // 1h12min
  var FIM_NORMAL   = 18 * 60;         // 18:00
  var FIM_BANCO    = 20 * 60;         // 20:00 (banco de horas)
  var VEL_MEDIA    = 35;              // km/h medio urbano Manaus

  var minutos = INICIO_MIN;
  var almocoFeito = false;
  var prev = {lat: -3.093544, lng: -60.075812};

  confOrdem.forEach(function(o, i) {
    // Distancia real entre paradas (graus -> km aproximado)
    var dlat = (parseFloat(o.lat)||prev.lat) - prev.lat;
    var dlng = (parseFloat(o.lng)||prev.lng) - prev.lng;
    var distKm = Math.sqrt(dlat*dlat + dlng*dlng) * 111;
    var tempoViagem = Math.round(distKm / VEL_MEDIA * 60);

    // Tempo de atendimento real do cliente
    var tempoAtend = parseInt(o.tempo_entrega || 20);

    // Inserir almoco se ainda nao foi e vai passar das 12:00
    if (!almocoFeito && (minutos + tempoViagem) >= ALMOCO_MIN) {
      minutos = ALMOCO_MIN + ALMOCO_DUR;
      almocoFeito = true;
    }

    minutos += tempoViagem + tempoAtend;
    prev = o;

    // Formatar ETA
    var h = Math.floor(minutos / 60) % 24;
    var m = minutos % 60;
    o._eta = String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0');
    o._minutos = minutos;
    o._distKm = distKm.toFixed(1);
    o._tempoAtend = tempoAtend;

    // Classificar status da jornada
    if (minutos <= FIM_NORMAL) {
      o._jornada = 'normal';
      o._jornadaCor = '#00FF88';
    } else if (minutos <= FIM_BANCO) {
      o._jornada = 'banco';
      o._jornadaCor = '#FFD700';
    } else {
      o._jornada = 'extra';
      o._jornadaCor = '#FF3355';
    }
  });

  // Retorno ao deposito
  var ultimo = confOrdem[confOrdem.length - 1];
  var distRetorno = 0;
  if (ultimo && ultimo.lat && ultimo.lng) {
    var dlat2 = -3.093544 - parseFloat(ultimo.lat);
    var dlng2 = -60.075812 - parseFloat(ultimo.lng);
    distRetorno = Math.sqrt(dlat2*dlat2 + dlng2*dlng2) * 111;
  }
  var minRetorno = minutos + Math.round(distRetorno / VEL_MEDIA * 60);

  // Distancia total
  var distTotal = confOrdem.reduce(function(s, o){ return s + parseFloat(o._distKm||0); }, 0) + distRetorno;

  // Atualizar UI
  var fimEl = document.getElementById('conf-hora-fim');
  if (fimEl && confOrdem.length) {
    var hR = Math.floor(minRetorno/60)%24;
    var mR = minRetorno%60;
    var horaRetorno = String(hR).padStart(2,'0')+':'+String(mR).padStart(2,'0');
    var cor = minRetorno <= FIM_NORMAL*60 ? '#00FF88' : minRetorno <= FIM_BANCO*60 ? '#FFD700' : '#FF3355';
    fimEl.textContent = horaRetorno;
    fimEl.style.color = cor;
  }

  // Atualizar distancia
  var distEl = document.getElementById('conf-distancia');
  if (distEl) distEl.textContent = distTotal.toFixed(0) + ' km (real)';

  // Alerta de jornada
  var alertaEl = document.getElementById('conf-alerta-jornada');
  if (alertaEl) {
    var extras = confOrdem.filter(function(o){ return o._jornada === 'extra'; }).length;
    var banco  = confOrdem.filter(function(o){ return o._jornada === 'banco'; }).length;
    if (extras > 0) {
      alertaEl.textContent = '⚠️ ' + extras + ' paradas em hora extra! Revisar rota.';
      alertaEl.style.color = '#FF3355';
      alertaEl.style.display = 'block';
    } else if (banco > 0) {
      alertaEl.textContent = '🕐 ' + banco + ' paradas em banco de horas (até 20:00)';
      alertaEl.style.color = '#FFD700';
      alertaEl.style.display = 'block';
    } else {
      alertaEl.textContent = '✅ Rota dentro da jornada normal (até 18:00)';
      alertaEl.style.color = '#00FF88';
      alertaEl.style.display = 'block';
    }
  }

  // Calcular custo combustivel
  var veiculo = window._confVeiculoSel;
  if (veiculo && veiculo.km_per_liter && veiculo.fuel_price) {
    var litros = distTotal / parseFloat(veiculo.km_per_liter);
    var custo  = litros * parseFloat(veiculo.fuel_price);
    var custoCombEl = document.getElementById('conf-custo-comb');
    if (custoCombEl) custoCombEl.textContent = 'R$ ' + custo.toFixed(2);
  }

  // Rerenderizar lista com novos ETAs e cores
  renderizarListaConf();
}

function reprocessarSequencia() {
  var modo = document.getElementById('conf-sequencia') ? document.getElementById('conf-sequencia').value : 'otimizado';
  var deposito = {lat: -3.093544, lng: -60.075812};

  var comGPS = confOrdem.filter(function(o){ return parseFloat(o.lat) && parseFloat(o.lng); });
  var semGPS = confOrdem.filter(function(o){ return !parseFloat(o.lat) || !parseFloat(o.lng); });

  if (modo === 'otimizado') {
    var nn = nearestNeighbor(comGPS, deposito);
    comGPS = otimizar2opt(nn, deposito);
    toast('✅ Rota otimizada com 2-opt!', 'success');

  } else if (modo === 'proximidade') {
    comGPS = nearestNeighbor(comGPS, deposito);
    toast('✅ Sequência por proximidade aplicada!', 'success');

  } else if (modo === 'distancia') {
    comGPS = otimizar2opt(comGPS, deposito);
    toast('✅ Menor distância calculada!', 'success');

  } else if (modo === 'agrupamento') {
    // Agrupar por regiao/bairro e dentro de cada grupo otimizar
    var grupos = {};
    comGPS.forEach(function(o){
      var chave = o.regiao || o.bairro || 'SEM_REGIAO';
      if (!grupos[chave]) grupos[chave] = [];
      grupos[chave].push(o);
    });
    // Ordenar grupos por proximidade ao deposito
    var chavesOrdenadas = Object.keys(grupos).sort(function(a, b){
      var centroA = grupos[a].reduce(function(s,o){return {lat:s.lat+parseFloat(o.lat)/grupos[a].length, lng:s.lng+parseFloat(o.lng)/grupos[a].length};}, {lat:0,lng:0});
      var centroB = grupos[b].reduce(function(s,o){return {lat:s.lat+parseFloat(o.lat)/grupos[b].length, lng:s.lng+parseFloat(o.lng)/grupos[b].length};}, {lat:0,lng:0});
      return distLatLng(deposito, centroA) - distLatLng(deposito, centroB);
    });
    comGPS = [];
    chavesOrdenadas.forEach(function(chave){
      var grupo = nearestNeighbor(grupos[chave], deposito);
      comGPS = comGPS.concat(grupo);
    });
    toast('✅ Agrupado por região e otimizado internamente!', 'success');
  }

  confOrdem = comGPS.concat(semGPS);
  atualizarEtaConf();

  var km = (distanciaTotal(comGPS, deposito) * 111).toFixed(0);
  setTimeout(function(){ toast('📍 Distância estimada: ~' + km + ' km', 'info'); }, 800);
}
'''

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir as duas funcoes atualizarEtaConf e reprocessarSequencia
padrao = r'function atualizarEtaConf\(\).*?(?=async function atualizarRotaMapa)'

novo = re.sub(padrao, NOVO_MOTOR + '\n', content, flags=re.DOTALL)

if novo == content:
    print("❌ Padrão não encontrado! Verificar manualmente.")
else:
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(novo)
    print("✅ Motor de planejamento atualizado com sucesso!")
    print("   - Jornada: 08:00 às 18:00")
    print("   - Almoço: 12:00 por 1h12min")
    print("   - Banco de horas: até 20:00")
    print("   - T.Atend real por cliente")
    print("   - Custo combustível calculado")
    print("   - Alertas de hora extra")
