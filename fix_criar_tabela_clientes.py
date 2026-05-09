from sqlalchemy import text
import sqlite3, os

# ── 1. Cria tabela clientes no banco ──────────────────────────────
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
conn.execute('''CREATE TABLE IF NOT EXISTS clientes (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  codparc    INTEGER UNIQUE NOT NULL,
  nome       TEXT,
  bairro     TEXT,
  cidade     TEXT,
  regiao     TEXT,
  cep        TEXT,
  endereco   TEXT,
  numero     TEXT,
  lat        REAL,
  lng        REAL,
  telefone   TEXT,
  ativo      TEXT DEFAULT 'S'
)''')
conn.commit()
conn.close()
print('Tabela clientes criada!')

# ── 2. Cria o router de clientes ──────────────────────────────────
router_path = r'C:\fleet-cloud\app\routers\clientes.py'
router_code = '''from fastapi import APIRouter, Depends
from app.database import get_db
import sqlite3

router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])

@router.get("")
def list_clientes(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM clientes ORDER BY nome")).fetchall()
    cols = [d[0] for d in db.execute(text("SELECT * FROM clientes LIMIT 0"))]
    return [dict(zip(cols, r)) for r in rows]

@router.get("/{codparc}")
def get_cliente(codparc: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute(text("SELECT * FROM clientes WHERE codparc=?"), (codparc,)).fetchone()
    if not row:
        return None
    cols = [d[0] for d in db.execute(text("SELECT * FROM clientes LIMIT 0"))]
    return dict(zip(cols, row))

@router.post("/bulk")
def bulk_import(clientes: list, db: sqlite3.Connection = Depends(get_db)):
    inserted = 0; updated = 0
    for c in clientes:
        existing = db.execute(text("SELECT id FROM clientes WHERE codparc=?"), (c.get("codparc"),)).fetchone()
        if existing:
            db.execute("""UPDATE clientes SET nome=?,bairro=?,cidade=?,regiao=?,
                cep=?,endereco=?,numero=?,lat=?,lng=?,telefone=?,ativo=? WHERE codparc=?""",
                (c.get("nome"),c.get("bairro"),c.get("cidade"),c.get("regiao"),
                 c.get("cep"),c.get("endereco"),c.get("numero"),c.get("lat"),
                 c.get("lng"),c.get("telefone"),c.get("ativo","S"),c.get("codparc")))
            updated += 1
        else:
            db.execute("""INSERT INTO clientes (codparc,nome,bairro,cidade,regiao,
                cep,endereco,numero,lat,lng,telefone,ativo)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (c.get("codparc"),c.get("nome"),c.get("bairro"),c.get("cidade"),
                 c.get("regiao"),c.get("cep"),c.get("endereco"),c.get("numero"),
                 c.get("lat"),c.get("lng"),c.get("telefone"),c.get("ativo","S")))
            inserted += 1
    db.commit()
    return {"inserted": inserted, "updated": updated, "total": len(clientes)}
'''
os.makedirs(os.path.dirname(router_path), exist_ok=True)
with open(router_path, 'w', encoding='utf-8') as f:
    f.write(router_code)
print('Router clientes criado!')

# ── 3. Registra no main.py ────────────────────────────────────────
main_path = r'C:\fleet-cloud\app\main.py'
with open(main_path, 'r') as f:
    main = f.read()

if 'clientes' not in main:
    main = main.replace(
        'from app.routers.ocorrencias import router as ocorrencias_router',
        'from app.routers.ocorrencias import router as ocorrencias_router\nfrom app.routers.clientes import router as clientes_router'
    )
    main = main.replace(
        'app.include_router(ocorrencias_router)',
        'app.include_router(ocorrencias_router)\napp.include_router(clientes_router)'
    )
    with open(main_path, 'w') as f:
        f.write(main)
    print('Router clientes registrado no main.py!')
else:
    print('Router já registrado!')

print('\nPasso 1 concluído! Execute fix_importar_base_clientes_js.py em seguida.')
