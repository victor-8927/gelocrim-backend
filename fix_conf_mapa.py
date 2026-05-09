path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_mapa = '''  // Mapa de verificação
  setTimeout(() => {
    const mapEl = document.getElementById('conf-mapa');
    if (!mapEl) return;

    if (!confMap) {
      confMap = L.map('conf-mapa').setView([-3.093544, -60.075812], 12);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OSM', maxZoom: 18
      }).addTo(confMap);
    } else {
      // Limpa camadas anteriores
      confMap.eachLayer(layer => {
        if (layer instanceof L.Marker || layer instanceof L.Polyline) {
          confMap.removeLayer(layer);
        }
      });
    }

    const coords = [];

    // Marcador do depósito
    L.marker([-3.093544, -60.075812], {
      icon: L.divIcon({
        className: '',
        html: '<div style="background:#0a1628;color:#64B4FF;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;border:2px solid #64B4FF;box-shadow:0 2px 6px rgba(0,0,0,.4)">🏭</div>',
        iconSize: [28,28], iconAnchor: [14,14]
      })
    }).addTo(confMap).bindPopup('<b>Depósito Gelocrim</b>');
    coords.push([-3.093544, -60.075812]);

    // Marcadores dos clientes
    confOrdem.forEach((o, i) => {
      if (o.lat && o.lng && Math.abs(parseFloat(o.lat)) > 0.01) {
        const lat = parseFloat(o.lat);
        const lng = parseFloat(o.lng);
        coords.push([lat, lng]);
        L.marker([lat, lng], {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#e8521a;color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4)">${i+1}</div>`,
            iconSize: [26,26], iconAnchor: [13,13]
          })
        }).addTo(confMap).bindPopup(`<b>${i+1}. ${o.recipient_name}</b><br>Peso: ${o.weight_kg||0}kg`);
      }
    });

    // Volta ao depósito
    if (coords.length > 1) coords.push([-3.093544, -60.075812]);

    // Desenha polyline do trajeto
    if (coords.length > 2) {
      L.polyline(coords, {color:'#64B4FF', weight:3, opacity:.85, dashArray:'8,4'}).addTo(confMap);
      const bounds = L.latLngBounds(coords);
      confMap.fitBounds(bounds, {padding:[30,30]});
    } else if (coords.length === 2) {
      confMap.setView(coords[1], 13);
    }

    // Invalida tamanho para forçar renderização correta
    setTimeout(() => confMap.invalidateSize(), 100);
  }, 300);
}'''

new_mapa = '''  // Mapa de verificação — inicializa APÓS painel estar visível
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

if old_mapa in content:
    content = content.replace(old_mapa, new_mapa)
    print('Mapa corrigido!')
else:
    print('Padrão não encontrado, buscando alternativa...')
    idx = content.find('// Mapa de verificação — inicializa APÓS')
    if idx == -1:
        idx = content.find('// Mapa de verificação')
        print(f'Encontrado em: {idx}')
        print(content[idx:idx+200])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Faca Ctrl+Shift+R.')
