import os

path_html = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path_html, 'r', encoding='utf-8') as f:
    content = f.read()

# Modal de motorista
idx = content.find('modal-driver')
print('=== MODAL DRIVER ===')
print(content[idx:idx+1200])

# API de motoristas
for root, dirs, files in os.walk(r'C:\fleet-cloud\app\routers'):
    for f in files:
        if 'driver' in f.lower() and f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                print(f'\n=== {path} ===')
                print(fp.read())
