# ── BACKEND: adicionar 3 novos campos de foto ──────────────────
PATH_BACKEND = r'C:\fleet-cloud\app\routers\routes.py'

with open(PATH_BACKEND, encoding='utf-8') as f:
    content = f.read()

OLD = "      foto_base64: Optional[str] = None"
NEW = """      foto_base64: Optional[str] = None
      foto_boleto_base64: Optional[str] = None
      foto_comodato_base64: Optional[str] = None
      foto_outros_base64: Optional[str] = None"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK: backend modelo atualizado!")

# Adicionar salvamento das fotos extras após o bloco de foto_base64
OLD_FOTO = """    if body.foto_base64:
            header, data = body.foto_base64.split(",",1)"""
NEW_FOTO = """    if body.foto_boleto_base64:
        try:
            header, data = body.foto_boleto_base64.split(",",1)
            img_bytes = base64.b64decode(data)
            fname = f"boleto_{stop_id}.jpg"
            fpath = os.path.join("uploads", fname)
            os.makedirs("uploads", exist_ok=True)
            with open(fpath, "wb") as f2: f2.write(img_bytes)
            fields.append("foto_boleto_url=:foto_boleto_url")
            params["foto_boleto_url"] = f"/uploads/{fname}"
        except: pass
    if body.foto_comodato_base64:
        try:
            header, data = body.foto_comodato_base64.split(",",1)
            img_bytes = base64.b64decode(data)
            fname = f"comodato_{stop_id}.jpg"
            fpath = os.path.join("uploads", fname)
            with open(fpath, "wb") as f2: f2.write(img_bytes)
            fields.append("foto_comodato_url=:foto_comodato_url")
            params["foto_comodato_url"] = f"/uploads/{fname}"
        except: pass
    if body.foto_base64:
            header, data = body.foto_base64.split(",",1)"""

if OLD_FOTO in content:
    content = content.replace(OLD_FOTO, NEW_FOTO)
    print("OK: backend salvamento fotos extras!")

with open(PATH_BACKEND, 'w', encoding='utf-8') as f:
    f.write(content)

# Adicionar colunas na tabela se não existirem
ADD_COLS = r"""
import sys
sys.path.insert(0, r'C:\fleet-cloud')
from app.database import engine_sync
from sqlalchemy import text
with engine_sync.connect() as conn:
    for col in ['foto_boleto_url', 'foto_comodato_url', 'foto_outros_url']:
        try:
            conn.execute(text(f'ALTER TABLE route_stops ADD COLUMN {col} TEXT'))
            conn.commit()
            print(f'OK: coluna {col} adicionada!')
        except:
            print(f'coluna {col} ja existe')
"""

with open(r'C:\fleet-cloud\add_foto_cols.py', 'w') as f:
    f.write(ADD_COLS)
print("Script add_foto_cols.py criado!")

# ── APP: quadradinhos maiores ──────────────────────────────────
PATH_APP = r'C:\gelocrim-motorista\screens\EntregaScreen.js'

with open(PATH_APP, encoding='utf-8') as f:
    app = f.read()

# Corrigir tamanho dos quadradinhos
replacements = [
    ("  fotoQuadrado: { width:'48%', aspectRatio:0.9,",
     "  fotoQuadrado: { width:'48%', height:150,"),
    ("  fotoQuadradoOk: { borderColor:'#00FF88', borderStyle:'solid', backgroundColor:'rgba(0,255,136,0.1)' },",
     "  fotoQuadradoOk: { borderColor:'#00FF88', borderStyle:'solid', borderWidth:2, backgroundColor:'rgba(0,255,136,0.1)' },"),
]

for old, new in replacements:
    if old in app:
        app = app.replace(old, new)
        print(f"OK: {old[:50]}...")

# Corrigir envio das 4 fotos no confirmarEntrega
OLD_BODY = """          body: JSON.stringify({
          status: 'completed',
          ata: new Date().toISOString(),
          lat_confirmacao: gps?.latitude,
          lng_confirmacao: gps?.longitude,
          foto_base64: fotoB64,
        }),"""

NEW_BODY = """          body: JSON.stringify({
          status: 'completed',
          ata: new Date().toISOString(),
          lat_confirmacao: gps?.latitude,
          lng_confirmacao: gps?.longitude,
          foto_base64: fotoB64,
          foto_boleto_base64: fotoBoleto,
          foto_comodato_base64: fotoComodato,
        }),"""

if OLD_BODY in app:
    app = app.replace(OLD_BODY, NEW_BODY)
    print("OK: envio 4 fotos no confirmarEntrega!")

with open(PATH_APP, 'w', encoding='utf-8') as f:
    f.write(app)

print("\nAgora rode: python add_foto_cols.py em C:\\fleet-cloud")
print("Depois reinicie backend e Expo!")
