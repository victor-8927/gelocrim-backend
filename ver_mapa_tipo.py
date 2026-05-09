path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se usa Google Maps ou Leaflet
uses_google = 'google.maps' in content
uses_leaflet = 'L.map(' in content
print(f'Google Maps: {uses_google}, Leaflet: {uses_leaflet}')

# Verifica a função initMap
idx = content.find('function initMap(')
print('\n=== initMap ===')
print(content[idx:idx+300])
