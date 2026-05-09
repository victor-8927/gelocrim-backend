import os

NGROK_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1'

files = [
    r'C:\gelocrim-motorista\screens\LoginScreen.js',
    r'C:\gelocrim-motorista\screens\RotaScreen.js',
    r'C:\gelocrim-motorista\screens\EntregaScreen.js',
]

for path in files:
    if not os.path.exists(path):
        print(f'Nao encontrado: {path}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    old = "const API_URL = 'http://11.0.1.72:8000/api/v1';"
    new = f"const API_URL = '{NGROK_URL}';"
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Atualizado: {os.path.basename(path)}')
    else:
        print(f'Padrao nao encontrado: {os.path.basename(path)}')

print('\nPronto! Recompile o APK.')
