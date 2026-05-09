with open(r'C:\fleet-cloud\app\routers\routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# O problema é que o bloco ws_code foi inserido ANTES dos imports
# Precisa mover os imports para o topo

# Verifica onde estão os imports
idx_import = content.find('from fastapi import APIRouter')
idx_ws = content.find('class ConnectionManager')

print(f'imports na linha: {content[:idx_import].count(chr(10))+1}')
print(f'ConnectionManager na linha: {content[:idx_ws].count(chr(10))+1}')

# Remove o bloco ws do início e coloca após os imports do fastapi
ws_block = '''
# Manager de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, route_id: str, ws: WebSocket):
        await ws.accept()
        if route_id not in self.active:
            self.active[route_id] = []
        self.active[route_id].append(ws)

    def disconnect(self, route_id: str, ws: WebSocket):
        if route_id in self.active:
            self.active[route_id].remove(ws)

    async def broadcast(self, route_id: str, data: dict):
        if route_id in self.active:
            dead = []
            for ws in self.active[route_id]:
                try:
                    await ws.send_json(data)
                except:
                    dead.append(ws)
            for d in dead:
                self.active[route_id].remove(d)

manager = ConnectionManager()

router_ws = APIRouter(tags=["WebSocket"])

@router_ws.websocket("/ws/routes/{route_id}")
async def websocket_rota(route_id: str, ws: WebSocket):
    await manager.connect(route_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(route_id, ws)
'''

# Reconstrói o arquivo na ordem correta
# 1. Remove todo o conteúdo antes dos imports reais
lines = content.split('\n')
first_import_line = None
for i, line in enumerate(lines):
    if line.startswith('from fastapi import') or line.startswith('import '):
        first_import_line = i
        break

clean_content = '\n'.join(lines[first_import_line:])

# 2. Adiciona ws_block após os imports principais
insert_after = 'router = APIRouter(prefix="/api/v1/routes", tags=["Rotas"])'
clean_content = clean_content.replace(insert_after, insert_after + '\n' + ws_block)

with open(r'C:\fleet-cloud\app\routers\routes.py', 'w', encoding='utf-8') as f:
    f.write(clean_content)

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\routes.py', doraise=True)
    print('routes.py VÁLIDO!')
except Exception as e:
    print(f'ERRO: {e}')
