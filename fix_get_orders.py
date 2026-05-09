orders_path = r'C:\fleet-cloud\app\routers\orders.py'

with open(orders_path, 'r') as f:
    content = f.read()

old_get = '''@router.get("", response_model=list[OrderOut])
def list_orders(
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """SELECT o.id, o.external_id, r.name AS recipient_name, r.address,
               o.lat, o.lng, o.weight_kg, o.volume_m3, o.tw_start, o.tw_end, o.status, o.created_at
        FROM orders o JOIN recipients r ON r.id = o.recipient_id"""
    params = {"limit": limit}
    if status:
        q += " WHERE o.status = :status"
        params["status"] = status
    q += " ORDER BY o.created_at DESC LIMIT :limit"
    rows = db.execute(text(q), params).fetchall()
    return [dict(r._mapping) for r in rows]'''

new_get = '''@router.get("", response_model=list[OrderOut])
def list_orders(
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    _=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = """SELECT o.id, o.external_id,
               COALESCE(o.recipient_name, r.name, 'Cliente') AS recipient_name,
               COALESCE(o.address, r.address, 'Manaus - AM') AS address,
               COALESCE(o.lat, r.lat) AS lat,
               COALESCE(o.lng, r.lng) AS lng,
               o.weight_kg, o.volume_m3,
               COALESCE(o.time_window_start, o.tw_start, '07:30') AS tw_start,
               COALESCE(o.time_window_end, o.tw_end, '18:00') AS tw_end,
               o.status, o.created_at,
               o.delivery_date, o.order_type, o.total_value, o.regiao, o.priority
        FROM orders o
        LEFT JOIN recipients r ON r.id = o.recipient_id"""
    params = {"limit": limit}
    if status:
        q += " WHERE o.status = :status"
        params["status"] = status
    q += " ORDER BY o.created_at DESC LIMIT :limit"
    rows = db.execute(text(q), params).fetchall()
    return [dict(r._mapping) for r in rows]'''

if old_get in content:
    content = content.replace(old_get, new_get)
    print('GET /orders corrigido com LEFT JOIN!')
else:
    print('Padrão não encontrado, corrigindo via regex...')
    import re
    content = re.sub(
        r'(@router\.get\("", response_model=list\[OrderOut\]\).*?FROM orders o )JOIN( recipients r ON r\.id = o\.recipient_id""")',
        r'\1LEFT JOIN\2',
        content, flags=re.DOTALL
    )
    # Adiciona COALESCE para recipient_name
    content = content.replace(
        'r.name AS recipient_name, r.address,',
        "COALESCE(o.recipient_name, r.name, 'Cliente') AS recipient_name,\n               COALESCE(o.address, r.address, 'Manaus - AM') AS address,"
    )
    print('Corrigido via regex!')

# Atualiza também o OrderOut para incluir novos campos
old_out = '''class OrderOut(BaseModel):
    id: str
    external_id: Optional[str]
    recipient_name: str
    address: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    weight_kg: float
    volume_m3: float
    tw_start: Optional[str]
    tw_end: Optional[str]
    status: str
    created_at: str
    model_config = {"from_attributes": True}'''

new_out = '''class OrderOut(BaseModel):
    id: str
    external_id: Optional[str] = None
    recipient_name: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    weight_kg: float = 0
    volume_m3: float = 0
    tw_start: Optional[str] = None
    tw_end: Optional[str] = None
    status: str = "pending"
    created_at: Optional[str] = None
    delivery_date: Optional[str] = None
    order_type: Optional[str] = None
    total_value: Optional[float] = None
    regiao: Optional[str] = None
    priority: Optional[int] = 1
    model_config = {"from_attributes": True}'''

if old_out in content:
    content = content.replace(old_out, new_out)
    print('OrderOut atualizado!')

with open(orders_path, 'w') as f:
    f.write(content)

print('\nPronto! Reinicie o servidor.')
