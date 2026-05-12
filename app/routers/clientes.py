from uuid import uuid4
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/clientes", tags=["Clients"])

class ClientOut(BaseModel):
    id:           Optional[str]   = None
    codparc:      Optional[int]   = None
    name:         Optional[str]   = None
    trade_name:   Optional[str]   = None
    legal_name:   Optional[str]   = None
    phone:        Optional[str]   = None
    address:      Optional[str]   = None
    district:     Optional[str]   = None
    city:         Optional[str]   = None
    state:        Optional[str]   = None
    lat:          Optional[float] = None
    lng:          Optional[float] = None
    segment:      Optional[str]   = None
    route:        Optional[str]   = None
    geo_zone:     Optional[str]   = None
    service_time: Optional[str]   = None
    status:       Optional[str]   = None
    model_config  = {"from_attributes": True}

@router.get("")
def list_clients(q: Optional[str] = None, db: Session = Depends(get_db)):
    if q and len(q) >= 2:
        rows = db.execute(text("""
            SELECT id, codparc, name, trade_name, legal_name, phone,
                   address, district, city, state, lat, lng,
                   segment, route, geo_zone, service_time, status,
                   similarity(name, :q) AS score
            FROM clients
            WHERE name % :q OR address % :q OR segment % :q
               OR name ILIKE :qlike OR legal_name ILIKE :qlike
            ORDER BY score DESC, name
            LIMIT 50
        """), {"q": q, "qlike": f"%{q}%"}).fetchall()
    else:
        rows = db.execute(text("""
            SELECT id, codparc, name, trade_name, legal_name, phone,
                   address, district, city, state, lat, lng,
                   segment, route, geo_zone, service_time, status
            FROM clients
            ORDER BY name
        """)).fetchall()
    return [dict(r._mapping) for r in rows]

@router.get("/{codparc}")
def get_client(codparc: int, db: Session = Depends(get_db)):
    row = db.execute(text("""
        SELECT id, codparc, name, trade_name, legal_name, phone,
               address, district, city, state, lat, lng,
               segment, route, geo_zone, service_time, status
        FROM clients WHERE codparc = :codparc
    """), {"codparc": codparc}).fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Client not found.")
    return dict(row._mapping)
