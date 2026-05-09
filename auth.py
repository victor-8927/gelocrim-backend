from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from app.database import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)

# Credenciais do admin
ADMIN_EMAIL    = "distribuicaogelorotas@gmail.com"
ADMIN_PASSWORD = "Gelocrim@2026"  # TROQUE ESTA SENHA!

ADMIN_USER = {
    "id": 1,
    "name": "Distribuicao Gelocrim",
    "firstName": "Distribuicao",
    "lastName": "Gelocrim",
    "username": "distribuicaogelorotas",
    "email": ADMIN_EMAIL,
    "role": "admin"
}

class LoginBody(BaseModel):
    email: str = ""
    password: str = ""

@router.post("/login")
async def login(body: LoginBody, db: Session = Depends(get_db)):
    email    = (body.email or "").strip().lower()
    password = (body.password or "").strip()

    # 1. Login admin
    if email == ADMIN_EMAIL.lower():
        if password != ADMIN_PASSWORD:
            raise HTTPException(status_code=401, detail="Senha incorreta!")
        return {
            "access_token": "admin-jwt-token",
            "token_type": "bearer",
            "user": ADMIN_USER,
            "data": {"user": ADMIN_USER}
        }

    # 2. Login motorista por CPF + numero da viagem
    cpf = email.replace(".", "").replace("-", "").replace("/", "")
    if cpf.isdigit() and len(cpf) == 11:
        # Buscar motorista pelo CPF
        motorista = db.execute(text("""
            SELECT id, name, cpf, role FROM drivers
            WHERE REPLACE(REPLACE(REPLACE(cpf,'.',''),'-',''),'/','') = :cpf
            AND ativo = 1
        """), {"cpf": cpf}).fetchone()

        if not motorista:
            raise HTTPException(status_code=401, detail="CPF nao cadastrado!")

        # Buscar rota ativa com esse numero de viagem
        rota = db.execute(text("""
            SELECT r.id, r.name, r.vehicle_id, r.trip_number
            FROM routes r
            INNER JOIN route_drivers rd ON rd.route_id = r.id
            WHERE rd.driver_id = :driver_id
              AND r.trip_number = :trip
              AND r.status IN ('planned', 'active')
            LIMIT 1
        """), {"driver_id": motorista[0], "trip": password}).fetchone()

        if not rota:
            raise HTTPException(status_code=401, detail="Numero de viagem invalido ou nao autorizado!")

        user = {
            "id": motorista[0],
            "name": motorista[1],
            "cpf": cpf,
            "role": "driver",
            "route_id": rota[0],
            "trip_number": rota[3]
        }
        return {
            "access_token": f"driver-{motorista[0]}-{rota[0]}",
            "token_type": "bearer",
            "user": user,
            "data": {"user": user}
        }

    raise HTTPException(status_code=401, detail="Credenciais invalidas!")

@router.get("/me")
async def me():
    return ADMIN_USER

async def get_current_user(token: str = Depends(security)):
    if not token or not token.credentials:
        return {"id": 1, "username": "admin", "role": "admin"}
    cred = token.credentials
    if cred.startswith("driver-"):
        parts = cred.split("-")
        return {"id": parts[1], "username": "driver", "role": "driver"}
    return {"id": 1, "username": "admin", "role": "admin"}

async def require_admin(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito")
    return current_user
