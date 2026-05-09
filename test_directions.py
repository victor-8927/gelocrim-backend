import urllib.request, json

key = 'AIzaSyB47DpEZW4qbU74LxcG1ZD76cYLRlJw88M'
# Manaus → Presidente Figueiredo
url = f'https://maps.googleapis.com/maps/api/directions/json?origin=-3.093544,-60.075812&destination=-1.945278,-60.024722&mode=driving&region=br&language=pt-BR&key={key}'

try:
    req = urllib.request.urlopen(url, timeout=10)
    data = json.loads(req.read())
    print(f'Status: {data["status"]}')
    if data['status'] == 'OK':
        leg = data['routes'][0]['legs'][0]
        print(f'Distância: {leg["distance"]["text"]}')
        print(f'Duração: {leg["duration"]["text"]}')
    else:
        print(f'Erro: {data.get("error_message", data["status"])}')
except Exception as e:
    print(f'Exceção: {e}')
