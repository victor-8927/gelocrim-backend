HTML_PATH = r'C:\fleet-cloud\gelocrim_v1.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Adicionar TrafficLayer ao inicializar o mapa de conferência
OLD_CONFMAP = """    if (!confMap) {
      confMap = initMap('conf-mapa', -3.093544, -60.075812, 12);
    }
    if (!confMap) return;
    confMap._confMarkers = [];"""

NEW_CONFMAP = """    if (!confMap) {
      confMap = initMap('conf-mapa', -3.093544, -60.075812, 12);
    }
    if (!confMap) return;
    confMap._confMarkers = [];

    // Ativar camada de tráfego em tempo real
    if (!confMap._trafficLayer) {
      confMap._trafficLayer = new google.maps.TrafficLayer();
      confMap._trafficLayer.setMap(confMap);
    }"""

# 2. Adicionar departure_time: now no request do Directions para usar tráfego real
OLD_DIRECTIONS = """        directionsService.route({
        origin:      new google.maps.LatLng(origem.lat, origem.lng),
        destination: new google.maps.LatLng(destino.lat, destino.lng),
        waypoints:   waypoints,
        travelMode:  google.maps.TravelMode.DRIVING,
        optimizeWaypoints: false // mantém a ordem do analista"""

NEW_DIRECTIONS = """        // Horário de saída = hoje às 08:00 para cálculo com tráfego real
        var hoje = new Date();
        var saida = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate(), 8, 0, 0);
        // Se já passou das 08:00, usar horário atual para tráfego real
        if (hoje.getHours() >= 8) saida = hoje;

        directionsService.route({
        origin:      new google.maps.LatLng(origem.lat, origem.lng),
        destination: new google.maps.LatLng(destino.lat, destino.lng),
        waypoints:   waypoints,
        travelMode:  google.maps.TravelMode.DRIVING,
        optimizeWaypoints: false, // mantém a ordem do analista
        drivingOptions: {
          departureTime: saida,
          trafficModel: google.maps.TrafficModel.BEST_GUESS
        }"""

# 3. Adicionar atualização automática do ETA a cada 5 minutos
OLD_TOAST_ETA = """          toast('✅ ' + kmReal.toFixed(1) + ' km reais · ' + hDeslocTotal + 'h' + String(mDeslocTotal).padStart(2,'0') + ' deslocamento · ' + totalAtend + ' min atendimento', 'success');"""

NEW_TOAST_ETA = """          toast('✅ ' + kmReal.toFixed(1) + ' km reais · ' + hDeslocTotal + 'h' + String(mDeslocTotal).padStart(2,'0') + ' deslocamento · ' + totalAtend + ' min atendimento · 🚦 com tráfego real', 'success');

          // Atualização automática do ETA a cada 5 minutos
          if (window._etaAutoRefresh) clearInterval(window._etaAutoRefresh);
          window._etaAutoRefresh = setInterval(function() {
            if (document.getElementById('painel-conferencia').style.display !== 'none') {
              atualizarRotaMapa();
              console.log('ETA atualizado com tráfego em tempo real:', new Date().toLocaleTimeString());
            } else {
              clearInterval(window._etaAutoRefresh);
            }
          }, 5 * 60 * 1000); // a cada 5 minutos"""

# 4. Parar atualização ao fechar conferência
OLD_FECHAR = """function fecharConferencia(){document.getElementById('painel-conferencia').style.display='none';}"""
NEW_FECHAR = """function fecharConferencia(){
  document.getElementById('painel-conferencia').style.display='none';
  if (window._etaAutoRefresh) { clearInterval(window._etaAutoRefresh); window._etaAutoRefresh = null; }
}"""

if OLD_CONFMAP in content:
    content = content.replace(OLD_CONFMAP, NEW_CONFMAP)
    changes += 1
    print("✅ Traffic Layer ativado no mapa de conferência")
else:
    print("⚠️ Bloco confMap não encontrado")

if OLD_DIRECTIONS in content:
    content = content.replace(OLD_DIRECTIONS, NEW_DIRECTIONS)
    changes += 1
    print("✅ Google Directions com tráfego real (departureTime + BEST_GUESS)")
else:
    print("⚠️ Bloco directionsService não encontrado")

if OLD_TOAST_ETA in content:
    content = content.replace(OLD_TOAST_ETA, NEW_TOAST_ETA)
    changes += 1
    print("✅ Atualização automática do ETA a cada 5 minutos")
else:
    print("⚠️ Bloco toast ETA não encontrado")

if OLD_FECHAR in content:
    content = content.replace(OLD_FECHAR, NEW_FECHAR)
    changes += 1
    print("✅ Auto-refresh para ao fechar o painel")
else:
    print("⚠️ fecharConferencia não encontrada")

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {changes} melhorias aplicadas!")
print("   Recarregue com Ctrl+Shift+R")
print("\n   Como funciona:")
print("   🚦 Tráfego em tempo real visível no mapa")
print("   ⏱️  ETA calculado considerando congestionamentos")
print("   🔄 Atualiza automaticamente a cada 5 minutos")
print("   🌅 Se for antes das 08:00, simula saída às 08:00")
print("   🕐 Se for depois das 08:00, usa horário atual")
