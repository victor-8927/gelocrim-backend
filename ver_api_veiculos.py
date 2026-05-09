import os

# Busca o arquivo de rotas de veículos
for root, dirs, files in os.walk(r'C:\fleet-cloud\app'):
    for f in files:
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        if 'vehicles' in content and ('PATCH' in content or 'patch' in content or 'update' in content.lower()):
            print(f'\n=== {path} ===')
            # Mostra trecho relevante
            idx = content.lower().find('vehicle')
            print(content[max(0,idx-100):idx+800])
            break
