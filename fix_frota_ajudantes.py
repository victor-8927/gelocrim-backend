import sys, os, uuid
from datetime import datetime, timezone

sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text

def now_str():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

with engine_sync.begin() as conn:
    # Adiciona coluna tipo se nao existir
    try:
        conn.execute(text("ALTER TABLE drivers ADD COLUMN tipo TEXT DEFAULT 'motorista'"))
        print('Coluna tipo adicionada!')
    except:
        print('Coluna tipo ja existe!')

    # Adiciona coluna ajudante1_id e ajudante2_id na tabela routes
    try:
        conn.execute(text("ALTER TABLE routes ADD COLUMN ajudante1_id TEXT"))
        print('Coluna ajudante1_id adicionada!')
    except:
        print('Coluna ajudante1_id ja existe!')

    try:
        conn.execute(text("ALTER TABLE routes ADD COLUMN ajudante2_id TEXT"))
        print('Coluna ajudante2_id adicionada!')
    except:
        print('Coluna ajudante2_id ja existe!')

    # Atualiza motoristas existentes com tipo=motorista
    conn.execute(text("UPDATE drivers SET tipo='motorista' WHERE tipo IS NULL"))
    print('Motoristas atualizados com tipo=motorista!')

    # Cria alguns ajudantes de exemplo
    ajudantes = [
        {'nome': 'AJUDANTE 1', 'cpf': '10000000001'},
        {'nome': 'AJUDANTE 2', 'cpf': '10000000002'},
        {'nome': 'AJUDANTE 3', 'cpf': '10000000003'},
    ]

    for a in ajudantes:
        existe = conn.execute(text("SELECT id FROM drivers WHERE cpf=:cpf"), {'cpf': a['cpf']}).fetchone()
        if not existe:
            conn.execute(text("""
                INSERT INTO drivers (id, name, cpf, status, tipo, created_at, updated_at)
                VALUES (:id, :name, :cpf, 'active', 'ajudante', :ts, :ts)
            """), {'id': str(uuid.uuid4()), 'name': a['nome'], 'cpf': a['cpf'], 'ts': now_str()})
            print(f'Ajudante criado: {a["nome"]}')
        else:
            print(f'Ajudante ja existe: {a["nome"]}')

print('\nConcluido! Reinicie a API.')
