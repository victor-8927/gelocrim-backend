# Testa se o servidor responde corretamente
import urllib.request
try:
    req = urllib.request.Request('http://localhost:8000', headers={'Host': 'localhost'})
    # Nao vai funcionar aqui pois estamos em container
    print('Nao consigo testar daqui - verificar no servidor')
except:
    pass

# Verifica o main.py - como serve o HTML
path = r'C:\fleet-cloud\app\main.py'
with open(path, 'r', encoding='utf-8') as f:
    print(f.read())
