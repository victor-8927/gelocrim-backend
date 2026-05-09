caminho = r"C:\fleet-cloud\app\routers\routes.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

# 1. Corrigir endpoint /iniciar para aceitar km_inicial
antigo = """@router.post("/{route_id}/iniciar")
def iniciar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='executing', started_at=:now WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat()})
    db.commit()
    return {"status":"executing"}"""

novo = """class IniciarBody(BaseModel):
    km_inicial: Optional[int] = None

@router.post("/{route_id}/iniciar")
def iniciar_rota(route_id: str, body: IniciarBody = IniciarBody(), db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='executing', started_at=:now, km_inicial=:km WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat(),"km":body.km_inicial})
    db.commit()
    return {"status":"executing"}"""

if antigo in data:
    data = data.replace(antigo, novo)
    print("OK1 - iniciar salva km_inicial!")
else:
    print("ERRO1")

# 2. Corrigir endpoint /finalizar para aceitar km_final
antigo2 = """@router.post("/{route_id}/finalizar")
def finalizar_rota(route_id: str, db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='done', finished_at=:now WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat()})
    db.commit()
    return {"status":"done"}"""

novo2 = """class FinalizarBody(BaseModel):
    km_final: Optional[int] = None

@router.post("/{route_id}/finalizar")
def finalizar_rota(route_id: str, body: FinalizarBody = FinalizarBody(), db: Session = Depends(get_db)):
    db.execute(text(
        "UPDATE routes SET status='done', finished_at=:now, km_final=:km WHERE id=:id"
    ),{"id":route_id,"now":datetime.now().isoformat(),"km":body.km_final})
    db.commit()
    return {"status":"done"}"""

if antigo2 in data:
    data = data.replace(antigo2, novo2)
    print("OK2 - finalizar salva km_final!")
else:
    print("ERRO2")

# 3. Adicionar km_inicial e km_final no list_routes
antigo3 = "               r.status, r.planned_start, r.planned_end, r.total_distance_km,"
novo3   = "               r.status, r.planned_start, r.planned_end, r.total_distance_km, r.km_inicial, r.km_final,"

if antigo3 in data:
    data = data.replace(antigo3, novo3)
    print("OK3 - km adicionado na listagem!")
else:
    print("ERRO3")

with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("Salvo!")
