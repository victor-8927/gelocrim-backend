with open(r'C:\fleet-cloud\app\routers\orders.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = """class PedidoPlanilha(BaseModel):
    external_id: str
    num_doc: Optional[str] = None
    codparc: Optional[int] = None
    recipient_name: str
    weight_kg: float
    itens: List[ItemPlanilha] = []
    data: Optional[str] = None"""

new = """class PedidoPlanilha(BaseModel):
    external_id: str
    num_doc: Optional[str] = None
    codparc: Optional[int] = None
    recipient_name: str
    weight_kg: float
    itens: List[ItemPlanilha] = []
    data: Optional[str] = None
    top_app: Optional[str] = None"""

if old in content:
    content = content.replace(old, new)
    print('top_app adicionado!')
else:
    print('Padrão não encontrado!')

with open(r'C:\fleet-cloud\app\routers\orders.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\orders.py', doraise=True)
    print('VÁLIDO! Reinicie o servidor.')
except Exception as e:
    print(f'ERRO: {e}')
