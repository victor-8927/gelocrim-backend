from fastapi import FastAPI, APIRouter, Depends
import sys
import os

# Impede que ele tente importar app.database
sys.path.insert(0, os.path.dirname(__file__))

# Simulação de get_db
def get_db():
    return "fake_db"

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login")
async def login(db: str = Depends(get_db)):
    return {"message": "Rota ativa"}

app = FastAPI()
app.include_router(router)