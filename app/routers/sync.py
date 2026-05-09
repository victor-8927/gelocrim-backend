"""
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
