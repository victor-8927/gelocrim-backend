path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui a URL da Directions API para usar o proxy local
old = """    var url = 'https://maps.googleapis.com/maps/api/directions/json' +
      '?origin=' + origem +
      '&destination=' + destino +
      '&waypoints=' + encodeURIComponent(wpsStr) +
      '&mode=driving&region=br&language=pt-BR' +
      '&key=' + GMAPS_KEY;

    var res  = await fetch(url);"""

new = """    // Usa proxy local para evitar CORS
    var params = '?origin=' + encodeURIComponent(origem) +
      '&destination=' + encodeURIComponent(destino) +
      (wpsStr ? '&waypoints=' + encodeURIComponent(wpsStr) : '');
    var url = '/api/v1/proxy/directions' + params;

    var res  = await fetch(url);"""

if old in content:
    content = content.replace(old, new)
    print('URL atualizada para proxy!')
else:
    print('Padrão não encontrado!')
    # Busca a linha
    idx = content.find('maps.googleapis.com/maps/api/directions')
    ln = content[:idx].count('\n')+1
    print(f'Directions URL na linha {ln}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Pronto!')
