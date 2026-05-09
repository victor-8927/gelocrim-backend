HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Após calcular km real do Google Directions, calcular ETA real por parada
OLD_LEGS = """          let kmReal = 0;
          result.routes[0].legs.forEach(leg => {
            kmReal += leg.distance.value / 1000;
          });
          const el = document.getElementById('conf-distancia');"""

NEW_LEGS = """          let kmReal = 0;
          let minReal = 0;
          var legs = result.routes[0].legs;
          legs.forEach(leg => {
            kmReal += leg.distance.value / 1000;
            minReal += leg.duration.value / 60;
          });

          // Recalcular ETA real usando tempos do Google por trecho
          var INICIO_MIN = 8 * 60;
          var ALMOCO_MIN = 12 * 60;
          var ALMOCO_DUR = 72;
          var FIM_NORMAL = 18 * 60;
          var FIM_BANCO  = 20 * 60;
          var minutosAcc = INICIO_MIN;
          var almocoFeito = false;

          // legs[0] = deposito->parada1, legs[1] = parada1->parada2, ..., legs[n-1] = paradaN->deposito
          for (var li = 0; li < confOrdem.length; li++) {
            var o = confOrdem[li];
            var tDeslocSeg = legs[li] ? legs[li].duration.value : 0;
            var tDeslocMin = Math.round(tDeslocSeg / 60);
            var tAtend = parseInt(o.tempo_entrega || o._tempoAtend || 20);
            var distKmLeg = legs[li] ? (legs[li].distance.value / 1000).toFixed(1) : '--';

            // Inserir almoco automatico
            if (!almocoFeito && (minutosAcc + tDeslocMin) >= ALMOCO_MIN) {
              minutosAcc = ALMOCO_MIN + ALMOCO_DUR;
              almocoFeito = true;
            }

            minutosAcc += tDeslocMin + tAtend;

            var h = Math.floor(minutosAcc / 60) % 24;
            var m = minutosAcc % 60;
            o._eta = String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0');
            o._minutos = minutosAcc;
            o._distKm = distKmLeg;
            o._tDeslocMin = tDeslocMin;
            o._tempoAtend = tAtend;

            if (minutosAcc <= FIM_NORMAL) {
              o._jornada = 'normal'; o._jornadaCor = '#00FF88';
            } else if (minutosAcc <= FIM_BANCO) {
              o._jornada = 'banco'; o._jornadaCor = '#FFD700';
            } else {
              o._jornada = 'extra'; o._jornadaCor = '#FF3355';
            }
          }

          // Tempo de retorno ao deposito (ultimo leg)
          var legRetorno = legs[confOrdem.length];
          var tRetornoMin = legRetorno ? Math.round(legRetorno.duration.value / 60) : 15;
          var minRetorno = minutosAcc + tRetornoMin;
          var hR = Math.floor(minRetorno/60)%24;
          var mR = minRetorno%60;
          var horaRetorno = String(hR).padStart(2,'0')+':'+String(mR).padStart(2,'0');
          var corRetorno = minRetorno <= FIM_NORMAL ? '#00FF88' : minRetorno <= FIM_BANCO ? '#FFD700' : '#FF3355';

          // Atualizar previsao de fim
          var fimEl2 = document.getElementById('conf-hora-fim');
          if (fimEl2) { fimEl2.textContent = horaRetorno; fimEl2.style.color = corRetorno; }

          // Alerta de jornada
          var alertaEl2 = document.getElementById('conf-alerta-jornada');
          if (alertaEl2) {
            var extras = confOrdem.filter(function(o){ return o._jornada === 'extra'; }).length;
            var banco  = confOrdem.filter(function(o){ return o._jornada === 'banco'; }).length;
            if (extras > 0) {
              alertaEl2.textContent = '⚠️ ' + extras + ' paradas em hora extra! Revisar rota.';
              alertaEl2.style.color = '#FF3355';
            } else if (banco > 0) {
              alertaEl2.textContent = '🕐 ' + banco + ' paradas em banco de horas (até 20:00)';
              alertaEl2.style.color = '#FFD700';
            } else {
              alertaEl2.textContent = '✅ Rota dentro da jornada normal (até 18:00)';
              alertaEl2.style.color = '#00FF88';
            }
            alertaEl2.style.display = 'block';
          }

          // Atualizar lista com novos dados
          renderizarListaConf();

          // Custo combustivel real
          var veicSel = window._confVeiculoSel || {};
          var kpl = parseFloat(veicSel.km_per_liter || 4);
          var fp  = parseFloat(veicSel.fuel_price || 6.50);
          var custoCombReal = (kmReal / kpl) * fp;
          var custoCombEl2 = document.getElementById('conf-custo-diesel');
          if (custoCombEl2) custoCombEl2.textContent = 'R$ ' + custoCombReal.toFixed(2);

          // Resumo de tempo
          var totalAtend = confOrdem.reduce(function(s,o){ return s + parseInt(o._tempoAtend||20); }, 0);
          var hDeslocTotal = Math.floor(minReal/60);
          var mDeslocTotal = Math.round(minReal%60);
          toast('✅ ' + kmReal.toFixed(1) + ' km reais · ' + hDeslocTotal + 'h' + String(mDeslocTotal).padStart(2,'0') + ' deslocamento · ' + totalAtend + ' min atendimento', 'success');

          const el = document.getElementById('conf-distancia');"""

# 2. Chamar atualizarEtaConf e renderizarListaConf ao abrir o painel
OLD_CONF_ORDEM = """  // Lista drag & drop
  confOrdem = [...selecionados];
  renderizarListaConf();"""

NEW_CONF_ORDEM = """  // Lista drag & drop
  confOrdem = [...selecionados];
  atualizarEtaConf();
  renderizarListaConf();"""

if OLD_LEGS in content:
    content = content.replace(OLD_LEGS, NEW_LEGS)
    changes += 1
    print("✅ ETA calculado com tempo real do Google Directions por trecho")
else:
    print("⚠️ Bloco legs não encontrado")

if OLD_CONF_ORDEM in content:
    content = content.replace(OLD_CONF_ORDEM, NEW_CONF_ORDEM, 1)
    changes += 1
    print("✅ atualizarEtaConf chamado ao abrir painel")
else:
    print("⚠️ Bloco confOrdem não encontrado")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {changes} correções aplicadas!")
print("   Recarregue com Ctrl+Shift+R")
print("\n   Agora o cálculo será:")
print("   08:00 + tempo real Google (45min) + T.Atend clientes + retorno = hora real de chegada")
