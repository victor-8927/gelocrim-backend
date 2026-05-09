import sys, os
sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')
import requests

r = requests.post('http://localhost:8000/api/v1/auth/login',
    json={'email':'distribuicaogelorotas@gmail.com','password':'Fleet2026'})
token = r.json()['access_token']
print('Login OK')

r2 = requests.get('http://localhost:8000/api/v1/routes?date=2026-04-15',
    headers={'Authorization': f'Bearer {token}'})
rotas = r2.json()
print(f'Rotas: {len(rotas)}')

for rota in rotas:
    rid = rota['route_id']
    print(f"\nRota: {rid} status={rota['status']}")
    r3 = requests.get(f'http://localhost:8000/api/v1/routes/{rid}/stops',
        headers={'Authorization': f'Bearer {token}'})
    print(f'Stops status: {r3.status_code}')
    stops = r3.json()
    if isinstance(stops, list):
        print(f'Total stops: {len(stops)}')
        if stops:
            print(f'Primeiro stop: {stops[0]}')
    else:
        print(f'Resposta: {stops}')
