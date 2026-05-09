path = r'C:\fleet-cloud\app\routers\orders.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Corrige a query do list_orders para incluir lat e lng
old_query = '''    q = """SELECT o.id, o.external_id, r.name AS recipient_name, r.address,
               o.weight_kg, o.volume_m3, o.tw_start, o.tw_end, o.status, o.created_at
        FROM orders o JOIN recipients r ON r.id = o.recipient_id"""'''

new_query = '''    q = """SELECT o.id, o.external_id, r.name AS recipient_name, r.address,
               o.lat, o.lng, o.weight_kg, o.volume_m3, o.tw_start, o.tw_end, o.status, o.created_at
        FROM orders o JOIN recipients r ON r.id = o.recipient_id"""'''

content = content.replace(old_query, new_query)

# Corrige o modelo OrderOut para incluir lat e lng
old_model = '''class OrderOut(BaseModel):
    id: str
    external_id: Optional[str]
    recipient_name: str
    address: str
    weight_kg: float
    volume_m3: float
    tw_start: Optional[str]
    tw_end: Optional[str]
    status: str
    created_at: str
    model_config = {"from_attributes": True}'''

new_model = '''class OrderOut(BaseModel):
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

content = content.replace(old_model, new_model)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('orders.py corrigido com lat/lng!')
