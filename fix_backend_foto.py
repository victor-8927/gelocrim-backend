import sqlite3, os

# 1. Adiciona coluna foto_url na tabela route_stops
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cols = [r[1] for r in conn.execute("PRAGMA table_info(route_stops)").fetchall()]
if 'foto_url' not in cols:
    conn.execute("ALTER TABLE route_stops ADD COLUMN foto_url TEXT")
    conn.commit()
    print('Coluna foto_url adicionada!')
else:
    print('foto_url já existe!')
conn.close()

# 2. Cria pasta para salvar fotos
pasta = r'C:\fleet-cloud\fotos'
os.makedirs(pasta, exist_ok=True)
print(f'Pasta fotos: {pasta}')

# 3. Atualiza o endpoint PATCH no router de rotas
path = r'C:\fleet-cloud\app\routers\routes.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona foto_base64 no StopUpdate
old_model = """class StopUpdate(BaseModel):
    status: Optional[str] = None
    ata: Optional[str] = None
    atd: Optional[str] = None
    lat_confirmacao: Optional[float] = None
    lng_confirmacao: Optional[float] = None
    failure_reason: Optional[str] = None"""

new_model = """class StopUpdate(BaseModel):
    status: Optional[str] = None
    ata: Optional[str] = None
    atd: Optional[str] = None
    lat_confirmacao: Optional[float] = None
    lng_confirmacao: Optional[float] = None
    failure_reason: Optional[str] = None
    foto_base64: Optional[str] = None"""

if old_model in content:
    content = content.replace(old_model, new_model)
    print('StopUpdate atualizado!')

# Adiciona import base64 e os no topo
if 'import base64' not in content:
    content = content.replace(
        'import uuid',
        'import uuid\nimport base64 as b64\nimport os'
    )
    print('Imports adicionados!')

# Adiciona lógica de salvar foto no endpoint PATCH
old_patch = """    if body.failure_reason:  fields.append("failure_reason = :fr");     params["fr"] = body.failure_reason
    if not fields:
        raise HTTPException(400, "Nenhum campo")"""

new_patch = """    if body.failure_reason:  fields.append("failure_reason = :fr");     params["fr"] = body.failure_reason
    # Salva foto se enviada
    foto_url = None
    if body.foto_base64:
        try:
            header, data = body.foto_base64.split(',', 1)
            img_data = b64.b64decode(data)
            foto_nome = f"{stop_id}.jpg"
            foto_path = os.path.join(r'C:\\fleet-cloud\\fotos', foto_nome)
            with open(foto_path, 'wb') as f:
                f.write(img_data)
            foto_url = f"/fotos/{foto_nome}"
            fields.append("foto_url = :foto_url")
            params["foto_url"] = foto_url
        except Exception as e:
            pass
    if not fields:
        raise HTTPException(400, "Nenhum campo")"""

if old_patch in content:
    content = content.replace(old_patch, new_patch)
    print('Endpoint PATCH atualizado com foto!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# 4. Serve a pasta fotos estaticamente no main.py
main_path = r'C:\fleet-cloud\app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main = f.read()

if 'StaticFiles' not in main:
    main = main.replace(
        'from fastapi.responses import FileResponse',
        'from fastapi.responses import FileResponse\nfrom fastapi.staticfiles import StaticFiles'
    )
    main = main.replace(
        'app.include_router(auth_router)',
        'app.mount("/fotos", StaticFiles(directory=r"C:\\fleet-cloud\\fotos"), name="fotos")\napp.include_router(auth_router)'
    )
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main)
    print('main.py atualizado com StaticFiles!')
else:
    print('StaticFiles já configurado!')

print('Pronto! Reinicie o servidor.')
