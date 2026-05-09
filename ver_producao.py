import os
path = r'C:\fleet-cloud\app\routers\producao.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print('NAO EXISTE!')
