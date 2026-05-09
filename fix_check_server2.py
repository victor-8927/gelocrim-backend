# Verifica se o router de rotas tem erro de sintaxe
import ast, py_compile, traceback

path = r'C:\fleet-cloud\app\routers\routes.py'
try:
    py_compile.compile(path, doraise=True)
    print('routes.py: SEM ERROS de sintaxe')
except py_compile.PyCompileError as e:
    print(f'ERRO em routes.py: {e}')

# Verifica main.py também
path2 = r'C:\fleet-cloud\app\main.py'
try:
    py_compile.compile(path2, doraise=True)
    print('main.py: SEM ERROS')
except py_compile.PyCompileError as e:
    print(f'ERRO em main.py: {e}')

# Tenta importar o router
import sys
sys.path.insert(0, r'C:\fleet-cloud')
try:
    from app.routers import routes
    print('routes router: importado OK')
except Exception as e:
    print(f'ERRO ao importar routes: {e}')
    traceback.print_exc()
