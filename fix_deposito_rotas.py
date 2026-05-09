import re

# 1. Atualiza coordenadas do deposito no .env
env_path = r'C:\fleet-cloud\.env'
with open(env_path, 'r', encoding='utf-8') as f:
    env = f.read()

env = env.replace('DEPOT_LAT=-3.1019', 'DEPOT_LAT=-3.093544')
env = env.replace('DEPOT_LNG=-60.0250', 'DEPOT_LNG=-60.075812')

with open(env_path, 'w', encoding='utf-8') as f:
    f.write(env)
print('Coordenadas do deposito atualizadas!')

# 2. Atualiza config.py
config_path = r'C:\fleet-cloud\app\config.py'
with open(config_path, 'r', encoding='utf-8') as f:
    config = f.read()

config = config.replace('"-3.1019"', '"-3.093544"')
config = config.replace('"-60.0250"', '"-60.075812"')

with open(config_path, 'w', encoding='utf-8') as f:
    f.write(config)
print('config.py atualizado!')

# 3. Atualiza o HTML para usar Google Maps Directions API nas rotas
html_path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Atualiza coordenadas do deposito no HTML
html = html.replace('lat: -3.1019, lng: -60.0250', 'lat: -3.093544, lng: -60.075812')
html = html.replace('{lat: -3.1019, lng: -60.0250}', '{lat: -3.093544, lng: -60.075812}')
html = html.replace('lat=-3.1019, lng=-60.0250', 'lat=-3.093544, lng=-60.075812')
html = html.replace('DEPOT_LAT = -3.1019', 'DEPOT_LAT = -3.093544')
html = html.replace('DEPOT_LNG = -60.0250', 'DEPOT_LNG = -60.075812')

# Adiciona funcao de rota real com Directions API
new_js = '''
// ── ROTA REAL PELAS RUAS (Google Maps Directions API) ────────────
const DEPOT = {lat: -3.093544, lng: -60.075812};

async function desenharRotaReal(map, stops, cor) {
  if (!map || !stops || stops.length < 2 || typeof google === 'undefined') return;

  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer({
    map: map,
    suppressMarkers: true,
    polylineOptions: {
      strokeColor: cor,
      strokeOpacity: 0.8,
      strokeWeight: 4
    }
  });

  // Monta waypoints (origem = deposito, destino = deposito)
  const waypoints = stops.slice(1, -1).map(s => ({
    location: new google.maps.LatLng(s.lat, s.lng),
    stopover: true
  }));

  try {
    const result = await new Promise((resolve, reject) => {
      directionsService.route({
        origin: new google.maps.LatLng(DEPOT.lat, DEPOT.lng),
        destination: new google.maps.LatLng(DEPOT.lat, DEPOT.lng),
        waypoints: waypoints.slice(0, 25), // limite Google = 25 waypoints
        optimizeWaypoints: false,
        travelMode: google.maps.TravelMode.DRIVING,
        region: 'BR'
      }, (result, status) => {
        if (status === 'OK') resolve(result);
        else reject(status);
      });
    });

    directionsRenderer.setDirections(result);
    return directionsRenderer;
  } catch(e) {
    console.warn('Directions API falhou, usando linha reta:', e);
    // Fallback: linha reta
    const path = [DEPOT, ...stops.map(s => ({lat: parseFloat(s.lat), lng: parseFloat(s.lng)})), DEPOT];
    return new google.maps.Polyline({
      path,
      geodesic: true,
      strokeColor: cor,
      strokeOpacity: 0.7,
      strokeWeight: 3,
      map
    });
  }
}
'''

# Injeta antes do ultimo </script>
last_script = html.rfind('</script>')
if last_script != -1:
    html = html[:last_script] + new_js + '\n' + html[last_script:]
    print('Funcao desenharRotaReal adicionada!')

# Substitui a linha reta pela rota real na Torre de Controle
old_poly = '''      // Desenha linha da rota
      if (tcMap && stopsLatLng.length > 2) {
        const poly = new google.maps.Polyline({
          path: stopsLatLng,
          geodesic: true,
          strokeColor: cor,
          strokeOpacity: 0.7,
          strokeWeight: 3,
          map: tcMap
        });
        tcPolylines.push(poly);
      }'''

new_poly = '''      // Desenha rota real pelas ruas
      if (tcMap && stops.length > 0) {
        const stopsComCoord = stops.filter(s => s.lat && s.lng);
        if (stopsComCoord.length > 0) {
          const renderer = await desenharRotaReal(tcMap, stopsComCoord, cor);
          if (renderer) tcPolylines.push(renderer);
        }
      }'''

html = html.replace(old_poly, new_poly)

# Substitui rota reta na roteirizacao visual tambem
old_draw = '''function drawRoute(map, stops, color) {
  if (stops.length < 2) return;
  const path = stops.map(s => ({lat: s.lat, lng: s.lng}));
  new google.maps.Polyline({
    path,
    geodesic: true,
    strokeColor: color,
    strokeOpacity: 0.8,
    strokeWeight: 3,
    map
  });
}'''

new_draw = '''async function drawRoute(map, stops, color) {
  if (!stops || stops.length < 1) return;
  await desenharRotaReal(map, stops, color);
}'''

html = html.replace(old_draw, new_draw)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML atualizado com rotas reais!')
print('\nResumo das mudancas:')
print('  Deposito: -3.093544, -60.075812 (coordenadas do link)')
print('  Rotas: agora usam Google Maps Directions API (ruas reais)')
print('  Fallback: linha reta se Directions API falhar')
print('\nReinicie a API e faca Ctrl+Shift+R no navegador!')
