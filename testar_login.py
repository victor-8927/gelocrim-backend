import urllib.request, json

data = json.dumps({'email':'distribuicaogelorotas@gmail.com','password':'Gelocrim@2026'}).encode()
req = urllib.request.Request('http://localhost:8000/api/v1/auth/login', 
    data=data, headers={'Content-Type':'application/json'})
try:
    resp = urllib.request.urlopen(req)
    print('OK:', resp.status, json.loads(resp.read()))
except urllib.error.HTTPError as e:
    print('ERRO:', e.code, json.loads(e.read()))
