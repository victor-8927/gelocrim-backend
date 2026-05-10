from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/vehicles", tags=["Veiculos"])

class VehicleIn(BaseModel):
    vda:           Optional[str]   = None
    plate:         str
    model:         str
    type:          str             = "caminhao_truck"
    capacity_kg:   float           = 1000
    capacity_m3:   float           = 8
    status:        str             = 'active'
    fuel_type:     Optional[str]   = "diesel"
    km_per_liter:  Optional[float] = 4.0
    fuel_price:    Optional[float] = 6.50
    ipva_anual:    Optional[float] = 0
    manut_mes:     Optional[float] = 0
    daily_cost:    Optional[float] = 0
    pallets:       Optional[int]   = 0
    bau_comp:      Optional[float] = 0
    bau_larg:      Optional[float] = 0
    bau_alt:       Optional[float] = 0
    oleo_ult_data: Optional[str]   = None
    oleo_prox_data:Optional[str]   = None
    oleo_custo:    Optional[float] = 0

class VehicleOut(BaseModel):
    id:            str
    vda:           Optional[str]   = None
    plate:         str
    model:         str
    type:          str
    capacity_kg:   float
    capacity_m3:   float
    status:        str
    fuel_type:     Optional[str]   = None
    km_per_liter:  Optional[float] = None
    fuel_price:    Optional[float] = None
    ipva_anual:    Optional[float] = None
    manut_mes:     Optional[float] = None
    daily_cost:    Optional[float] = None
    pallets:       Optional[int]   = None
    bau_comp:      Optional[float] = None
    bau_larg:      Optional[float] = None
    bau_alt:       Optional[float] = None
    oleo_ult_data: Optional[str]   = None
    oleo_prox_data:Optional[str]   = None
    oleo_custo:    Optional[float] = None
    created_at:    str
    model_config   = {"from_attributes": True}

CAMPOS = "id,vda,plate,model,type,capacity_kg,capacity_m3,status,fuel_type,km_per_liter,fuel_price,ipva_anual,manut_mes,daily_cost,pallets,bau_comp,bau_larg,bau_alt,oleo_ult_data,oleo_prox_data,oleo_custo,created_at"

@router.get("", response_model=list[VehicleOut])
def list_vehicles(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text(f"SELECT {CAMPOS} FROM vehicles WHERE status!='deleted' ORDER BY vda, plate")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", response_model=VehicleOut, status_code=201)
def create_vehicle(body: VehicleIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4())
    ts  = now_str()
    try:
        db.execute(text("""
            INSERT INTO vehicles (id,vda,plate,model,type,capacity_kg,capacity_m3,status,
                fuel_type,km_per_liter,fuel_price,ipva_anual,manut_mes,daily_cost,
                pallets,bau_comp,bau_larg,bau_alt,oleo_ult_data,oleo_prox_data,oleo_custo,
                created_at,updated_at)
            VALUES (:id,:vda,:plate,:model,:type,:kg,:m3,:status,
                :fuel_type,:km_per_liter,:fuel_price,:ipva_anual,:manut_mes,:daily_cost,
                :pallets,:bau_comp,:bau_larg,:bau_alt,:oleo_ult_data,:oleo_prox_data,:oleo_custo,
                :ts,:ts)
        """), {
            "id":uid,"vda":body.vda,"plate":body.plate,"model":body.model,
            "type":body.type,"kg":body.capacity_kg,"m3":body.capacity_m3,"status":body.status,
            "fuel_type":body.fuel_type,"km_per_liter":body.km_per_liter,"fuel_price":body.fuel_price,
            "ipva_anual":body.ipva_anual,"manut_mes":body.manut_mes,"daily_cost":body.daily_cost,
            "pallets":body.pallets,"bau_comp":body.bau_comp,"bau_larg":body.bau_larg,"bau_alt":body.bau_alt,
            "oleo_ult_data":body.oleo_ult_data,"oleo_prox_data":body.oleo_prox_data,"oleo_custo":body.oleo_custo,
            "ts":ts
        })
        db.commit()
    except Exception as e:
        db.rollback()
        if "UNIQUE" in str(e): raise HTTPException(status_code=409, detail="Placa ja cadastrada.")
        raise HTTPException(status_code=500, detail=str(e))
    row = db.execute(text(f"SELECT {CAMPOS} FROM vehicles WHERE id=:id"), {"id":uid}).fetchone()
    return dict(row._mapping)

@router.patch("/{vid}", response_model=VehicleOut)
def update_vehicle(vid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {
        "vda","plate","model","type","capacity_kg","capacity_m3","status",
        "fuel_type","km_per_liter","fuel_price","ipva_anual","manut_mes","daily_cost",
        "pallets","bau_comp","bau_larg","bau_alt","oleo_ult_data","oleo_prox_data","oleo_custo"
    }
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="Nenhum campo valido.")
    updates["updated_at"] = now_str()
    updates["id"] = vid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE vehicles SET {sets} WHERE id=:id"), updates)
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM vehicles WHERE id=:id"), {"id":vid}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Veiculo nao encontrado.")
    return dict(row._mapping)

@router.delete("/{vid}", status_code=204)
def delete_vehicle(vid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE vehicles SET status='deleted', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":vid})
    db.commit()
