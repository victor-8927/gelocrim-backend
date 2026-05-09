"""
fix_all_routers.py
Corrige todos os routers removendo async/await desnecessários.
"""
import os

BASE = r"C:\fleet-cloud"

# ── vehicles.py ───────────────────────────────────────────────
vehicles_content = '''from uuid import uuid4
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
    plate: str
    model: str
    type: str = "truck"
    capacity_kg: float = 1000
    capacity_m3: float = 8
    status: str = "active"

class VehicleOut(BaseModel):
    id: str
    plate: str
    model: str
    type: str
    capacity_kg: float
    capacity_m3: float
    status: str
    created_at: str
    model_config = {"from_attributes": True}

@router.get("", response_model=list[VehicleOut])
def list_vehicles(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id,plate,model,type,capacity_kg,capacity_m3,status,created_at FROM vehicles WHERE status!='deleted' ORDER BY plate")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", response_model=VehicleOut, status_code=201)
def create_vehicle(body: VehicleIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4())
    try:
        db.execute(text("INSERT INTO vehicles (id,plate,model,type,capacity_kg,capacity_m3,status,created_at,updated_at) VALUES (:id,:plate,:model,:type,:kg,:m3,:status,:ts,:ts)"),
            {"id":uid,"plate":body.plate,"model":body.model,"type":body.type,"kg":body.capacity_kg,"m3":body.capacity_m3,"status":body.status,"ts":now_str()})
        db.commit()
    except Exception as e:
        db.rollback()
        if "UNIQUE" in str(e): raise HTTPException(status_code=409, detail="Placa ja cadastrada.")
        raise HTTPException(status_code=500, detail=str(e))
    row = db.execute(text("SELECT id,plate,model,type,capacity_kg,capacity_m3,status,created_at FROM vehicles WHERE id=:id"), {"id":uid}).fetchone()
    return dict(row._mapping)

@router.patch("/{vid}", response_model=VehicleOut)
def update_vehicle(vid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"plate","model","type","capacity_kg","capacity_m3","status"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="Nenhum campo valido.")
    updates["updated_at"] = now_str()
    updates["id"] = vid
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE vehicles SET {sets} WHERE id=:id"), updates)
    db.commit()
    row = db.execute(text("SELECT id,plate,model,type,capacity_kg,capacity_m3,status,created_at FROM vehicles WHERE id=:id"), {"id":vid}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Veiculo nao encontrado.")
    return dict(row._mapping)

@router.delete("/{vid}", status_code=204)
def delete_vehicle(vid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE vehicles SET status=\'deleted\', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":vid})
    db.commit()
'''

# ── drivers.py ────────────────────────────────────────────────
drivers_content = '''from uuid import uuid4
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
    name: str
    cpf: Optional[str] = None
    cnh: Optional[str] = None
    cnh_category: Optional[str] = None
    phone: Optional[str] = None
    vehicle_id: Optional[str] = None

class DriverOut(BaseModel):
    id: str
    name: str
    cpf: Optional[str]
    cnh: Optional[str]
    cnh_category: Optional[str]
    phone: Optional[str]
    vehicle_id: Optional[str]
    status: str
    created_at: str
    model_config = {"from_attributes": True}

@router.get("", response_model=list[DriverOut])
def list_drivers(_=Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id,name,cpf,cnh,cnh_category,phone,vehicle_id,status,created_at FROM drivers WHERE status!=\'deleted\' ORDER BY name")).fetchall()
    return [dict(r._mapping) for r in rows]

@router.post("", response_model=DriverOut, status_code=201)
def create_driver(body: DriverIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    uid = str(uuid4())
    db.execute(text("INSERT INTO drivers (id,name,cpf,cnh,cnh_category,phone,vehicle_id,created_at,updated_at) VALUES (:id,:name,:cpf,:cnh,:cat,:phone,:vid,:ts,:ts)"),
        {"id":uid,"name":body.name,"cpf":body.cpf,"cnh":body.cnh,"cat":body.cnh_category,"phone":body.phone,"vid":body.vehicle_id,"ts":now_str()})
    db.commit()
    row = db.execute(text("SELECT id,name,cpf,cnh,cnh_category,phone,vehicle_id,status,created_at FROM drivers WHERE id=:id"), {"id":uid}).fetchone()
    return dict(row._mapping)

@router.patch("/{did}", response_model=DriverOut)
def update_driver(did: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"name","cpf","cnh","cnh_category","phone","vehicle_id","status"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if not updates: raise HTTPException(status_code=422, detail="Nenhum campo valido.")
    updates["updated_at"] = now_str()
    updates["id"] = did
    sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
    db.execute(text(f"UPDATE drivers SET {sets} WHERE id=:id"), updates)
    db.commit()
    row = db.execute(text("SELECT id,name,cpf,cnh,cnh_category,phone,vehicle_id,status,created_at FROM drivers WHERE id=:id"), {"id":did}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Motorista nao encontrado.")
    return dict(row._mapping)

@router.delete("/{did}", status_code=204)
def delete_driver(did: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(text("UPDATE drivers SET status=\'deleted\', updated_at=:ts WHERE id=:id"), {"ts":now_str(),"id":did})
    db.commit()
'''

# ── orders.py ─────────────────────────────────────────────────
orders_content = '''from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_compat import now_str
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/orders", tags=["Pedidos"])

class RecipientIn(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    phone: Optional[str] = None

class OrderIn(BaseModel):
    external_id: Optional[str] = None
    recipient: RecipientIn
    weight_kg: float = 0
    volume_m3: float = 0
    tw_start: Optional[str] = "08:00"
    tw_end: Optional[str] = "18:00"
    notes: Optional[str] = None

class BatchIn(BaseModel):
    source: str = "manual"
    orders: list[OrderIn]

class OrderOut(BaseModel):
    id: str
    external_id: Optional[str]
    recipient_name: str
    address: str
    weight_kg: float
    volume_m3: float
    tw_start: Optional[str]
    tw_end: Optional[str]
    status: str
    created_at: str
    model_config = {"from_attributes": True}

@router.get("", response_model=list[OrderOut])
def list_orders(
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """SELECT o.id, o.external_id, r.name AS recipient_name, r.address,
               o.weight_kg, o.volume_m3, o.tw_start, o.tw_end, o.status, o.created_at
        FROM orders o JOIN recipients r ON r.id = o.recipient_id"""
    params = {"limit": limit}
    if status:
        q += " WHERE o.status = :status"
        params["status"] = status
    q += " ORDER BY o.created_at DESC LIMIT :limit"
    rows = db.execute(text(q), params).fetchall()
    return [dict(r._mapping) for r in rows]

@router.get("/{oid}")
def get_order(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.execute(text("""SELECT o.id, o.external_id, r.name AS recipient_name, r.address,
               r.lat, r.lng, r.phone, o.weight_kg, o.volume_m3,
               o.tw_start, o.tw_end, o.nfe_status, o.status, o.notes, o.created_at
        FROM orders o JOIN recipients r ON r.id = o.recipient_id WHERE o.id = :id"""), {"id": oid}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Pedido nao encontrado.")
    return dict(row._mapping)

@router.post("/batch", status_code=201)
def create_batch(body: BatchIn, _=Depends(get_current_user), db: Session = Depends(get_db)):
    created = []
    skipped = 0
    ts = now_str()
    for o in body.orders:
        if o.external_id:
            ex = db.execute(text("SELECT id FROM orders WHERE external_id=:ext"), {"ext": o.external_id}).fetchone()
            if ex: skipped += 1; continue
        rid = str(uuid4())
        db.execute(text("INSERT OR IGNORE INTO recipients (id,name,address,lat,lng,phone,created_at) VALUES (:id,:name,:addr,:lat,:lng,:phone,:ts)"),
            {"id":rid,"name":o.recipient.name,"addr":o.recipient.address,"lat":o.recipient.lat,"lng":o.recipient.lng,"phone":o.recipient.phone,"ts":ts})
        oid = str(uuid4())
        db.execute(text("INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,weight_kg,volume_m3,tw_start,tw_end,notes,created_at,updated_at) VALUES (:id,:ext,:src,:rid,:lat,:lng,:kg,:m3,:tws,:twe,:notes,:ts,:ts)"),
            {"id":oid,"ext":o.external_id,"src":body.source,"rid":rid,"lat":o.recipient.lat,"lng":o.recipient.lng,"kg":o.weight_kg,"m3":o.volume_m3,"tws":o.tw_start,"twe":o.tw_end,"notes":o.notes,"ts":ts})
        created.append(oid)
    db.commit()
    return {"created": len(created), "skipped": skipped, "ids": created}

@router.patch("/{oid}")
def update_order(oid: str, body: dict, _=Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = {"status","nfe_key","nfe_status","notes"}
    updates = {k:v for k,v in body.items() if k in allowed}
    if updates:
        updates["updated_at"] = now_str()
        updates["id"] = oid
        sets = ", ".join(f"{k}=:{k}" for k in updates if k != "id")
        db.execute(text(f"UPDATE orders SET {sets} WHERE id=:id"), updates)
        db.commit()
    return {"ok": True}

@router.delete("/{oid}", status_code=204)
def delete_order(oid: str, _=Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.execute(text("SELECT status FROM orders WHERE id=:id"), {"id": oid}).fetchone()
    if not row: raise HTTPException(status_code=404, detail="Pedido nao encontrado.")
    if row.status == "routed": raise HTTPException(status_code=409, detail="Pedido ja roteirizado.")
    db.execute(text("DELETE FROM orders WHERE id=:id"), {"id": oid})
    db.commit()
'''

# Salva os arquivos
files = {
    "app/routers/vehicles.py": vehicles_content,
    "app/routers/drivers.py": drivers_content,
    "app/routers/orders.py": orders_content,
}

for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path.replace("/", "\\"))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {rel_path} corrigido!")

# Corrige routes.py removendo await
routes_path = os.path.join(BASE, "app", "routers", "routes.py")
with open(routes_path, "r", encoding="utf-8") as f:
    routes = f.read()

# Remove await das chamadas de banco
import re
routes = re.sub(r'await (db\.execute|db\.commit)\(', r'\1(', routes)
routes = re.sub(r'await db\.commit\(\)', r'db.commit()', routes)
routes = routes.replace('async def list_routes', 'def list_routes')
routes = routes.replace('async def optimize', 'def optimize')
routes = routes.replace('async def update_route', 'def update_route')
routes = routes.replace('async def update_stop', 'def update_stop')
routes = routes.replace('async def get_route_stops', 'def get_route_stops')
routes = routes.replace('AsyncSession', 'Session')
routes = routes.replace('from sqlalchemy.ext.asyncio import AsyncSession', '')
routes = re.sub(r'rows = db\.execute\((.+?)\)(?!\s*\.fetchall)', r'rows = db.execute(\1).fetchall', routes, flags=re.DOTALL)

with open(routes_path, "w", encoding="utf-8") as f:
    f.write(routes)
print("✅ app/routers/routes.py corrigido!")

print("\n🎉 Todos os routers corrigidos!")
print("Reinicie o servidor para aplicar as mudancas.")
