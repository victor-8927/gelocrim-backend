from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user
import httpx, os

router = APIRouter(prefix="/api/v1/drivers", tags=["Drivers"])

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

class DriverIn(BaseModel):
    name:             str
    type:             Optional[str]   = 'driver'
    cpf:              Optional[str]   = None
    license_number:   Optional[str]   = None
    license_category: Optional[str]   = None
    phone:            Optional[str]   = None
    vehicle_id:       Optional[str]   = None
    fixed_vehicle:    Optional[str]   = None
    daily_cost:       Optional[float] = 0
    hire_date:        Optional[str]   = None
    notes:            Optional[str]   = None
    photo:            Optional[str]   = None
    license_photo:    Optional[str]   = None
    day_off:          Optional[str]   = None
    work_hours:       Optional[str]   = None
    lunch_time:       Optional[str]   = None
    vda:              Optional[str]   = None

class DriverOut(BaseModel):
    id:               str
    name:             str
    type:             Optional[str]   = 'driver'
    cpf:              Optional[str]   = None
    license_number:   Optional[str]   = None
    license_category: Optional[str]   = None
    phone:            Optional[str]   = None
    vehicle_id:       Optional[str]   = None
    fixed_vehicle:    Optional[str]   = None
    daily_cost:       Optional[float] = 0
    hire_date:        Optional[str]   = None
    notes:            Optional[str]   = None
    photo:            Optional[str]   = None
    license_photo:    Optional[str]   = None
    day_off:          Optional[str]   = None
    work_hours:       Optional[str]   = None
    lunch_time:       Optional[str]   = None
    vda:              Optional[str]   = None
    status:           str             = 'active'
    created_at:       Optional[str]   = None
    model_config      = {"from_attributes": True}

CAMPOS = "id,name,type,cpf,license_number,license_category,phone,vehicle_id,fixed_vehicle,daily_cost,hire_date,notes,photo,license_photo,day_off,work_hours,lunch_time,vda,status,created_at"

@router.get("", response_model=list[DriverOut])
def list_drivers(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text(f"SELECT {CAMPOS} FROM drivers WHERE status!='deleted' ORDER BY type, name")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", response_model=DriverOut, status_code=201)
def create_driver(body: DriverIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4())
    ts  = now_str()
    db.execute(text("""
        INSERT INTO drivers (id,name,type,cpf,license_number,license_category,phone,
            vehicle_id,fixed_vehicle,daily_cost,hire_date,notes,photo,license_photo,
            day_off,work_hours,lunch_time,vda,created_at,updated_at)
        VALUES (:id,:name,:type,:cpf,:license_number,:license_category,:phone,
            :vehicle_id,:fixed_vehicle,:daily_cost,:hire_date,:notes,:photo,:license_photo,
            :day_off,:work_hours,:lunch_time,:vda,:ts,:ts)
    """), {
        "id":uid,"name":body.name,"type":body.type,"cpf":body.cpf,
        "license_number":body.license_number,"license_category":body.license_category,
        "phone":body.phone,"vehicle_id":body.vehicle_id,"fixed_vehicle":body.fixed_vehicle,
        "daily_cost":body.daily_cost,"hire_date":body.hire_date,"notes":body.notes,
        "photo":body.photo,"license_photo":body.license_photo,"day_off":body.day_off,
        "work_hours":body.work_hours,"lunch_time":body.lunch_time,"vda":body.vda,"ts":ts
    })
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM drivers WHERE id=:id"), {"id":uid}).fetchone()
    return dict(row._mapping)

@router.patch("/{did}", response_model=DriverOut)
def update_driver(did: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"name","type","cpf","license_number","license_category","phone","vehicle_id",
               "fixed_vehicle","daily_cost","hire_date","notes","photo","license_photo",
               "day_off","work_hours","lunch_time","vda","status"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="No valid fields.")
    updates["updated_at"] = now_str()
    updates["id"] = did
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE drivers SET {sets} WHERE id=:id"), updates)
    db.commit()
    row = db.execute(text(f"SELECT {CAMPOS} FROM drivers WHERE id=:id"), {"id":did}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Driver not found.")
    return dict(row._mapping)

@router.delete("/{did}", status_code=204)
def delete_driver(did: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE drivers SET status='deleted', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":did})
    db.commit()

@router.post("/{did}/upload-photo")
async def upload_photo(did: str, file: UploadFile = File(...), _=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    ext = file.filename.split(".")[-1].lower()
    path = f"{did}/photo.{ext}"
    headers = {"Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": file.content_type}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SUPABASE_URL}/storage/v1/object/driver-photos/{path}", content=content, headers=headers)
        if r.status_code not in (200, 201):
            # tenta upsert
            r = await client.put(f"{SUPABASE_URL}/storage/v1/object/driver-photos/{path}", content=content, headers=headers)
    url = f"{SUPABASE_URL}/storage/v1/object/public/driver-photos/{path}"
    db.execute(text("UPDATE drivers SET photo=:url, updated_at=:ts WHERE id=:id"), {"url":url,"ts":now_str(),"id":did})
    db.commit()
    return {"url": url}

@router.post("/{did}/upload-license")
async def upload_license(did: str, file: UploadFile = File(...), _=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    ext = file.filename.split(".")[-1].lower()
    path = f"{did}/license.{ext}"
    headers = {"Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": file.content_type}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SUPABASE_URL}/storage/v1/object/driver-documents/{path}", content=content, headers=headers)
        if r.status_code not in (200, 201):
            r = await client.put(f"{SUPABASE_URL}/storage/v1/object/driver-documents/{path}", content=content, headers=headers)
    url = f"{SUPABASE_URL}/storage/v1/object/public/driver-documents/{path}"
    db.execute(text("UPDATE drivers SET license_photo=:url, updated_at=:ts WHERE id=:id"), {"url":url,"ts":now_str(),"id":did})
    db.commit()
    return {"url": url}

