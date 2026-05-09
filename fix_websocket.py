# Adiciona WebSocket e endpoint de notas por stop no backend
ws_code = '''
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

# Manager de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}  # route_id -> [ws]

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
            await ws.receive_text()  # mantém conexão viva
    except WebSocketDisconnect:
        manager.disconnect(route_id, ws)
'''

# Adiciona ao arquivo routes.py
with open(r'C:\fleet-cloud\app\routers\routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona imports necessários
if 'WebSocket' not in content:
    content = content.replace(
        'from fastapi import APIRouter, Depends, HTTPException',
        'from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect'
    )
    content = content.replace(
        'from typing import Optional, List',
        'from typing import Optional, List, Dict'
    )
    # Adiciona manager e WebSocket antes do primeiro router
    content = ws_code + '\n' + content
    print('WebSocket adicionado!')

# Adiciona endpoint de notas por stop
notas_endpoint = '''
@router.get("/{route_id}/stops/{stop_id}/notas")
def get_notas_stop(route_id: str, stop_id: str, db: Session = Depends(get_db)):
    """Retorna todas as notas/pedidos de uma parada agrupados"""
    stop = db.execute(text(
        "SELECT codparc, order_id FROM route_stops WHERE stop_id = :id"
    ), {"id": stop_id}).mappings().fetchone()
    if not stop:
        raise HTTPException(404, "Stop não encontrado")
    
    # Busca todos os orders do mesmo codparc com status routed/pending
    orders = db.execute(text("""
        SELECT o.id, o.external_id, o.weight_kg, o.status,
               oi.item_tipo, oi.item_nome, oi.qtd, oi.peso_unit, oi.top_app
        FROM orders o
        LEFT JOIN order_items oi ON oi.codparc = o.codparc
        WHERE o.codparc = :codparc
        AND o.status IN ('routed', 'pending', 'delivered')
        ORDER BY o.external_id, oi.item_tipo
    """), {"codparc": stop["codparc"]}).mappings().all()
    
    # Agrupa por order
    notas = {}
    for r in orders:
        oid = r["external_id"]
        if oid not in notas:
            notas[oid] = {
                "external_id": oid,
                "top_app": r["top_app"] or "1000",
                "weight_kg": float(r["weight_kg"] or 0),
                "status": r["status"],
                "itens": []
            }
        if r["item_nome"]:
            notas[oid]["itens"].append({
                "nome": r["item_nome"],
                "qtd": r["qtd"],
                "peso_unit": r["peso_unit"]
            })
    
    return list(notas.values())
'''

if 'get_notas_stop' not in content:
    content += notas_endpoint
    print('Endpoint notas adicionado!')

with open(r'C:\fleet-cloud\app\routers\routes.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Registra no main.py
with open(r'C:\fleet-cloud\app\main.py', 'r', encoding='utf-8') as f:
    main = f.read()

if 'router_ws' not in main:
    main = main.replace(
        'from app.routers.routes import router as routes_router',
        'from app.routers.routes import router as routes_router, router_ws, manager'
    )
    main = main.replace(
        'app.include_router(routes_router)',
        'app.include_router(routes_router)\napp.include_router(router_ws)'
    )
    with open(r'C:\fleet-cloud\app\main.py', 'w', encoding='utf-8') as f:
        f.write(main)
    print('WebSocket registrado no main.py!')

import py_compile
for f in [r'C:\fleet-cloud\app\routers\routes.py', r'C:\fleet-cloud\app\main.py']:
    try:
        py_compile.compile(f, doraise=True)
        print(f'{f.split(chr(92))[-1]}: VÁLIDO')
    except Exception as e:
        print(f'ERRO: {e}')
