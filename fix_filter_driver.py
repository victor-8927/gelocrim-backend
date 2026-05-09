path = r'C:\fleet-cloud\app\routers\routes.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_fn = '''def list_routes(
    date_: Optional[date] = Query(None, alias="date"),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """
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

new_fn = '''def list_routes(
    date_: Optional[date] = Query(None, alias="date"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """
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
    # Motorista so ve suas proprias rotas
    if hasattr(current_user, 'role') and current_user.role == 'driver':
        driver_id = getattr(current_user, 'driver_id', None)
        if driver_id:
            wheres.append("r.driver_id = :driver_id")
            params["driver_id"] = str(driver_id)
    if wheres:
        q += " WHERE " + " AND ".join(wheres)'''

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print('Filtro por motorista adicionado!')
else:
    print('Padrao nao encontrado, verificando...')
    idx = content.find('def list_routes')
    print(content[idx:idx+300])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Reinicie a API!')
