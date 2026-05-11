from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/cron", tags=["Cron"])

@router.post("/fechar-rotas")
def fechar_rotas(db: Session = Depends(get_db)):
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result = db.execute(text("""
        UPDATE routes SET status='done', finished_at=:now
        WHERE status IN ('executing', 'executando')
        AND route_date <= :ontem
    """), {"now": datetime.now().isoformat(), "ontem": ontem})
    db.commit()
    return {"fechadas": result.rowcount}

@router.post("/limpar-gps")
def limpar_gps(db: Session = Depends(get_db)):
    limite = (datetime.now() - timedelta(days=30)).isoformat()
    result = db.execute(text("""
        DELETE FROM route_gps WHERE ts < :limite
    """), {"limite": limite})
    db.commit()
    return {"deletados": result.rowcount}
