PATH = r'C:\fleet-cloud\app\routers\orders.py'

with open(PATH, encoding='utf-8') as f:
    content = f.read()

OLD = """class PedidoPlanilha(BaseModel):
    external_id: str
    num_doc: Optional[str] = None
    codparc: Optional[int] = None
    recipient_name: str
    weight_kg: float
    itens: List[ItemPlanilha] = []
    data: Optional[str] = None
    top_app: Optional[str] = None"""

NEW = """class PedidoPlanilha(BaseModel):
    external_id: str
    num_doc: Optional[str] = None
    codparc: Optional[int] = None
    recipient_name: str
    weight_kg: float
    itens: List[ItemPlanilha] = []
    data: Optional[str] = None
    top_app: Optional[str] = None
    total_value: Optional[float] = None
    order_type: Optional[str] = None
    regiao: Optional[str] = None"""

if OLD in content:
    content = content.replace(OLD, NEW)
    print("OK! Modelo PedidoPlanilha corrigido com total_value e order_type!")
else:
    print("AVISO: modelo nao encontrado")

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reinicie o backend!")
