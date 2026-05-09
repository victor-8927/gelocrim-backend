import os
path = r'C:\fleet-cloud\app\routers\clientes.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print('ARQUIVO NAO EXISTE!')
    # Lista routers disponíveis
    for f in os.listdir(r'C:\fleet-cloud\app\routers'):
        print(f)
