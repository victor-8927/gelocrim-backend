path = r'C:\fleet-cloud\app\routers\drivers.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona tipo no DriverOut
old_out = '''class DriverOut(BaseModel):
    id: str
    name: str
    cpf: Optional[str]
    cnh: Optional[str]
    cnh_category: Optional[str]
    phone: Optional[str]
    vehicle_id: Optional[str]
    status: str
    created_at: str
    model_config = {"from_attributes": True}'''

new_out = '''class DriverOut(BaseModel):
    id: str
    name: str
    cpf: Optional[str]
    cnh: Optional[str]
    cnh_category: Optional[str]
    phone: Optional[str]
    vehicle_id: Optional[str]
    status: str
    tipo: Optional[str] = "motorista"
    created_at: str
    model_config = {"from_attributes": True}'''

content = content.replace(old_out, new_out)

# Adiciona tipo na query SELECT
old_query = '"SELECT id,name,cpf,cnh,cnh_category,phone,vehicle_id,status,created_at FROM drivers WHERE status!=\'deleted\' ORDER BY name"'
new_query = '"SELECT id,name,cpf,cnh,cnh_category,phone,vehicle_id,status,tipo,created_at FROM drivers WHERE status!=\'deleted\' ORDER BY name"'
content = content.replace(old_query, new_query)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('drivers.py corrigido!')
print('Reinicie a API!')
