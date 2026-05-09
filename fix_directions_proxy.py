# 1. Cria endpoint proxy no backend
proxy_code = '''
from fastapi import APIRouter, Depends
import httpx

router_proxy = APIRouter(prefix="/api/v1/proxy", tags=["Proxy"])

@router_proxy.get("/directions")
async def directions_proxy(
    origin: str, destination: str, waypoints: str = ""
):
    key = "AIzaSyB47DpEZW4qbU74LxcG1ZD76cYLRlJw88M"
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "region": "br",
        "language": "pt-BR",
        "key": key
    }
    if waypoints:
        params["waypoints"] = waypoints
    
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params, timeout=30)
        return res.json()
'''

with open(r'C:\fleet-cloud\app\routers\proxy.py', 'w', encoding='utf-8') as f:
    f.write(proxy_code)
print('proxy.py criado!')

# 2. Adiciona no main.py
with open(r'C:\fleet-cloud\app\main.py', 'r', encoding='utf-8') as f:
    main = f.read()

if 'proxy' not in main:
    main = main.replace(
        'from app.routers.order_items import router as order_items_router',
        'from app.routers.order_items import router as order_items_router\nfrom app.routers.proxy import router_proxy'
    )
    main = main.replace(
        'app.include_router(order_items_router)',
        'app.include_router(order_items_router)\napp.include_router(router_proxy)'
    )
    with open(r'C:\fleet-cloud\app\main.py', 'w', encoding='utf-8') as f:
        f.write(main)
    print('main.py atualizado!')
else:
    print('proxy já no main.py!')

# 3. Instala httpx
import subprocess
r = subprocess.run(
    [r'C:\fleet-cloud\venv\Scripts\pip.exe', 'install', 'httpx'],
    capture_output=True, text=True
)
print('httpx:', r.stdout.strip().split('\n')[-1])

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\proxy.py', doraise=True)
    print('proxy.py VÁLIDO!')
except Exception as e:
    print(f'ERRO: {e}')
