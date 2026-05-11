from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])

class ClienteIn(BaseModel):
    codparc: int
    nome: Optional[str] = ""
    razao_social: Optional[str] = ""
    endereco: Optional[str] = ""
    cep: Optional[str] = ""
    bairro: Optional[str] = ""
    cidade: Optional[str] = ""
    lat: Optional[float] = None
    lng: Optional[float] = None
    cpf_cnpj: Optional[str] = ""
    segmento: Optional[str] = ""
    zona_geo: Optional[str] = ""
    regiao: Optional[str] = ""
    comodatos: Optional[str] = ""
    tempo_entrega: Optional[str] = ""
    rota: Optional[str] = ""
    telefone: Optional[str] = ""
    ativo: Optional[str] = "S"

@router.get("")
def list_clientes(q: Optional[str] = None, db: Session = Depends(get_db)):
    if q and len(q) >= 2:
        result = db.execute(text("""
            SELECT codparc, name AS nome, name AS nome_fantasia,
                   razao_social, cpf_cnpj, phone AS telefone,
                   address AS endereco, bairro, cidade, cep,
                   lat, lng, segmento, rota, zona_geo,
                   tempo_entrega, comodatos,
                   CASE WHEN status='active' THEN 'S' ELSE 'N' END AS ativo,
                   id, created_at,
                   similarity(name, :q) AS score
            FROM clientes
            WHERE name % :q OR address % :q OR segmento % :q
               OR name ILIKE :qlike OR razao_social ILIKE :qlike
            ORDER BY score DESC, name
            LIMIT 50
        """), {"q": q, "qlike": f"%{q}%"})
    else:
        result = db.execute(text("""
            SELECT codparc, name AS nome, name AS nome_fantasia,
                   razao_social, cpf_cnpj, phone AS telefone,
                   address AS endereco, bairro, cidade, cep,
                   lat, lng, segmento, rota, zona_geo,
                   tempo_entrega, comodatos,
                   CASE WHEN status='active' THEN 'S' ELSE 'N' END AS ativo,
                   id, created_at
            FROM clientes ORDER BY name
        """))
    rows = result.mappings().all()
    return [dict(r) for r in rows]

@router.post("/bulk")
def bulk_clientes(clientes: List[ClienteIn], db: Session = Depends(get_db)):
    inserted = 0
    updated = 0
    for c in clientes:
        existing = db.execute(
            text("SELECT id FROM clientes WHERE codparc = :codparc"),
            {"codparc": c.codparc}
        ).fetchone()
        if existing:
            db.execute(text("""
                UPDATE clientes SET
                    nome=:nome, razao_social=:razao_social, endereco=:endereco,
                    cep=:cep, bairro=:bairro, cidade=:cidade,
                    lat=:lat, lng=:lng, cpf_cnpj=:cpf_cnpj,
                    segmento=:segmento, zona_geo=:zona_geo, regiao=:regiao,
                    comodatos=:comodatos, tempo_entrega=:tempo_entrega,
                    rota=:rota, telefone=:telefone, ativo=:ativo
                WHERE codparc=:codparc
            """), c.model_dump())
            updated += 1
        else:
            db.execute(text("""
                INSERT INTO clientes
                    (codparc, nome, razao_social, endereco, cep, bairro, cidade,
                     lat, lng, cpf_cnpj, segmento, zona_geo, regiao,
                     comodatos, tempo_entrega, rota, telefone, ativo)
                VALUES
                    (:codparc, :nome, :razao_social, :endereco, :cep, :bairro, :cidade,
                     :lat, :lng, :cpf_cnpj, :segmento, :zona_geo, :regiao,
                     :comodatos, :tempo_entrega, :rota, :telefone, :ativo)
            """), c.model_dump())
            inserted += 1
    db.commit()
    return {"inserted": inserted, "updated": updated, "total": inserted + updated}
