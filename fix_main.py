path = r'C:\fleet-cloud\app\main.py'

new_main = '''from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, vehicles, drivers, orders, routes, reports, sync
from app.routers.producao import router as producao_router
from app.routers.ocorrencias import router as ocorrencias_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import init_schema
    init_schema()
    yield

app = FastAPI(title="Gelocrim Fleet API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(orders.router)
app.include_router(routes.router)
app.include_router(reports.router)
app.include_router(sync.router)
app.include_router(producao_router)
app.include_router(ocorrencias_router)

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
def root():
    return {"app": "Gelocrim Fleet API", "docs": "/docs"}
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_main)

print('main.py atualizado com producao e ocorrencias!')
print('Reinicie o servidor!')
