import sqlite3
from uuid import uuid4
from datetime import datetime

# ── 1. Cria tabela no banco ────────────────────────────────────────
db = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS ocorrencias (
    id                TEXT PRIMARY KEY,
    tipo              TEXT NOT NULL,
    gravidade         TEXT DEFAULT "info",
    pedido            TEXT,
    cliente           TEXT,
    veiculo           TEXT,
    descricao         TEXT,
    foto              TEXT,
    assinatura        TEXT,
    status            TEXT DEFAULT "pendente",
    gerar_devolucao   INTEGER DEFAULT 0,
    atualizar_estoque INTEGER DEFAULT 0,
    created_at        TEXT,
    updated_at        TEXT
)''')

conn.commit()
conn.close()
print('Tabela ocorrencias criada!')

# ── 2. Cria router de ocorrências ──────────────────────────────────
api_content = '''from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/ocorrencias", tags=["Ocorrencias"])

class OcorrenciaIn(BaseModel):
    tipo:              str
    gravidade:         Optional[str]  = "info"
    pedido:            Optional[str]  = None
    cliente:           Optional[str]  = None
    veiculo:           Optional[str]  = None
    descricao:         Optional[str]  = None
    foto:              Optional[str]  = None
    assinatura:        Optional[str]  = None
    status:            Optional[str]  = "pendente"
    gerar_devolucao:   Optional[bool] = False
    atualizar_estoque: Optional[bool] = False

CAMPOS = "id,tipo,gravidade,pedido,cliente,veiculo,descricao,foto,status,gerar_devolucao,atualizar_estoque,created_at,updated_at"

@router.get("")
def list_ocorrencias(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text(f"SELECT {CAMPOS} FROM ocorrencias WHERE status!=\'deleted\' ORDER BY created_at DESC")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", status_code=201)
def create_ocorrencia(body: OcorrenciaIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4()); ts = now_str()
    db.execute(text("""INSERT INTO ocorrencias 
        (id,tipo,gravidade,pedido,cliente,veiculo,descricao,foto,assinatura,status,gerar_devolucao,atualizar_estoque,created_at,updated_at)
        VALUES (:id,:tipo,:grav,:pedido,:cliente,:veiculo,:desc,:foto,:assin,:status,:gdev,:aest,:ts,:ts)"""),
        {"id":uid,"tipo":body.tipo,"grav":body.gravidade,"pedido":body.pedido,
         "cliente":body.cliente,"veiculo":body.veiculo,"desc":body.descricao,
         "foto":body.foto,"assin":body.assinatura,"status":body.status,
         "gdev":int(body.gerar_devolucao),"aest":int(body.atualizar_estoque),"ts":ts})
    db.commit()
    return {"id":uid,"message":"Ocorrência registrada!"}

@router.patch("/{oid}")
def update_ocorrencia(oid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"tipo","gravidade","pedido","cliente","veiculo","descricao","foto","assinatura","status","gerar_devolucao","atualizar_estoque"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="Nenhum campo valido.")
    updates["updated_at"] = now_str(); updates["id"] = oid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k!="id")
    db.execute(text(f"UPDATE ocorrencias SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message":"Atualizado!"}

@router.delete("/{oid}", status_code=204)
def delete_ocorrencia(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE ocorrencias SET status=\'deleted\', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":oid})
    db.commit()
'''

with open(r'C:\fleet-cloud\app\routers\ocorrencias.py', 'w', encoding='utf-8') as f:
    f.write(api_content)
print('ocorrencias.py criado!')

# ── 3. Registra o router no main.py ───────────────────────────────
main_path = r'C:\fleet-cloud\app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main = f.read()

if 'ocorrencias' not in main:
    # Adiciona import
    main = main.replace(
        'from app.routers.producao import router as producao_router',
        'from app.routers.producao import router as producao_router\nfrom app.routers.ocorrencias import router as ocorrencias_router'
    )
    # Registra router
    main = main.replace(
        'app.include_router(producao_router)',
        'app.include_router(producao_router)\napp.include_router(ocorrencias_router)'
    )
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main)
    print('main.py atualizado com ocorrencias!')
else:
    print('ocorrencias já registrado!')

print('\nReinicie o servidor e Ctrl+Shift+R!')
