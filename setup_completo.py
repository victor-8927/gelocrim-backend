"""
setup_completo.py
Execute: python setup_completo.py
Cria todos os arquivos necessários diretamente em C:\\fleet-cloud
"""
import os

BASE = r"C:\fleet-cloud"

files = {}

# ── app/integrations/sankhya/auth.py ──────────────────────────────────────
files["app/integrations/sankhya/auth.py"] = '''"""
Autenticacao Sankhya via API REST OAuth2 + fallback legado.
Configure no .env:
    SANKHYA_GATEWAY_URL, SANKHYA_CLIENT_ID, SANKHYA_CLIENT_SECRET,
    SANKHYA_TOKEN, SANKHYA_USERNAME, SANKHYA_PASSWORD
"""
import os, time, logging, httpx
logger = logging.getLogger(__name__)

GATEWAY_URL   = os.getenv("SANKHYA_GATEWAY_URL", "https://api.sankhya.com.br")
CLIENT_ID     = os.getenv("SANKHYA_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SANKHYA_CLIENT_SECRET", "")
X_TOKEN       = os.getenv("SANKHYA_TOKEN", "")
USERNAME      = os.getenv("SANKHYA_USERNAME", "")
PASSWORD      = os.getenv("SANKHYA_PASSWORD", "")

_cache = {"token": None, "expires_at": 0}

async def get_access_token() -> str:
    if _cache["token"] and time.time() < _cache["expires_at"] - 60:
        return _cache["token"]
    if CLIENT_ID and CLIENT_SECRET:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.post(f"{GATEWAY_URL}/auth/oauth/token",
                    headers={"Content-Type":"application/x-www-form-urlencoded","token":X_TOKEN},
                    data={"grant_type":"client_credentials","client_id":CLIENT_ID,"client_secret":CLIENT_SECRET})
                r.raise_for_status()
                d = r.json()
                _cache["token"] = d["access_token"]
                _cache["expires_at"] = time.time() + d.get("expires_in", 3600)
                return _cache["token"]
        except Exception as e:
            logger.warning(f"OAuth falhou: {e}")
    if USERNAME and PASSWORD:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.post(f"{GATEWAY_URL}/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json",
                    json={"serviceName":"MobileLoginSP.login","requestBody":{"NOMUSU":{"$":USERNAME},"INTERNO":{"$":"S"},"NUNOTA":{"$":"0"}}})
                r.raise_for_status()
                t = r.json().get("responseBody",{}).get("jsessionid",{}).get("$")
                if t:
                    _cache["token"] = t
                    _cache["expires_at"] = time.time() + 3600
                    return t
        except Exception as e:
            logger.error(f"Login legado falhou: {e}")
    raise RuntimeError("Nao foi possivel obter token Sankhya. Verifique credenciais no .env")

async def get_headers() -> dict:
    token = await get_access_token()
    return {"Authorization": f"Bearer {token}", "token": X_TOKEN, "Content-Type": "application/json"}

async def test_connection() -> dict:
    try:
        headers = await get_headers()
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{GATEWAY_URL}/mge/service.sbr?serviceName=AwsUtil.ping&outputType=json", headers=headers)
            if r.status_code < 400:
                return {"status": "ok", "message": f"Conexao Sankhya estabelecida! ({GATEWAY_URL})"}
            return {"status": "error", "message": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''

# ── app/integrations/sankhya/sync.py ──────────────────────────────────────
files["app/integrations/sankhya/sync.py"] = '''"""
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
        db.execute(text("INSERT INTO integration_runs (id,source,entity,status,started_at) VALUES (:id,\'sankhya\',:e,\'running\',NOW())"), {"id":rid,"e":entity})
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
                headers=headers, json={"serviceName":"DbExplorerSP.loadRecords","requestBody":{"dataSet":{"rootEntity":"Parceiro","includePresentationFields":"S","offsetPage":"0","criteria":{"expression":{"$":"this.CLIENTE = \'S\' AND this.ATIVO = \'S\'"}},"entity":{"fieldset":{"list":"CODPARC,NOMEPARC,NOMEFANTASIA,CGC_CPF,TELEFONE"}}}}})
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
                    db.execute(text("INSERT INTO recipients (id,name,address,lat,lng,phone,created_at) VALUES (:id,:n,\'Endereço pendente\',-3.1019,-60.0250,:p,NOW()) ON CONFLICT DO NOTHING"),{"id":ext_id,"n":nome,"p":fm.get("TELEFONE","")})
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
                headers=headers, json={"serviceName":"DbExplorerSP.loadRecords","requestBody":{"dataSet":{"rootEntity":"CabecalhoNota","includePresentationFields":"S","offsetPage":"0","criteria":{"expression":{"$":f"this.TIPMOV = \'V\' AND this.STATUSNOTA = \'L\' AND this.DTNEG >= SYSDATE - {dias}"}},"entity":{"fieldset":{"list":"NUNOTA,NUMNOTA,CODPARC,DTNEG,DTENTSAI,VLRNOTA,PESOBRUT,VOLUMEBRUT,OBSERVACAO"}}}}})
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
                db.execute(text("INSERT INTO orders (id,external_id,source,recipient_id,lat,lng,weight_kg,volume_m3,tw_start,tw_end,status,notes,created_at) VALUES (:id,:ext,\'sankhya\',:rid,:lat,:lng,:kg,:m3,\'08:00\',\'18:00\',\'pending\',:notes,NOW()) ON CONFLICT (external_id) DO NOTHING"),
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
                    db.execute(text("INSERT INTO vehicles (id,plate,model,type,capacity_kg,capacity_m3,status,created_at) VALUES (:id,:p,:m,\'truck\',:kg,:m3,:s,NOW()) ON CONFLICT (plate) DO NOTHING"),
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
'''

# ── app/routers/sync.py ────────────────────────────────────────────────────
files["app/routers/sync.py"] = '''"""
app/routers/sync.py — Endpoints de integração Sankhya
"""
import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/v1/sync", tags=["Integração Sankhya"])

_state = {"running": False, "last_result": None, "last_run_at": None}

@router.get("/sankhya/status")
def sync_status(_=Depends(get_current_user)):
    return _state

@router.get("/sankhya/test")
async def test_connection(_=Depends(get_current_user)):
    try:
        from app.integrations.sankhya.auth import test_connection as _t
        return await _t()
    except Exception as e:
        try:
            from app.sankhya_sync import get_sankhya_engine
            from sqlalchemy import text
            with get_sankhya_engine().connect() as c:
                c.execute(text("SELECT 1"))
            return {"status": "ok", "message": "Conexão banco Sankhya OK!"}
        except Exception as e2:
            return {"status": "error", "message": f"API: {e} | Banco: {e2}"}

@router.post("/sankhya")
async def sync_sankhya(background_tasks: BackgroundTasks, dias: int = 1,
    entities: str = "all", _=Depends(require_admin), db: Session = Depends(get_db)):
    if _state["running"]:
        return {"status": "already_running"}

    def _run():
        _state["running"] = True
        result = {"timestamp": datetime.now().isoformat(), "entities": {}, "errors": []}
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                from app.integrations.sankhya import sync as snk
                if entities in ("all","customers"):
                    result["entities"]["customers"] = loop.run_until_complete(snk.sync_customers(db))
                if entities in ("all","fleet"):
                    result["entities"]["fleet"] = loop.run_until_complete(snk.sync_fleet(db))
                if entities in ("all","orders"):
                    result["entities"]["orders"] = loop.run_until_complete(snk.sync_orders(db, dias=dias))
            except Exception as e:
                result["errors"].append(f"API REST falhou: {e} — tentando banco direto...")
                try:
                    from app.sankhya_sync import run_sync
                    result["entities"] = run_sync(dias_pedidos=dias)
                except Exception as e2:
                    result["errors"].append(str(e2))
            loop.close()
        except Exception as e:
            result["errors"].append(str(e))
        finally:
            _state["running"] = False
            _state["last_result"] = result
            _state["last_run_at"] = datetime.now().isoformat()

    background_tasks.add_task(_run)
    return {"status": "started", "message": f"Sync iniciado — {entities} — últimos {dias} dia(s)"}

@router.get("/sankhya/runs")
def get_runs(limit: int = 20, _=Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import text
    try:
        rows = db.execute(text("""
            SELECT id,entity,status,records_found,records_created,records_updated,
                   records_failed,error_message,started_at,finished_at
            FROM integration_runs ORDER BY started_at DESC LIMIT :l
        """), {"l": limit}).fetchall()
        return [dict(r._mapping) for r in rows]
    except:
        return []

@router.post("/sankhya/publish-route/{route_id}")
async def publish_route(route_id: str, _=Depends(require_admin), db: Session = Depends(get_db)):
    try:
        from app.integrations.sankhya.sync import publish_route_to_sankhya
        return await publish_route_to_sankhya(db, route_id)
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''

# ── app/integrations/__init__.py ───────────────────────────────────────────
files["app/integrations/__init__.py"] = ""
files["app/integrations/sankhya/__init__.py"] = ""

# ── Criar todos os arquivos ────────────────────────────────────────────────
print("Criando arquivos em C:\\fleet-cloud...\n")
for rel_path, content in files.items():
    full_path = os.path.join(BASE, rel_path.replace("/", "\\"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {rel_path}")

# ── Criar/atualizar .env se não existir ───────────────────────────────────
env_path = os.path.join(BASE, ".env")
if not os.path.exists(env_path):
    env_content = """DATABASE_URL=sqlite:///C:/fleet-cloud/fleet.db
JWT_SECRET=gelocrim-chave-secreta-2026
DEPOT_LAT=-3.1019
DEPOT_LNG=-60.0250
VRP_TIME_LIMIT_SEC=30
SANKHYA_GATEWAY_URL=https://api.sankhya.com.br
SANKHYA_CLIENT_ID=
SANKHYA_CLIENT_SECRET=
SANKHYA_TOKEN=
SANKHYA_USERNAME=
SANKHYA_PASSWORD=
SANKHYA_HOST=localhost
SANKHYA_PORT=5432
SANKHYA_DB=sankhya
SANKHYA_USER=
SANKHYA_PASS=
GOOGLE_MAPS_KEY=
"""
    with open(env_path, "w") as f:
        f.write(env_content)
    print(f"\n  ✅ .env criado (preencha as credenciais)")
else:
    print(f"\n  ℹ️  .env já existe (não alterado)")

# ── Adicionar tabelas novas ao banco ──────────────────────────────────────
print("\nAdicionando novas tabelas ao banco...")
try:
    from app.database import engine_sync
    from sqlalchemy import text
    with engine_sync.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS integration_runs (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL DEFAULT 'sankhya',
                entity TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'running',
                records_found INTEGER DEFAULT 0,
                records_created INTEGER DEFAULT 0,
                records_updated INTEGER DEFAULT 0,
                records_skipped INTEGER DEFAULT 0,
                records_failed INTEGER DEFAULT 0,
                error_message TEXT,
                started_at TEXT DEFAULT (datetime('now')),
                finished_at TEXT,
                duration_sec REAL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS integration_errors (
                id TEXT PRIMARY KEY,
                run_id TEXT,
                entity TEXT NOT NULL,
                external_id TEXT,
                error TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sync_checkpoints (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL DEFAULT 'sankhya',
                entity TEXT NOT NULL UNIQUE,
                last_sync_at TEXT,
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS occurrences (
                id TEXT PRIMARY KEY,
                route_id TEXT,
                stop_id TEXT,
                order_id TEXT,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'open',
                created_at TEXT DEFAULT (datetime('now'))
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS route_events (
                id TEXT PRIMARY KEY,
                route_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """))
    print("  ✅ Novas tabelas criadas!")
except Exception as e:
    print(f"  ⚠️  Tabelas: {e}")

print("\n🎉 Setup completo!")
print("\nPróximos passos:")
print("  1. Preencha C:\\fleet-cloud\\.env com suas credenciais")
print("  2. Execute: iniciar_api.bat")
print("  3. Execute: iniciar_frontend.bat")
print("  4. Acesse: http://localhost:8080/gelocrim_v1.html")
