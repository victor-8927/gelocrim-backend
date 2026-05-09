# Ver prefix dos outros routers
import os
routers_path = r'C:\fleet-cloud\app\routers'
for f in os.listdir(routers_path):
    if f.endswith('.py'):
        with open(os.path.join(routers_path, f), 'r') as fp:
            content = fp.read()
        idx = content.find('APIRouter(')
        if idx != -1:
            print(f'{f}: {repr(content[idx:idx+80])}')
