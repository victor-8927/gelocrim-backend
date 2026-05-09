"""
Sincronizacao de entidades Sankhya via API REST.
"""
import os, logging, httpx
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.integrations.sankhya.auth import get_headers, GATEWAY_URL

logger = logging.getLogger(__name__)
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY", "")

def now_iso(): return datetime.now(timezone.utc).isoformat()

def _start_run(db, entity):
    rid = str(uuid4())
    try:
        db.execute(text("INSERT INTO integration_runs (id,source,entity,status,started_at) VALUES (:id,'sankhya',:e,'running',NOW())"), {"id":rid,"e":entity})
        db.commit()
    except: db.rollback()
    return rid

def _finish_run(db, rid, stats, error=None):
    try:
        db.execute(text("""UPDATE integration_runs SET status=:s,records_found=:f,records_created=:c,
            records_updated=:u,records_skipped=:sk,records_failed=:fa,error_message=:e,
            finished_at=NOW() WHERE id=:id"""),
            {"id":rid,"s":"error" if error else "success","f":stats.get("found",0),
             "c":stats.get("created",0),"u":stats.get("updated",0),
             "sk":stats.get("skipped",0),"fa":stats.get("failed",0),"e":error})
        db.commit()
    except: db.rollback()

def _fmap(entity):
    fields = entity.get("f", [])
    if isinstance(fields, dict): fields = [fields]
    return {f["@name"]: f.get("$", "") for f in fields}

async def sync_customers(db: Session) -> dict:
    rid = _start_run(db, "customers")
    stats = {"found":0,"created":0,"updated":0,"skipped":0,"failed":0}
    try:
        headers = await get_headers()
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{GATEWAY_URL}/mge/service.sbr?serviceName=DbExplorerSP.loadRecords&outputType=json",
                headers=headers, json={"serviceName":"DbExplorerSP.loadRecords","requestBody":{"dataSet":{"rootEntity":"Parceiro","includePresentationFields":"S","offsetPage":"0","criteria":{"expression":{"$":"this.CLIENTE = 'S' AND this.ATIVO = 'S'"}},"entity":{"fieldset":{"list":"CODPARC,NOMEPARC,NOMEFANTASIA,CGC_CPF,TELEFONE"}}}}})
            r.raise_for_status()
            entities = r.json().get("responseBody",{}).get("entities",{}).get("entity",[])
            if isinstance(entities, dict): entities = [entities]
        stats["found"] = len(entities)
        for ent in entities:
            fm = _fmap(ent)
            codparc = fm.get("CODPARC","")
            nome = fm.get("NOMEPARC","")
            if not codparc or not nome: stats["skipped"]+=1; continue
            ext_id = f"SNK-CLI-{codparc}"
            try:
                ex = db.execute(text("SELECT id FROM recipients WHERE id=:id"),{"id":ext_id}).fetchone()
                if ex:
                    db.execute(text("UPDATE recipients SET name=:n,phone=:p,updated_at=NOW() WHERE id=:id"),{"id":ext_id,"n":nome,"p":fm.get("TELEFONE","")})
                    stats["updated"]+=1
                else:
                    db.execute(text("INSERT INTO recipients (id,name,address,lat,lng,phone,created_at) VALUES (:id,:n,'Endereço pendente',-3.1019,-60.0250,:p,NOW()) ON CONFLICT DO NOTHING"),{"id":ext_id,"n":nome,"p":fm.get("TELEFONE","")})
                    stats["created"]+=1
                db.commit()
            except Exception as e:
                db.rollback(); stats["failed"]+=1; logger.warning(f"Cliente {codparc}: {e}")
        _finish_run(db, rid, stats)
    except Exception as e:
        logger.exception("Erro sync customers")
        _finish_run(db, rid, stats, str(e))
    return stats

async def sync_orders(db: Session, dias: int = 1) -> dict:
    rid = _start_run(db, "orders")
    stats = {"found":0,"created":0,"updated":0,"skipped":0,"failed":0}
    try:
        headers = await get_headers()
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{GATEWAY_URL}/mge/service.sbr?serviceName=DbExplorerSP.loadRecords&outputType=json",
                headers=headers, json={"serviceName":"DbExplorerSP.loadRecords","requestBody":{"dataSet":{"rootEntity":"CabecalhoNota","includePresentationFields":"S","offsetPage":"0","criteria":{"expression":{"$":f"this.TIPMOV = 'V' AND this.STATUSNOTA = 'L' AND this.DTNEG >= SYSDATE - {dias}"}},"entity":{"fieldset":{"list":"NUNOTA,NUMNOTA,CODPARC,DTNEG,DTENTSAI,VLRNOTA,PESOBRUT,VOLUMEBRUT,OBSERVACAO"}}}}})
            r.raise_for_status()
            entities = r.json().get("responseBody",{}).get("entities",{}).get("entity",[])
            if isinstance(entities, dict): entities = [entities]
        stats["found"] = len(entities)
        for ent in entities:
            fm = _fmap(ent)
            nunota = fm.get("NUNOTA","")
            codparc = fm.get("CODPARC","")
            if not nunota: stats["skipped"]+=1; continue
            ext_id = f"SNK-{nunota}"
            try:
                ex = db.execute(text("SELECT id FROM orders WHERE external_id=:e"),{"e":ext_id}).fetchone()
                if ex: stats["skipped"]+=1; continue
                rec = db.execute(text("SELECT id,lat,lng FROM recipients WHERE id=:id"),{"id":f"SNK-CLI-{codparc}"}).fetchone()
                if not rec: stats["skipped"]+=1; continue
                db.execute(text("INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,weight_kg,volume_m3,tw_start,tw_end,status,notes,created_at) VALUES (:id,:ext,'sankhya',:rid,:lat,:lng,:kg,:m3,'08:00','18:00','pending',:notes,NOW()) ON CONFLICT (external_id) DO NOTHING"),
                    {"id":str(uuid4()),"ext":ext_id,"rid":rec.id,"lat":rec.lat,"lng":rec.lng,"kg":float(fm.get("PESOBRUT") or 0),"m3":float(fm.get("VOLUMEBRUT") or 0),"notes":fm.get("OBSERVACAO","")})
                db.commit(); stats["created"]+=1
            except Exception as e:
                db.rollback(); stats["failed"]+=1; logger.warning(f"Pedido {nunota}: {e}")
        _finish_run(db, rid, stats)
    except Exception as e:
        logger.exception("Erro sync orders")
        _finish_run(db, rid, stats, str(e))
    return stats

async def sync_fleet(db: Session) -> dict:
    rid = _start_run(db, "fleet")
    stats = {"found":0,"created":0,"updated":0,"skipped":0,"failed":0}
    try:
        headers = await get_headers()
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{GATEWAY_URL}/mge/service.sbr?serviceName=DbExplorerSP.loadRecords&outputType=json",
                headers=headers, json={"serviceName":"DbExplorerSP.loadRecords","requestBody":{"dataSet":{"rootEntity":"Veiculo","includePresentationFields":"S","offsetPage":"0","entity":{"fieldset":{"list":"CODVEI,PLACA,DESCRICAO,TIPOVEI,PESOMAX,VOLMAX,ATIVO"}}}}})
            r.raise_for_status()
            entities = r.json().get("responseBody",{}).get("entities",{}).get("entity",[])
            if isinstance(entities, dict): entities = [entities]
        stats["found"] = len(entities)
        for ent in entities:
            fm = _fmap(ent)
            placa = str(fm.get("PLACA","")).strip().upper()
            if not placa: stats["skipped"]+=1; continue
            status = "active" if fm.get("ATIVO")=="S" else "inactive"
            try:
                ex = db.execute(text("SELECT id FROM vehicles WHERE plate=:p"),{"p":placa}).fetchone()
                if ex:
                    db.execute(text("UPDATE vehicles SET model=:m,capacity_kg=:kg,capacity_m3=:m3,status=:s,updated_at=NOW() WHERE plate=:p"),
                        {"m":fm.get("DESCRICAO",placa),"kg":float(fm.get("PESOMAX") or 1000),"m3":float(fm.get("VOLMAX") or 8),"s":status,"p":placa})
                    stats["updated"]+=1
                else:
                    db.execute(text("INSERT INTO vehicles (id,plate,model,type,capacity_kg,capacity_m3,status,created_at) VALUES (:id,:p,:m,'truck',:kg,:m3,:s,NOW()) ON CONFLICT (plate) DO NOTHING"),
                        {"id":str(uuid4()),"p":placa,"m":fm.get("DESCRICAO",placa),"kg":float(fm.get("PESOMAX") or 1000),"m3":float(fm.get("VOLMAX") or 8),"s":status})
                    stats["created"]+=1
                db.commit()
            except Exception as e:
                db.rollback(); stats["failed"]+=1
        _finish_run(db, rid, stats)
    except Exception as e:
        _finish_run(db, rid, stats, str(e))
    return stats

async def publish_route_to_sankhya(db: Session, route_id: str) -> dict:
    try:
        headers = await get_headers()
        stops = db.execute(text("SELECT s.*,o.external_id FROM stops s JOIN orders o ON o.id=s.order_id WHERE s.route_id=:rid ORDER BY s.sequence"),{"rid":route_id}).fetchall()
        for s in stops:
            ext = getattr(s,"external_id","")
            if not ext or not ext.startswith("SNK-"): continue
            nunota = ext.replace("SNK-","")
            async with httpx.AsyncClient(timeout=10) as c:
                await c.post(f"{GATEWAY_URL}/mge/service.sbr?serviceName=CRUDServiceProvider.saveRecord&outputType=json",
                    headers=headers, json={"serviceName":"CRUDServiceProvider.saveRecord","requestBody":{"dataSet":{"rootEntity":"CabecalhoNota","dataRow":{"localFields":{"f":[{"@nome":"NUNOTA","$":nunota},{"@nome":"AD_ROTA_ID","$":route_id},{"@nome":"AD_SEQ_ENTREGA","$":str(s.sequence)},{"@nome":"AD_ETA","$":s.eta or ""}]}}}}})
        db.execute(text("UPDATE routes SET published_at=NOW() WHERE id=:id"),{"id":route_id})
        db.commit()
        return {"status":"ok","stops_published":len(stops)}
    except Exception as e:
        return {"status":"error","message":str(e)}
