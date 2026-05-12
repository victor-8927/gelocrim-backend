from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/vehicles", tags=["Vehicles"])

class VehicleIn(BaseModel):
    plate:                str
    model:                Optional[str]   = None
    brand:                Optional[str]   = None
    year:                 Optional[int]   = None
    capacity_kg:          Optional[float] = 0
    volume_m3:            Optional[float] = 0
    vda:                  Optional[str]   = None
    type:                 Optional[str]   = None
    fuel_type:            Optional[str]   = None
    km_per_liter:         Optional[float] = None
    fuel_price:           Optional[float] = None
    annual_tax:           Optional[float] = None
    monthly_maintenance:  Optional[float] = None
    daily_cost:           Optional[float] = None
    pallets:              Optional[int]   = None
    box_length:           Optional[float] = None
    box_width:            Optional[float] = None
    box_height:           Optional[float] = None
    last_oil_date:        Optional[str]   = None
    next_oil_date:        Optional[str]   = None
    oil_cost:             Optional[float] = None

class VehicleOut(BaseModel):
    id:                   str
    plate:                str
    model:                Optional[str]   = None
    brand:                Optional[str]   = None
    year:                 Optional[int]   = None
    capacity_kg:          Optional[float] = 0
    volume_m3:            Optional[float] = 0
    vda:                  Optional[str]   = None
    type:                 Optional[str]   = None
    fuel_type:            Optional[str]   = None
    km_per_liter:         Optional[float] = None
    fuel_price:           Optional[float] = None
    annual_tax:           Optional[float] = None
    monthly_maintenance:  Optional[float] = None
    daily_cost:           Optional[float] = None
    pallets:              Optional[int]   = None
    box_length:           Optional[float] = None
    box_width:            Optional[float] = None
    box_height:           Optional[float] = None
    last_oil_date:        Optional[str]   = None
    next_oil_date:        Optional[str]   = None
    oil_cost:             Optional[float] = None
    status:               str             = 'active'
    created_at:           Optional[str]   = None
    model_config          = {"from_attributes": True}

CAMPOS = "id,plate,model,brand,year,capacity_kg,volume_m3,vda,type,fuel_type,km_per_liter,fuel_price,annual_tax,monthly_maintenance,daily_cost,pallets,box_length,box_width,box_height,last_oil_date,next_oil_date,oil_cost,status,created_at"

@router.get("", response_model=list[VehicleOut])
def list_vehicles(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text(f"SELECT {CAMPOS} FROM vehicles WHERE status!='deleted' ORDER BY vda, plate")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", response_model=VehicleOut, status_code=201)
def create_vehicle(body: VehicleIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4())
    ts  = now_str()
    db.execute(text("""
        INSERT INTO vehicles (id,plate,model,brand,year,capacity_kg,volume_m3,vda,type,
            fuel_type,km_per_liter,fuel_price,annual_tax,monthly_maintenance,daily_cost,
            pallets,box_length,box_width,box_height,last_oil_date,next_oil_date,oil_cost,
            status,created_at,updated_at)
        VALUES (:id,:plate,:model,:brand,:year,:capacity_kg,:volume_m3,:vda,:type,
            :fuel_type,:km_per_liter,:fuel_price,:annual_tax,:monthly_maintenance,:daily_cost,
            :pallets,:box_length,:box_width,:box_height,:last_oil_date,:next_oil_date,:oil_cost,
            'active',:ts,:ts)
    """), {
        "id":uid,"plate":body.plate,"model":body.model,"brand":body.brand,"year":body.year,
        "capacity_kg":body.capacity_kg,"volume_m3":body.volume_m3,"vda":body.vda,"type":body.type,
        "fuel_type":body.fuel_type,"km_per_liter":body.km_per_liter,"fuel_price":body.fuel_price,
        "annual_tax":body.annual_tax,"monthly_maintenance":body.monthly_maintenance,
        "daily_cost":body.daily_cost,"pallets":body.pallets,"box_length":body.box_length,
        "box_width":body.box_width,"box_height":body.box_height,"last_oil_date":body.last_oil_date,
        "next_oil_date":body.next_oil_date,"oil_cost":body.oil_cost,"ts":ts
    })
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM vehicles WHERE id=:id"), {"id":uid}).fetchone()
    return dict(row._mapping)

@router.patch("/{vid}", response_model=VehicleOut)
def update_vehicle(vid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"plate","model","brand","year","capacity_kg","volume_m3","vda","type",
              "fuel_type","km_per_liter","fuel_price","annual_tax","monthly_maintenance",
               "daily_cost","pallets","box_length","box_width","box_height",
               "last_oil_date","next_oil_date","oil_cost","status"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="No valid fields.")
    updates["updated_at"] = now_str()
    updates["id"] = vid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE vehicles SET {sets} WHERE id=:id"), updates)
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM vehicles WHERE id=:id"), {"id":vid}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Vehicle not found.")
    return dict(row._mapping)

@router.delete("/{vid}", status_code=204)
def delete_vehicle(vid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE vehicles SET status='deleted', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":vid})
    db.commit()
