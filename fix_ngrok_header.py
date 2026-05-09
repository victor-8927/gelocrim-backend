import os

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

    # Adiciona header ngrok-skip-browser-warning em todos os headers
    old = "const headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` };"
    new = "const headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`, 'ngrok-skip-browser-warning': '1' };"
    
    if old in content:
        content = content.replace(old, new)
        print(f'Header ngrok adicionado: {os.path.basename(path)}')
    
    # LoginScreen nao tem token ainda
    old2 = "headers: { 'Content-Type': 'application/json' },"
    new2 = "headers: { 'Content-Type': 'application/json', 'ngrok-skip-browser-warning': '1' },"
    if old2 in content:
        content = content.replace(old2, new2)
        print(f'Header ngrok adicionado no login: {os.path.basename(path)}')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('\nPronto! Recompile o APK.')
