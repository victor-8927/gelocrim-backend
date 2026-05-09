import sqlite3

# ── 1. Atualiza banco de dados ─────────────────────────────────────
db = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute("PRAGMA table_info(drivers)")
cols = [r[1] for r in cur.fetchall()]
print('Colunas atuais:', cols)

novas = [
    ('tipo',         'TEXT DEFAULT "motorista"'),
    ('daily_cost',   'REAL DEFAULT 0'),
    ('veiculo_fixo', 'TEXT'),
    ('data_admissao','TEXT'),
    ('observacoes',  'TEXT'),
]

for col, tipo in novas:
    if col not in cols:
        cur.execute(f'ALTER TABLE drivers ADD COLUMN {col} {tipo}')
        print(f'Coluna adicionada: {col}')
    else:
        print(f'Já existe: {col}')

conn.commit()
conn.close()
print('Banco atualizado!\n')

# ── 2. Atualiza drivers.py ─────────────────────────────────────────
new_api = '''from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/drivers", tags=["Motoristas"])

class DriverIn(BaseModel):
    name:          str
    tipo:          Optional[str]  = "motorista"
    cpf:           Optional[str]  = None
    cnh:           Optional[str]  = None
    cnh_category:  Optional[str]  = None
    phone:         Optional[str]  = None
    vehicle_id:    Optional[str]  = None
    veiculo_fixo:  Optional[str]  = None
    daily_cost:    Optional[float]= 0
    data_admissao: Optional[str]  = None
    observacoes:   Optional[str]  = None

class DriverOut(BaseModel):
    id:            str
    name:          str
    tipo:          Optional[str]  = "motorista"
    cpf:           Optional[str]  = None
    cnh:           Optional[str]  = None
    cnh_category:  Optional[str]  = None
    phone:         Optional[str]  = None
    vehicle_id:    Optional[str]  = None
    veiculo_fixo:  Optional[str]  = None
    daily_cost:    Optional[float]= 0
    data_admissao: Optional[str]  = None
    observacoes:   Optional[str]  = None
    status:        str
    created_at:    str
    model_config   = {"from_attributes": True}

CAMPOS = "id,name,tipo,cpf,cnh,cnh_category,phone,vehicle_id,veiculo_fixo,daily_cost,data_admissao,observacoes,status,created_at"

@router.get("", response_model=list[DriverOut])
def list_drivers(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text(f"SELECT {CAMPOS} FROM drivers WHERE status!=\'deleted\' ORDER BY tipo, name")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", response_model=DriverOut, status_code=201)
def create_driver(body: DriverIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4())
    ts  = now_str()
    db.execute(text("""
        INSERT INTO drivers (id,name,tipo,cpf,cnh,cnh_category,phone,vehicle_id,
            veiculo_fixo,daily_cost,data_admissao,observacoes,created_at,updated_at)
        VALUES (:id,:name,:tipo,:cpf,:cnh,:cat,:phone,:vid,
            :veiculo_fixo,:daily_cost,:data_admissao,:observacoes,:ts,:ts)
    """), {
        "id":uid,"name":body.name,"tipo":body.tipo,"cpf":body.cpf,
        "cnh":body.cnh,"cat":body.cnh_category,"phone":body.phone,"vid":body.vehicle_id,
        "veiculo_fixo":body.veiculo_fixo,"daily_cost":body.daily_cost,
        "data_admissao":body.data_admissao,"observacoes":body.observacoes,"ts":ts
    })
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM drivers WHERE id=:id"), {"id":uid}).fetchone()
    return dict(row._mapping)

@router.patch("/{did}", response_model=DriverOut)
def update_driver(did: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"name","tipo","cpf","cnh","cnh_category","phone","vehicle_id",
               "veiculo_fixo","daily_cost","data_admissao","observacoes","status"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="Nenhum campo valido.")
    updates["updated_at"] = now_str()
    updates["id"] = did
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE drivers SET {sets} WHERE id=:id"), updates)
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM drivers WHERE id=:id"), {"id":did}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Motorista nao encontrado.")
    return dict(row._mapping)

@router.delete("/{did}", status_code=204)
def delete_driver(did: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE drivers SET status=\'deleted\', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":did})
    db.commit()
'''

with open(r'C:\fleet-cloud\app\routers\drivers.py', 'w', encoding='utf-8') as f:
    f.write(new_api)
print('drivers.py atualizado!')
