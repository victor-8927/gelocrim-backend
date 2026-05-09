from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/producao", tags=["Producao"])

class PalletIn(BaseModel):
    nome:        str
    comprimento: Optional[float] = 0
    largura:     Optional[float] = 0
    altura:      Optional[float] = 0
    cubagem:     Optional[float] = 0
    peso_max:    Optional[float] = 0
    observacao:  Optional[str]   = None

class ItemIn(BaseModel):
    nome:        str
    peso:        float
    comprimento: Optional[float] = 0
    largura:     Optional[float] = 0
    altura:      Optional[float] = 0
    un_pallet:   Optional[int]   = 0
    top:         Optional[str]   = "1000"
    observacao:  Optional[str]   = None

# ── PALLETS ──────────────────────────────────────────────────────
@router.get("/pallets")
def list_pallets(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM pallets ORDER BY nome")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("/pallets", status_code=201)
def create_pallet(body: PalletIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4()); ts = now_str()
    db.execute(text("""INSERT INTO pallets (id,nome,comprimento,largura,altura,cubagem,peso_max,observacao,created_at,updated_at)
        VALUES (:id,:nome,:comp,:larg,:alt,:cub,:pmax,:obs,:ts,:ts)"""),
        {"id":uid,"nome":body.nome,"comp":body.comprimento,"larg":body.largura,"alt":body.altura,
         "cub":body.cubagem,"pmax":body.peso_max,"obs":body.observacao,"ts":ts})
    db.commit()
    return {"id":uid,"message":"Pallet criado!"}

@router.patch("/pallets/{pid}")
def update_pallet(pid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"nome","comprimento","largura","altura","cubagem","peso_max","observacao"}
    updates = {k:v for k,v in body.items() if k in allowed}
    updates["updated_at"] = now_str(); updates["id"] = pid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k!="id")
    db.execute(text(f"UPDATE pallets SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message":"Atualizado!"}

@router.delete("/pallets/{pid}", status_code=204)
def delete_pallet(pid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM pallets WHERE id=:id"), {"id":pid})
    db.commit()

# ── ITENS ─────────────────────────────────────────────────────────
@router.get("/itens")
def list_itens(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM itens_producao ORDER BY peso")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("/itens", status_code=201)
def create_item(body: ItemIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4()); ts = now_str()
    db.execute(text("""INSERT INTO itens_producao (id,nome,peso,comprimento,largura,altura,un_pallet,top,observacao,created_at,updated_at)
        VALUES (:id,:nome,:peso,:comp,:larg,:alt,:un,:top,:obs,:ts,:ts)"""),
        {"id":uid,"nome":body.nome,"peso":body.peso,"comp":body.comprimento,"larg":body.largura,
         "alt":body.altura,"un":body.un_pallet,"top":body.top,"obs":body.observacao,"ts":ts})
    db.commit()
    return {"id":uid,"message":"Item criado!"}

@router.patch("/itens/{iid}")
def update_item(iid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"nome","peso","comprimento","largura","altura","un_pallet","top","observacao"}
    updates = {k:v for k,v in body.items() if k in allowed}
    updates["updated_at"] = now_str(); updates["id"] = iid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k!="id")
    db.execute(text(f"UPDATE itens_producao SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message":"Atualizado!"}

@router.delete("/itens/{iid}", status_code=204)
def delete_item(iid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM itens_producao WHERE id=:id"), {"id":iid})
    db.commit()
