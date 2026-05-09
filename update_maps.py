"""
Atualiza o gelocrim_v1.html para usar Google Maps em vez de OpenStreetMap.
Execute: python update_maps.py
"""
import os

html_path = r"C:\fleet-cloud\gelocrim_v1.html"

# Lê o arquivo atual
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Lê a API key do .env
api_key = ""
env_path = r"C:\fleet-cloud\.env"
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("GOOGLE_MAPS_KEY="):
            api_key = line.strip().split("=", 1)[1]
            break

if not api_key:
    print("❌ GOOGLE_MAPS_KEY não encontrada no .env!")
    exit(1)

print(f"✅ API Key encontrada: {api_key[:20]}...")

# Remove Leaflet e adiciona Google Maps
content = content.replace(
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>',
    ''
)
content = content.replace(
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>',
    f'<script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=geometry,places"></script>'
)

# Substitui a função initMap para usar Google Maps
old_map_func = """// ── MAP HELPER ──
function initMap(id, lat=-3.1019, lng=-60.0250, zoom=12) {
  if (maps[id]) { maps[id].invalidateSize(); return maps[id]; }
  const m = L.map(id).setView([lat, lng], zoom);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution:'© OpenStreetMap',maxZoom:19}).addTo(m);
  L.marker([lat, lng], {icon: L.divIcon({className:'', html:`<div style="width:14px;height:14px;background:#e8521a;border:2px solid #fff;border-radius:50%;box-shadow:0 2px 8px rgba(232,82,26,.5)"></div>`, iconSize:[14,14]})}).addTo(m).bindPopup('<b>Depósito Gelocrim</b>');
  maps[id] = m;
  return m;
}"""

new_map_func = """// ── MAP HELPER (Google Maps) ──
function initMap(id, lat=-3.1019, lng=-60.0250, zoom=12) {
  if (maps[id]) return maps[id];
  const el = document.getElementById(id);
  if (!el) return null;
  const m = new google.maps.Map(el, {
    center: {lat, lng},
    zoom,
    mapTypeId: 'roadmap',
    styles: [
      {featureType:'poi',elementType:'labels',stylers:[{visibility:'off'}]},
      {featureType:'transit',stylers:[{visibility:'off'}]}
    ]
  });
  // Marcador do depósito
  new google.maps.Marker({
    position: {lat, lng},
    map: m,
    title: 'Depósito Gelocrim',
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: '#e8521a',
      fillOpacity: 1,
      strokeColor: '#fff',
      strokeWeight: 2
    }
  });
  maps[id] = m;
  return m;
}

function addMarker(map, lat, lng, color, title, info) {
  const marker = new google.maps.Marker({
    position: {lat, lng},
    map,
    title,
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 8,
      fillColor: color,
      fillOpacity: 1,
      strokeColor: '#fff',
      strokeWeight: 2
    }
  });
  if (info) {
    const iw = new google.maps.InfoWindow({content: info});
    marker.addListener('click', () => iw.open(map, marker));
  }
  return marker;
}

function drawRoute(map, stops, color) {
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
}"""

if old_map_func in content:
    content = content.replace(old_map_func, new_map_func)
    print("✅ Função initMap atualizada para Google Maps!")
else:
    print("⚠️  Função initMap não encontrada exatamente — adicionando nova versão...")
    content = content.replace(
        "// ── MAP HELPER ──",
        new_map_func + "\n// ── MAP HELPER LEGADO ──"
    )

# Atualiza função loadMapOrders para usar Google Maps
old_load_orders = """async function loadMapOrders() {
  if (!map) { initMap(); return; }
  clearMapMarkers();
  try {
    const orders = await api('GET', '/orders?status=pending');
    orders.forEach((o, i) => {
      if (!o.lat || !o.lng) return;
      const m = L.marker([o.lat || -3.1019, o.lng || -60.0250], {
        icon: L.divIcon({className:'', html:`<div style="width:8px;height:8px;background:#d97706;border:1px solid #fff;border-radius:50%"></div>`, iconSize:[8,8]})
      }).addTo(map).bindPopup(`<b>${o.recipient_name}</b><br>${o.address}<br>Peso: ${o.weight_kg}kg`);
      mapMarkers.push(m);
    });
    document.getElementById('map-info').textContent = `${orders.length} pedidos pendentes exibidos no mapa`;
    toast(`${orders.length} pedidos carregados no mapa`);
  } catch(e) { toast(e.message,'error'); }
}"""

new_load_orders = """async function loadMapOrders() {
  const m = initMap('dash-map');
  if (!m) return;
  clearMapMarkers();
  try {
    const orders = await api('GET', '/orders?status=pending');
    orders.forEach(o => {
      if (!o.lat || !o.lng || Math.abs(o.lat) < 0.01) return;
      const marker = addMarker(m, o.lat, o.lng, '#d97706', o.recipient_name,
        `<div style="font-family:sans-serif;font-size:13px"><b>${o.recipient_name}</b><br>${o.address}<br>Peso: ${o.weight_kg}kg</div>`);
      mapMarkers.push(marker);
    });
    if (document.getElementById('map-info'))
      document.getElementById('map-info').textContent = `${orders.length} pedidos pendentes exibidos no mapa`;
    toast(`${orders.length} pedidos carregados`);
  } catch(e) { toast(e.message,'error'); }
}"""

if old_load_orders in content:
    content = content.replace(old_load_orders, new_load_orders)
    print("✅ loadMapOrders atualizado!")

# Atualiza clearMapMarkers para Google Maps
content = content.replace(
    """function clearMapMarkers() {
  mapMarkers.forEach(m => map.removeLayer(m));
  mapMarkers = [];
}""",
    """function clearMapMarkers() {
  mapMarkers.forEach(m => { if(m && m.setMap) m.setMap(null); });
  mapMarkers = [];
}"""
)

# Salva o arquivo atualizado
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n🎉 gelocrim_v1.html atualizado com Google Maps!")
print(f"Acesse: http://localhost:8080/gelocrim_v1.html")
