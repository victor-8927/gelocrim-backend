"""
Cria o primeiro usuário administrador no banco Supabase.
Execute: python criar_admin.py
"""
import asyncio
from passlib.context import CryptContext
from sqlalchemy import text
from app.database import engine_async, init_schema

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def main():
    print("\n=== Criar usuário administrador ===\n")
    nome  = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    await init_schema()

    async with engine_async.begin() as conn:
        ex = await conn.execute(text("SELECT id FROM users WHERE email=:e"), {"e": email})
        if ex.fetchone():
            print(f"\nUsuário {email} já existe!")
            return
        from uuid import uuid4
        await conn.execute(text("""
            INSERT INTO users (id, name, email, password_hash, role)
            VALUES (:id, :name, :email, :hash, 'admin')
        """), {"id": str(uuid4()), "name": nome, "email": email, "hash": pwd_ctx.hash(senha)})

    print(f"\nAdministrador criado com sucesso!")
    print(f"Email: {email}")
    print(f"Agora execute: iniciar.bat")

asyncio.run(main())
