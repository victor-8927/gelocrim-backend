from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/producao", tags=["Production"])

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

@router.get("/pallets")
def list_pallets(_=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        rows = db.execute(text("SELECT id, name AS nome, length AS comprimento, width AS largura, height AS altura, volume AS cubagem, max_weight AS peso_max, notes AS observacao, created_at FROM pallets ORDER BY name")).fetchall()
        return [dict(r._mapping) for r in rows]
    except:
        return []

@router.post("/pallets", status_code=201)
def create_pallet(body: PalletIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4()); ts = now_str()
    db.execute(text("""INSERT INTO pallets (id,name,length,width,height,volume,max_weight,notes,created_at,updated_at)
        VALUES (:id,:name,:length,:width,:height,:volume,:max_weight,:notes,:ts,:ts)"""),
        {"id":uid,"name":body.nome,"length":body.comprimento,"width":body.largura,
         "height":body.altura,"volume":body.cubagem,"max_weight":body.peso_max,
         "notes":body.observacao,"ts":ts})
    db.commit()
    return {"id":uid,"message":"Pallet created!"}

@router.patch("/pallets/{pid}")
def update_pallet(pid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    mapping = {"nome":"name","comprimento":"length","largura":"width","altura":"height","cubagem":"volume","peso_max":"max_weight","observacao":"notes"}
    updates = {mapping.get(k,k):v for k,v in body.items() if k in mapping}
    if not updates: raise HTTPException(422, "No valid fields.")
    updates["updated_at"] = now_str(); updates["id"] = pid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k!="id")
    db.execute(text(f"UPDATE pallets SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message":"Updated!"}

@router.delete("/pallets/{pid}", status_code=204)
def delete_pallet(pid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM pallets WHERE id=:id"), {"id":pid})
    db.commit()

@router.get("/itens")
def list_items(_=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        rows = db.execute(text("SELECT id, name AS nome, weight AS peso, length AS comprimento, width AS largura, height AS altura, units_per_pallet AS un_pallet, top, notes AS observacao, created_at FROM production_items ORDER BY weight")).fetchall()
        return [dict(r._mapping) for r in rows]
    except:
        return []

@router.post("/itens", status_code=201)
def create_item(body: ItemIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4()); ts = now_str()
    db.execute(text("""INSERT INTO production_items (id,name,weight,length,width,height,units_per_pallet,top,notes,created_at,updated_at)
        VALUES (:id,:name,:weight,:length,:width,:height,:units,:top,:notes,:ts,:ts)"""),
        {"id":uid,"name":body.nome,"weight":body.peso,"length":body.comprimento,
         "width":body.largura,"height":body.altura,"units":body.un_pallet,
         "top":body.top,"notes":body.observacao,"ts":ts})
    db.commit()
    return {"id":uid,"message":"Item created!"}

@router.patch("/itens/{iid}")
def update_item(iid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    mapping = {"nome":"name","peso":"weight","comprimento":"length","largura":"width","altura":"height","un_pallet":"units_per_pallet","top":"top","observacao":"notes"}
    updates = {mapping.get(k,k):v for k,v in body.items() if k in mapping}
    if not updates: raise HTTPException(422, "No valid fields.")
    updates["updated_at"] = now_str(); updates["id"] = iid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k!="id")
    db.execute(text(f"UPDATE production_items SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message":"Updated!"}

@router.delete("/itens/{iid}", status_code=204)
def delete_item(iid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM production_items WHERE id=:id"), {"id":iid})
    db.commit()
