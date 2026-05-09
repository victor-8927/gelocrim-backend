path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_polyline = '''    // Polyline do trajeto
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

new_polyline = '''    // Trajeto real pelas ruas usando Directions API
    if (coords.length >= 2) {
      const directionsService  = new google.maps.DirectionsService();
      const directionsRenderer = new google.maps.DirectionsRenderer({
        map: confMap,
        suppressMarkers: true, // usa nossos marcadores numerados
        polylineOptions: {
          strokeColor: '#64B4FF',
          strokeOpacity: 0.85,
          strokeWeight: 4
        }
      });
      confMap._confLine = directionsRenderer;

      // Monta waypoints (paradas intermediárias — máx 25 no Google)
      const origem  = coords[0]; // depósito
      const destino = coords[coords.length - 1]; // volta ao depósito
      const waypoints = coords.slice(1, coords.length - 1).slice(0, 23).map(c => ({
        location: new google.maps.LatLng(c.lat, c.lng),
        stopover: true
      }));

      directionsService.route({
        origin:      new google.maps.LatLng(origem.lat, origem.lng),
        destination: new google.maps.LatLng(destino.lat, destino.lng),
        waypoints:   waypoints,
        travelMode:  google.maps.TravelMode.DRIVING,
        optimizeWaypoints: false // mantém a ordem do analista
      }, (result, status) => {
        if (status === 'OK') {
          directionsRenderer.setDirections(result);
          // Calcula distância real total
          let kmReal = 0;
          result.routes[0].legs.forEach(leg => {
            kmReal += leg.distance.value / 1000;
          });
          const el = document.getElementById('conf-distancia');
          if (el) el.textContent = kmReal.toFixed(1) + ' km (real)';
        } else {
          // Fallback: linha reta se Directions falhar
          confMap._confLine = new google.maps.Polyline({
            path: coords, geodesic: true,
            strokeColor: '#64B4FF', strokeOpacity: 0.7, strokeWeight: 3,
            map: confMap
          });
          confMap.fitBounds(bounds);
        }
      });

      confMap.fitBounds(bounds);
    }

    // Força resize do mapa
    google.maps.event.trigger(confMap, 'resize');
    if (!bounds.isEmpty()) confMap.fitBounds(bounds);
  }, 500);
}'''

if old_polyline in content:
    content = content.replace(old_polyline, new_polyline)
    print('Trajeto real implementado com Directions API!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
