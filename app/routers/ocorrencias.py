from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/ocorrencias", tags=["Incidents"])

class IncidentIn(BaseModel):
    tipo:              str
    gravidade:         Optional[str]  = "info"
    pedido:            Optional[str]  = None
    cliente:           Optional[str]  = None
    veiculo:           Optional[str]  = None
    descricao:         Optional[str]  = None
    foto:              Optional[str]  = None
    assinatura:        Optional[str]  = None
    status:            Optional[str]  = "pending"
    gerar_devolucao:   Optional[bool] = False
    atualizar_estoque: Optional[bool] = False

CAMPOS = "id,type,severity,invoice,client,vehicle,description,photo,status,created_at,updated_at"

@router.get("")
def list_incidents(_=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        rows = db.execute(text(f"SELECT {CAMPOS} FROM incidents WHERE status!='deleted' ORDER BY created_at DESC")).fetchall()
        return [dict(r._mapping) for r in rows]
    except:
        return []

@router.post("", status_code=201)
def create_incident(body: IncidentIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4()); ts = now_str()
    db.execute(text("""INSERT INTO incidents
        (id,type,severity,invoice,client,vehicle,description,photo,signature,status,created_at,updated_at)
        VALUES (:id,:type,:severity,:invoice,:client,:vehicle,:description,:photo,:signature,:status,:ts,:ts)"""),
        {"id":uid,"type":body.tipo,"severity":body.gravidade,"invoice":body.pedido,
         "client":body.cliente,"vehicle":body.veiculo,"description":body.descricao,
         "photo":body.foto,"signature":body.assinatura,"status":body.status,"ts":ts})
    db.commit()
    return {"id":uid,"message":"Incident registered!"}

@router.patch("/{oid}")
def update_incident(oid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"type","severity","invoice","client","vehicle","description","photo","signature","status"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="No valid fields.")
    updates["updated_at"] = now_str(); updates["id"] = oid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k!="id")
    db.execute(text(f"UPDATE incidents SET {sets} WHERE id=:id"), updates)
    db.commit()
    return {"message":"Updated!"}

@router.delete("/{oid}", status_code=204)
def delete_incident(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE incidents SET status='deleted', updated_at=:ts WHERE id=:id"),
               {"ts":now_str(),"id":oid})
    db.commit()
