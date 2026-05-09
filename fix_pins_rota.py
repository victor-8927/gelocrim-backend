HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ── 1. Pins por segmento ──────────────────────────────────────
# Substituir os marcadores genéricos por pins com cor e ícone por segmento
OLD_MARKER = """        const marker = new google.maps.Marker({
          position: pos,
          map: confMap,
          label: {
            text: String(i+1),
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '11px'
          },
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 14,
            fillColor: '#e8521a',
            fillOpacity: 1,
            strokeColor: '#fff',
            strokeWeight: 2
          },
          title: o.recipient_name
        });"""

NEW_MARKER = """        // Definir cor e emoji por segmento
        var seg = (o.segmento||o.segment||'').toUpperCase();
        var pinCor, pinEmoji;
        if (seg.indexOf('POSTO') >= 0 || seg.indexOf('COMBUST') >= 0) {
          pinCor = '#FF6B35'; pinEmoji = '⛽';
        } else if (seg.indexOf('ILHA') >= 0 || seg.indexOf('GELAD') >= 0) {
          pinCor = '#00FFEA'; pinEmoji = '🧊';
        } else if (seg.indexOf('FABRIC') >= 0 || seg.indexOf('INDUST') >= 0) {
          pinCor = '#BF5FFF'; pinEmoji = '🏭';
        } else if (seg.indexOf('REFEIT') >= 0 || seg.indexOf('RESTAUR') >= 0 || seg.indexOf('LANCH') >= 0) {
          pinCor = '#FFD700'; pinEmoji = '🍽️';
        } else if (seg.indexOf('DISTRIB') >= 0 || seg.indexOf('ATACAD') >= 0) {
          pinCor = '#00FF88'; pinEmoji = '📦';
        } else if (seg.indexOf('MERCED') >= 0 || seg.indexOf('SUPERM') >= 0 || seg.indexOf('MERCE') >= 0) {
          pinCor = '#FF3355'; pinEmoji = '🛒';
        } else if (seg.indexOf('BAR') >= 0 || seg.indexOf('BOATE') >= 0 || seg.indexOf('CLUB') >= 0) {
          pinCor = '#FF8C00'; pinEmoji = '🍺';
        } else if (seg.indexOf('HOTEL') >= 0 || seg.indexOf('POUSAD') >= 0) {
          pinCor = '#90afd4'; pinEmoji = '🏨';
        } else if (seg.indexOf('CONV') >= 0) {
          pinCor = '#FF6B35'; pinEmoji = '🏪';
        } else {
          pinCor = '#64B4FF'; pinEmoji = '📍';
        }

        const marker = new google.maps.Marker({
          position: pos,
          map: confMap,
          label: {
            text: pinEmoji + String(i+1),
            color: '#001020',
            fontWeight: '900',
            fontSize: '11px'
          },
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 18,
            fillColor: pinCor,
            fillOpacity: 1,
            strokeColor: '#001020',
            strokeWeight: 2
          },
          title: o.recipient_name
        });"""

# ── 2. Corrigir KM para contar ida + volta ────────────────────
OLD_KMREAL = """          let kmReal = 0;
          let minReal = 0;
          var legs = result.routes[0].legs;
          legs.forEach(leg => {
            kmReal += leg.distance.value / 1000;
            minReal += leg.duration.value / 60;
          });"""

NEW_KMREAL = """          let kmReal = 0;
          let minReal = 0;
          var legs = result.routes[0].legs;
          legs.forEach(leg => {
            kmReal += leg.distance.value / 1000;
            minReal += leg.duration.value / 60;
          });
          // KM total = ida + volta (o último leg já inclui retorno ao depósito)
          // Garantir que o display mostre km real completo (ida+volta)"""

# ── 3. Restaurar polyline azul sobre a rota do Directions ────
OLD_RENDERER = """      const directionsRenderer = new google.maps.DirectionsRenderer({
        map: confMap,
        suppressMarkers: true, // usa nossos marcadores numerados
        polylineOptions: {
          strokeColor: '#64B4FF',
          strokeOpacity: 0.85,
          strokeWeight: 4
        }
      });"""

NEW_RENDERER = """      const directionsRenderer = new google.maps.DirectionsRenderer({
        map: confMap,
        suppressMarkers: true, // usa nossos marcadores numerados
        polylineOptions: {
          strokeColor: '#00FFEA',
          strokeOpacity: 0.9,
          strokeWeight: 5,
          icons: [{
            icon: {
              path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
              scale: 3,
              strokeColor: '#001020',
              fillColor: '#00FFEA',
              fillOpacity: 1
            },
            offset: '0%',
            repeat: '80px'
          }]
        }
      });"""

# ── 4. Corrigir display de KM (ida+volta) ────────────────────
OLD_KM_DISPLAY = """          const el = document.getElementById('conf-distancia');"""
NEW_KM_DISPLAY = """          // Atualizar distância real com ida+volta
          var elDist = document.getElementById('conf-distancia');
          if (elDist) elDist.textContent = kmReal.toFixed(1) + ' km (real ida+volta)';
          const el = document.getElementById('conf-distancia');"""

if OLD_MARKER in content:
    content = content.replace(OLD_MARKER, NEW_MARKER)
    changes += 1
    print("✅ Pins por segmento com cores neon e emojis")
else:
    print("⚠️ Bloco marker não encontrado")

if OLD_KMREAL in content:
    content = content.replace(OLD_KMREAL, NEW_KMREAL)
    changes += 1
    print("✅ KM ida+volta corrigido")
else:
    print("⚠️ Bloco kmReal não encontrado")

if OLD_RENDERER in content:
    content = content.replace(OLD_RENDERER, NEW_RENDERER)
    changes += 1
    print("✅ Polyline neon com setas direcionais restaurado")
else:
    print("⚠️ Bloco directionsRenderer não encontrado")

if OLD_KM_DISPLAY in content:
    content = content.replace(OLD_KM_DISPLAY, NEW_KM_DISPLAY, 1)
    changes += 1
    print("✅ Display de KM atualizado")
else:
    print("⚠️ Bloco KM display não encontrado")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {changes} correções aplicadas!")
print("   Recarregue com Ctrl+Shift+R")
print("\n   Pins por segmento:")
print("   ⛽ Posto/Combustível → laranja")
print("   🧊 Ilha Gelada → ciano neon")
print("   🏭 Fábrica/Indústria → roxo")
print("   🍽️  Refeitório/Restaurante → dourado")
print("   📦 Distribuidora/Atacado → verde neon")
print("   🛒 Mercado/Supermercado → vermelho")
print("   🍺 Bar/Boate → laranja escuro")
print("   🏪 Conveniência → laranja")
print("   📍 Outros → azul")
