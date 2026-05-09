path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona filtro por driver_id na query de rotas
old_query = '''    q = """
        SELECT r.id AS route_id, v.plate AS vehicle_plate,
               d.name AS driver_name, r.status,
               r.total_stops, r.total_distance_km,
               r.planned_start, r.planned_end, r.route_date,
               COUNT(CASE WHEN s.status='completed' THEN 1 END) AS stops_completed,
               COUNT(CASE WHEN s.status='failed' THEN 1 END) AS stops_failed
        FROM routes r
        LEFT JOIN vehicles v ON v.id = r.vehicle_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        LEFT JOIN stops s ON s.route_id = r.id
        GROUP BY r.id
    """
    params = {}
    if date_:
        q += " WHERE r.route_date = :d"
        params["d"] = str(date_)'''

new_query = '''    q = """
        SELECT r.id AS route_id, v.plate AS vehicle_plate,
               d.name AS driver_name, r.status,
               r.total_stops, r.total_distance_km,
               r.planned_start, r.planned_end, r.route_date,
               r.driver_id,
               COUNT(CASE WHEN s.status='completed' THEN 1 END) AS stops_completed,
               COUNT(CASE WHEN s.status='failed' THEN 1 END) AS stops_failed
        FROM routes r
        LEFT JOIN vehicles v ON v.id = r.vehicle_id
        LEFT JOIN drivers d ON d.id = r.driver_id
        LEFT JOIN stops s ON s.route_id = r.id
        GROUP BY r.id
    """
    params = {}
    wheres = []
    if date_:
        wheres.append("r.route_date = :d")
        params["d"] = str(date_)
    if wheres:
        q += " WHERE " + " AND ".join(wheres)'''

if old_query in content:
    content = content.replace(old_query, new_query)
    print('Query de rotas atualizada com driver_id!')
else:
    print('Padrao da query nao encontrado!')

# Adiciona driver_id no INSERT da rota
old_insert = '''        db.execute(text("""
            INSERT INTO routes (id,vehicle_id,route_date,status,total_distance_km,
                total_stops,planned_start,planned_end,optimized_at,created_at,updated_at)
            VALUES (:id,:vid,:d,:st,:dist,:ts2,:ps,:pe,:ts,:ts,:ts)
        """), {"id": rid, "vid": str(v["id"]), "d": str(body.route_date),'''

new_insert = '''        driver_id = str(body.driver_id) if body.driver_id else None
        db.execute(text("""
            INSERT INTO routes (id,vehicle_id,driver_id,route_date,status,total_distance_km,
                total_stops,planned_start,planned_end,optimized_at,created_at,updated_at)
            VALUES (:id,:vid,:did,:d,:st,:dist,:ts2,:ps,:pe,:ts,:ts,:ts)
        """), {"id": rid, "vid": str(v["id"]), "did": driver_id, "d": str(body.route_date),'''

if old_insert in content:
    content = content.replace(old_insert, new_insert)
    print('driver_id adicionado no INSERT da rota!')

# Adiciona driver_id no schema do body
old_schema = '''class OptimizeRequest(BaseModel):
    route_date: date
    vehicle_id: UUID
    order_ids: List[UUID]
    tw_start: Optional[str] = "07:30"
    tw_end:   Optional[str] = "18:00"'''

new_schema = '''class OptimizeRequest(BaseModel):
    route_date: date
    vehicle_id: UUID
    order_ids: List[UUID]
    driver_id: Optional[UUID] = None
    tw_start: Optional[str] = "07:30"
    tw_end:   Optional[str] = "18:00"'''

if old_schema in content:
    content = content.replace(old_schema, new_schema)
    print('driver_id adicionado no schema!')

# Adiciona filtro por driver no endpoint de rotas para o app motorista
# O app motorista envia o token e filtramos pelo driver_id do usuario logado
old_get_routes = '''@router.get("")
def list_routes(
    date_: Optional[date] = Query(None, alias="date"),
    _=Depends(get_current_user),
    db: Session = Depends(get_db)
):'''

new_get_routes = '''@router.get("")
def list_routes(
    date_: Optional[date] = Query(None, alias="date"),
    driver_id: Optional[str] = Query(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):'''

if old_get_routes in content:
    content = content.replace(old_get_routes, new_get_routes)
    print('Parametro driver_id adicionado no endpoint!')

# Adiciona filtro automatico por driver quando o role for 'driver'
old_filter = '''    if wheres:
        q += " WHERE " + " AND ".join(wheres)'''

new_filter = '''    # Se o usuario for motorista, filtra automaticamente pelas suas rotas
    if hasattr(current_user, 'role') and current_user.role == 'driver':
        if hasattr(current_user, 'driver_id') and current_user.driver_id:
            wheres.append("r.driver_id = :did")
            params["did"] = str(current_user.driver_id)
    elif driver_id:
        wheres.append("r.driver_id = :did")
        params["did"] = driver_id

    if wheres:
        q += " WHERE " + " AND ".join(wheres)'''

if old_filter in content:
    content = content.replace(old_filter, new_filter)
    print('Filtro automatico por motorista adicionado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nRoutes.py atualizado!')
print('Reinicie a API!')
