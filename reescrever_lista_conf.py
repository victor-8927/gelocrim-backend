HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Reescrever renderizarListaConf com detalhes completos ──
OLD_RENDER = """function renderizarListaConf() {
  var lista = document.getElementById('conf-lista-clientes');
  if (!lista) return;
  if (!confOrdem || !confOrdem.length) {
    lista.innerHTML = '<div style="padding:16px;text-align:center;color:#90afd4;font-size:11px">Nenhum cliente selecionado</div>';
    return;
  }
  lista.innerHTML = confOrdem.map(function(o, i) {
    var peso = (parseFloat(o.weight_kg)||0).toFixed(0);
    var eta  = o._eta || '\u2014';
    return '<div class="conf-item" draggable="true" data-idx="'+i+'" '+
      'ondragstart="confDragStart(event,'+i+')" '+
      'ondragover="confDragOver(event)" '+
      'ondrop="confDrop(event,'+i+')" '+
      'style="display:flex;align-items:center;gap:8px;padding:8px;margin-bottom:4px;'+
      'background:#0a1628;border:1px solid #1e3a5c;border-radius:8px;cursor:grab">'+
      '<div style="width:22px;height:22px;border-radius:50%;background:#64B4FF;color:#002855;'+
      'font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0">'+(i+1)+'</div>'+
      '<div style="flex:1;min-width:0">'+
        '<div style="font-size:11px;font-weight:700;color:#e8f0fe;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+
          (o.recipient_name||o.nome||'\u2014')+'</div>'+
        '<div style="font-size:10px;color:#90afd4">\u2696\ufe0f '+peso+' kg \xb7 \u23f1 '+eta+'</div>'+
      '</div>'+
      '<button onclick="removerDaConf('+i+')" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:14px;padding:2px 6px;flex-shrink:0">\u2715</button>'+
    '</div>';
  }).join('');
}"""

NEW_RENDER = """function renderizarListaConf() {
  var lista = document.getElementById('conf-lista-clientes');
  if (!lista) return;
  if (!confOrdem || !confOrdem.length) {
    lista.innerHTML = '<div style="padding:16px;text-align:center;color:#90afd4;font-size:11px">Nenhum cliente selecionado</div>';
    return;
  }
  lista.innerHTML = confOrdem.map(function(o, i) {
    var peso      = (parseFloat(o.weight_kg)||0).toFixed(0);
    var eta       = o._eta || '--';
    var tAtend    = o.tempo_entrega || o._tempoAtend || 20;
    var distKm    = o._distKm ? o._distKm + ' km' : '--';
    var tDeslocMin = o._tDeslocMin || '--';
    var jornadaCor = o._jornadaCor || '#64B4FF';
    var jornadaLabel = o._jornada === 'extra' ? ' ⚠️ EXTRA' : o._jornada === 'banco' ? ' 🕐 BANCO' : '';

    // Cor do card baseada na jornada
    var borderCor = o._jornada === 'extra' ? '#FF3355' : o._jornada === 'banco' ? '#FFD700' : '#1e3a5c';

    return '<div class="conf-item" draggable="true" data-idx="'+i+'" '+
      'ondragstart="confDragStart(event,'+i+')" '+
      'ondragover="confDragOver(event)" '+
      'ondrop="confDrop(event,'+i+')" '+
      'style="display:flex;align-items:flex-start;gap:8px;padding:10px;margin-bottom:6px;'+
      'background:#0a1628;border:1px solid '+borderCor+';border-left:3px solid '+jornadaCor+';border-radius:8px;cursor:grab">'+

      // Número da parada
      '<div style="width:24px;height:24px;border-radius:50%;background:'+jornadaCor+';color:#002855;'+
      'font-size:11px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px">'+(i+1)+'</div>'+

      '<div style="flex:1;min-width:0">'+
        // Nome do cliente
        '<div style="font-size:11px;font-weight:800;color:#e8f0fe;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:4px">'+
          (o.recipient_name||o.nome||'--') + jornadaLabel +
        '</div>'+

        // Linha 1: Peso + ETA chegada
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:3px">'+
          '<span style="font-size:10px;color:#90afd4;background:rgba(100,180,255,0.1);padding:1px 5px;border-radius:4px">⚖️ '+peso+' kg</span>'+
          '<span style="font-size:10px;color:'+jornadaCor+';background:rgba(100,180,255,0.1);padding:1px 5px;border-radius:4px;font-weight:700">🕐 '+eta+'</span>'+
        '</div>'+

        // Linha 2: T.Atend + Deslocamento + Distância
        '<div style="display:flex;gap:8px;flex-wrap:wrap">'+
          '<span style="font-size:10px;color:#00FFEA" title="Tempo de atendimento">⏱️ Atend: '+tAtend+' min</span>'+
          '<span style="font-size:10px;color:#90afd4" title="Tempo de deslocamento">🚛 Desloc: '+tDeslocMin+' min</span>'+
          '<span style="font-size:10px;color:#90afd4" title="Distância até esta parada">📍 '+distKm+'</span>'+
        '</div>'+
      '</div>'+

      '<button onclick="removerDaConf('+i+')" style="background:none;border:none;color:#f87171;cursor:pointer;font-size:14px;padding:2px 6px;flex-shrink:0">✕</button>'+
    '</div>';
  }).join('');
}"""

# ── 2. Reescrever atualizarEtaConf para salvar _tDeslocMin ──
OLD_ETA = "    o._distKm = distKm.toFixed(1);\n    o._tempoAtend = tempoAtend;"
NEW_ETA = "    o._distKm = distKm.toFixed(1);\n    o._tempoAtend = tempoAtend;\n    o._tDeslocMin = tempoViagem;"

# ── 3. Corrigir alerta de capacidade (120% = bloqueio, não valor fixo) ──
OLD_PESO = """  el('conf-peso',       pesoTotal.toFixed(1) + ' kg (' + Math.round(pesoTotal/capKg*100) + '% cap.)');"""
NEW_PESO = """  var pctCap = Math.round(pesoTotal/capKg*100);
  var corPeso = pctCap <= 100 ? '#00FF88' : pctCap <= 120 ? '#FFD700' : '#FF3355';
  var pesoEl = document.getElementById('conf-peso');
  if (pesoEl) {
    pesoEl.textContent = pesoTotal.toFixed(1) + ' kg (' + pctCap + '% cap.)';
    pesoEl.style.color = corPeso;
  }
  // Bloquear GRAVAR CARGA se acima de 120%
  if (pctCap > 120) {
    var bG2 = document.getElementById('btn-gravar-carga');
    if (bG2) { bG2.disabled=true; bG2.style.opacity='0.3'; bG2.title='Peso acima de 120% da capacidade!'; }
    toast('⚠️ Peso ' + pctCap + '% da capacidade — acima do limite máximo!', 'error');
  }"""

# ── 4. Corrigir distância inicial para usar Google Directions (já está no código) ──
# Garantir que kmEst seja atualizado após o cálculo real
OLD_KMINIT = "  const kmEst = 15 + selecionados.length * 3;"
NEW_KMINIT = "  var kmEst = 15 + selecionados.length * 3; // será atualizado pelo Google Directions"

changes = 0

if OLD_RENDER in content:
    content = content.replace(OLD_RENDER, NEW_RENDER)
    changes += 1
    print("✅ Lista de clientes reescrita com T.Atend, distância e tempo de deslocamento")
else:
    print("⚠️ renderizarListaConf não encontrada — verificar manualmente")

if OLD_ETA in content:
    content = content.replace(OLD_ETA, NEW_ETA)
    changes += 1
    print("✅ ETA agora salva tempo de deslocamento por parada")
else:
    print("⚠️ Bloco ETA não encontrado")

if OLD_PESO in content:
    content = content.replace(OLD_PESO, NEW_PESO)
    changes += 1
    print("✅ Alerta de capacidade por % do veículo (amarelo >100%, vermelho >120%)")
else:
    print("⚠️ Bloco peso não encontrado")

if OLD_KMINIT in content:
    content = content.replace(OLD_KMINIT, NEW_KMINIT)
    changes += 1
    print("✅ kmEst corrigido para variável atualizável")
else:
    print("⚠️ kmEst não encontrado")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {changes} melhorias aplicadas!")
print("   Recarregue com Ctrl+Shift+R")
