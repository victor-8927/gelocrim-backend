from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from app.database import get_db
router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)
ADMIN_EMAIL    = "distribuicaogelorotas@gmail.com"
ADMIN_PASSWORD = "Gelocrim@2026"
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
    if "@" in email:
        if email == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
            return {
                "access_token": "admin-jwt-token",
                "token_type": "bearer",
                "user": ADMIN_USER,
                "data": {"user": ADMIN_USER}
            }
        raise HTTPException(status_code=401, detail="Email ou senha incorretos!")
    cpf = email.replace(".", "").replace("-", "").replace("/", "")
    if cpf.isdigit() and len(cpf) == 11:
        motorista = db.execute(text("""
            SELECT id, name, cpf, tipo FROM drivers
            WHERE REPLACE(REPLACE(REPLACE(cpf,'.',''),'-',''),'/','') = :cpf
            AND tipo = 'motorista'
        """), {"cpf": cpf}).fetchone()
        if not motorista:
            raise HTTPException(status_code=401, detail="CPF nao encontrado ou nao autorizado!")
        seq = password.zfill(3) if password.isdigit() else password.split('-')[-1].zfill(3)
        rota = db.execute(text("""
            SELECT r.id, r.trip_number FROM routes r
            JOIN drivers d ON d.id = r.driver_id
            WHERE REPLACE(REPLACE(REPLACE(d.cpf,'.',''),'-',''),'/','') = :cpf
            AND r.trip_number LIKE :seq
            AND r.status IN ('released','liberada','executing','executando')
            ORDER BY r.route_date DESC LIMIT 1
        """), {"cpf": cpf, "seq": f"%-{seq}"}).fetchone()
        if not rota:
            raise HTTPException(status_code=401, detail="CPF ou numero de viagem invalido!")
        user = {
            "id": motorista[0],
            "name": motorista[1],
            "cpf": cpf,
            "role": "driver",
            "trip_number": rota[1]
        }
        return {
            "access_token": f"driver-{cpf}",
            "token_type": "bearer",
            "user": user,
            "data": {"user": user}
        }
    raise HTTPException(status_code=401, detail="Credenciais invalidas!")
@router.get("/me")
async def me(token: str = Depends(security)):
    if not token or not token.credentials:
        raise HTTPException(status_code=401, detail="Token invalido")
    cred = token.credentials
    if cred == "admin-jwt-token":
        return ADMIN_USER
    if cred.startswith("driver-"):
        cpf = cred.split("-")[1]
        return {"id": cpf, "role": "driver", "cpf": cpf}
    raise HTTPException(status_code=401, detail="Token invalido")
async def get_current_user(token: str = Depends(security)):
    if not token or not token.credentials:
        return {"id": 1, "username": "admin", "role": "admin"}
    cred = token.credentials
    if cred.startswith("driver-"):
        return {"id": cred.split("-")[1], "username": "driver", "role": "driver"}
    return {"id": 1, "username": "admin", "role": "admin"}
async def require_admin(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito")
    return current_user
