from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.vehicles import router as vehicles_router
from app.routers.drivers import router as drivers_router
from app.routers.orders import router as orders_router
from app.routers.routes import router as routes_router, router_ws, manager
from app.routers.reports import router as reports_router
from app.routers.sync import router as sync_router
from app.routers.producao import router as producao_router
from app.routers.ocorrencias import router as ocorrencias_router
from app.routers.clientes import router as clientes_router
from app.routers.order_items import router as order_items_router
from app.routers.proxy import router_proxy

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import init_schema
    init_schema()
    yield

app = FastAPI(title="Gelocrim Fleet API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.mount("/fotos", StaticFiles(directory="fotos"), name="fotos")
app.include_router(auth_router)
app.include_router(vehicles_router)
app.include_router(drivers_router)
app.include_router(orders_router)
app.include_router(routes_router)
app.include_router(router_ws)
app.include_router(reports_router)
app.include_router(sync_router)
app.include_router(producao_router)
app.include_router(ocorrencias_router)
app.include_router(clientes_router)
app.include_router(order_items_router)
app.include_router(router_proxy)

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
def root():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gelocrim_v1.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"app": "Gelocrim Fleet API", "docs": "/docs"}

@app.get("/app")
def app_html():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gelocrim_v1.html")
    return FileResponse(html_path)

