path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_mapa = '''  // Mapa de verificação — inicializa APÓS painel estar visível
  setTimeout(() => {
    const mapEl = document.getElementById('conf-mapa');
    if (!mapEl) return;

    // Destroi mapa anterior se existir
    if (confMap) {
      confMap.remove();
      confMap = null;
    }

    // Cria novo mapa
    confMap = L.map('conf-mapa', {zoomControl: true}).setView([-3.093544, -60.075812], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OSM', maxZoom: 18
    }).addTo(confMap);

    const coords = [];

    // Depósito
    L.marker([-3.093544, -60.075812], {
      icon: L.divIcon({
        className: '',
        html: '<div style="background:#0a1628;color:#64B4FF;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;border:2px solid #64B4FF;box-shadow:0 2px 6px rgba(0,0,0,.5)">🏭</div>',
        iconSize: [28,28], iconAnchor: [14,14]
      })
    }).addTo(confMap).bindPopup('<b>Depósito Gelocrim</b>');
    coords.push([-3.093544, -60.075812]);

    // Clientes selecionados
    confOrdem.forEach((o, i) => {
      const lat = parseFloat(o.lat);
      const lng = parseFloat(o.lng);
      if (!isNaN(lat) && !isNaN(lng) && Math.abs(lat) > 0.01) {
        coords.push([lat, lng]);
        L.marker([lat, lng], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#e8521a;color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4)">${i+1}</div>`,
            iconSize: [26,26], iconAnchor: [13,13]
          })
        }).addTo(confMap).bindPopup(`<b>${i+1}. ${o.recipient_name}</b><br>${o.weight_kg||0}kg`);
      }
    });

    // Fecha volta ao depósito
    if (coords.length > 1) coords.push([-3.093544, -60.075812]);

    // Polyline do trajeto
    if (coords.length > 2) {
      L.polyline(coords, {color:'#64B4FF', weight:3, opacity:.85, dashArray:'8,4'}).addTo(confMap);
      confMap.fitBounds(L.latLngBounds(coords), {padding:[40,40]});
    } else if (coords.length === 2) {
      confMap.setView(coords[1], 14);
    }

    // Força renderização correta
    setTimeout(() => confMap.invalidateSize(true), 200);
  }, 500);
}'''

new_mapa = '''  // Mapa de verificação com Google Maps
  setTimeout(() => {
    // Limpa marcadores e polyline anteriores
    if (confMap && confMap._confMarkers) {
      confMap._confMarkers.forEach(m => m.setMap(null));
      confMap._confMarkers = [];
    }
    if (confMap && confMap._confLine) {
      confMap._confLine.setMap(null);
      confMap._confLine = null;
    }

    // Inicializa ou reutiliza o mapa
    if (!confMap) {
      confMap = initMap('conf-mapa', -3.093544, -60.075812, 12);
    }
    if (!confMap) return;
    confMap._confMarkers = [];

    const bounds = new google.maps.LatLngBounds();
    const coords = [];

    // Marcador do depósito
    const deposito = {lat: -3.093544, lng: -60.075812};
    const mDep = new google.maps.Marker({
      position: deposito,
      map: confMap,
      label: { text: '🏭', fontSize: '16px' },
      title: 'Depósito Gelocrim'
    });
    confMap._confMarkers.push(mDep);
    bounds.extend(deposito);
    coords.push(deposito);

    // Marcadores dos clientes
    confOrdem.forEach((o, i) => {
      const lat = parseFloat(o.lat);
      const lng = parseFloat(o.lng);
      if (!isNaN(lat) && !isNaN(lng) && Math.abs(lat) > 0.01) {
        const pos = {lat, lng};
        coords.push(pos);
        bounds.extend(pos);
        const marker = new google.maps.Marker({
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
        });
        const info = new google.maps.InfoWindow({
          content: `<b>${i+1}. ${o.recipient_name}</b><br>${o.weight_kg||0}kg`
        });
        marker.addListener('click', () => info.open(confMap, marker));
        confMap._confMarkers.push(marker);
      }
    });

    // Fecha no depósito
    coords.push(deposito);

    // Polyline do trajeto
    if (coords.length > 2) {
      confMap._confLine = new google.maps.Polyline({
        path: coords,
        geodesic: true,
        strokeColor: '#64B4FF',
        strokeOpacity: 0.85,
        strokeWeight: 3,
        map: confMap
      });
      confMap.fitBounds(bounds);
    } else if (coords.length === 2) {
      confMap.setCenter(coords[1]);
      confMap.setZoom(14);
    }

    // Força resize do mapa
    google.maps.event.trigger(confMap, 'resize');
    if (bounds.isEmpty() === false) confMap.fitBounds(bounds);
  }, 500);
}'''

if old_mapa in content:
    content = content.replace(old_mapa, new_mapa)
    print('Mapa da conferência corrigido para Google Maps!')
else:
    print('Padrão não encontrado, buscando...')
    idx = content.find('// Mapa de verificação')
    print(f'Posição: {idx}')
    if idx != -1:
        print(content[idx:idx+100])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
