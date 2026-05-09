import sys, os, uuid
from datetime import datetime, timezone

sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text
import bcrypt

def now_str():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

motoristas = [
    {'nome': 'JAVIER DAVID LUNA',              'email': 'javier@gelocrim.com',    'cpf': '00000000001'},
    {'nome': 'ROLDAO DUARTE',                   'email': 'roldao@gelocrim.com',    'cpf': '00000000002'},
    {'nome': 'HOMERO GUSMAO TORRES',            'email': 'homero@gelocrim.com',    'cpf': '00000000003'},
    {'nome': 'ALEX CEZAR MENDONCA',             'email': 'alex@gelocrim.com',      'cpf': '00000000004'},
    {'nome': 'MAICON ALEXANDER XAVIER',         'email': 'maicon@gelocrim.com',    'cpf': '00000000005'},
    {'nome': 'TERCEIRO (DANIEL LIMA DE SOUZA)', 'email': 'terceiro@gelocrim.com',  'cpf': '00000000006'},
    {'nome': 'TESTE (INTEGRACAO)',              'email': 'teste@gelocrim.com',     'cpf': '00000000007'},
]

SENHA_PADRAO = 'Gelocrim2026'

with engine_sync.begin() as conn:
    cols = conn.execute(text('PRAGMA table_info(users)')).fetchall()
    user_cols = [c[1] for c in cols]
    print('Colunas users:', user_cols)
    print()

    for m in motoristas:
        ts = now_str()

        # Driver
        existe_d = conn.execute(text("SELECT id FROM drivers WHERE cpf=:cpf"), {'cpf': m['cpf']}).fetchone()
        if existe_d:
            driver_id = existe_d[0]
        else:
            driver_id = str(uuid.uuid4())
            conn.execute(text(
                "INSERT INTO drivers (id, name, cpf, status, created_at, updated_at) VALUES (:id,:name,:cpf,'active',:ts,:ts)"
            ), {'id': driver_id, 'name': m['nome'], 'cpf': m['cpf'], 'ts': ts})

        # User
        existe_u = conn.execute(text("SELECT id FROM users WHERE email=:e"), {'e': m['email']}).fetchone()
        if existe_u:
            print(f'Ja existe: {m["email"]}')
            continue

        user_id = str(uuid.uuid4())
        pwd     = hash_senha(SENHA_PADRAO)

        # Monta insert dinamico baseado nas colunas existentes
        fields = ['id', 'name', 'email', 'password_hash', 'role', 'is_active', 'created_at']
        values = [user_id, m['nome'], m['email'], pwd, 'driver', 1, ts]

        if 'driver_id' in user_cols:
            fields.append('driver_id')
            values.append(driver_id)
        if 'updated_at' in user_cols:
            fields.append('updated_at')
            values.append(ts)

        placeholders = ','.join([f':{f}' for f in fields])
        params = dict(zip(fields, values))

        conn.execute(text(f"INSERT INTO users ({','.join(fields)}) VALUES ({placeholders})"), params)
        print(f'Criado: {m["nome"]}')
        print(f'  Email: {m["email"]}  |  Senha: {SENHA_PADRAO}')

print('\nConcluido!')
