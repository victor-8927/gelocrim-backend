import traceback
try:
    from app.database import get_db
    from sqlalchemy import text
    from passlib.context import CryptContext

    db = next(get_db())
    row = db.execute(
        text("SELECT id,name,email,password_hash,role,is_active,driver_id FROM users WHERE email=:e"),
        {"e": "distribuicaogelorotas@gmail.com"}
    ).fetchone()

    if not row:
        print("ERRO: Usuario nao encontrado no banco!")
    else:
        print("Usuario encontrado:", row.email, "| role:", row.role)
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        ok = pwd.verify("Fleet2026", row.password_hash)
        print("Senha correta:", ok)
        print("Hash salvo:", row.password_hash[:30], "...")
except Exception:
    traceback.print_exc()
