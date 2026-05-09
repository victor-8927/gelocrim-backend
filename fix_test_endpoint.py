# Testa importando o router diretamente
import sys
sys.path.insert(0, r'C:\fleet-cloud')

try:
    from app.routers.order_items import router
    print('Router importado OK!')
    print('Rotas:')
    for route in router.routes:
        print(f'  {route.methods} {route.path}')
except Exception as e:
    print(f'ERRO ao importar router: {e}')
    import traceback
    traceback.print_exc()

# Testa get_db
try:
    from app.database import get_db
    db = next(get_db())
    print('\nget_db OK!')
    rows = db.execute("SELECT COUNT(*) FROM order_items").fetchone()
    print(f'order_items count: {rows[0]}')
except Exception as e:
    print(f'ERRO get_db: {e}')
