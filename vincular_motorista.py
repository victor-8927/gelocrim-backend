import sys, os
sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text

JAVIER_DRIVER_ID = '5fdd2166-37a7-4aae-8ef7-954c1f63e7c3'
ROTA_ID = '56b9650d-61f7-4c99-996c-0a4b9fd3f3ae'

with engine_sync.begin() as conn:
    # Vincula Javier à rota
    conn.execute(text("UPDATE routes SET driver_id=:did WHERE id=:rid"),
        {'did': JAVIER_DRIVER_ID, 'rid': ROTA_ID})
    print(f'Javier vinculado à rota {ROTA_ID[:8]}...')

    # Verifica
    row = conn.execute(text("SELECT id, driver_id, status FROM routes WHERE id=:rid"),
        {'rid': ROTA_ID}).fetchone()
    print(f'Resultado: {row}')

print('\nAgora corrija o filtro na API...')

# Corrige routes.py para filtrar por driver_id quando role=driver
routes_path = r'C:\fleet-cloud\app\routers\routes.py'
with open(routes_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verifica se o filtro ja existe
if 'role' in content and 'driver' in content and 'driver_id' in content:
    print('Filtro ja pode existir, verificando...')
    idx = content.find('def list_routes')
    print(content[idx:idx+800])
else:
    print('Filtro nao encontrado!')
    idx = content.find('def list_routes')
    print(content[idx:idx+500])
