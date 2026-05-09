path = r'C:\fleet-cloud\app\routers\orders.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona endpoint bulk_planilha
novo_endpoint = '''

class ItemPlanilha(BaseModel):
    cod: str
    nome: str
    qtd: int
    peso_unit: float

class PedidoPlanilha(BaseModel):
    external_id: str
    num_doc: Optional[str] = None
    codparc: Optional[int] = None
    recipient_name: str
    weight_kg: float
    itens: List[ItemPlanilha] = []
    data: Optional[str] = None

class BulkPlanilhaRequest(BaseModel):
    pedidos: List[PedidoPlanilha]

@router.post("/bulk_planilha")
def bulk_planilha(body: BulkPlanilhaRequest, db: Session = Depends(get_db)):
    importados = 0
    atualizados = 0
    
    for p in body.pedidos:
        # Busca cliente no banco pelo codparc
        cli = db.execute(text(
            "SELECT lat, lng, address, regiao FROM clientes WHERE codparc = :c"
        ), {"c": p.codparc}).mappings().fetchone()
        
        lat = float(cli["lat"]) if cli and cli["lat"] else None
        lng = float(cli["lng"]) if cli and cli["lng"] else None
        address = cli["address"] if cli and cli.get("address") else ""
        regiao = cli["regiao"] if cli and cli.get("regiao") else ""
        
        # Verifica se pedido já existe
        existente = db.execute(text(
            "SELECT id, status FROM orders WHERE external_id = :eid"
        ), {"eid": p.external_id}).fetchone()
        
        if existente:
            if existente[1] == 'pending':
                db.execute(text("""
                    UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
                    codparc=:codparc, lat=:lat, lng=:lng, address=:addr,
                    regiao=:regiao, updated_at=CURRENT_TIMESTAMP
                    WHERE external_id=:eid
                """), {
                    "kg": p.weight_kg, "nome": p.recipient_name,
                    "codparc": p.codparc, "lat": lat, "lng": lng,
                    "addr": address, "regiao": regiao, "eid": p.external_id
                })
                atualizados += 1
        else:
            import uuid
            order_id = str(uuid.uuid4())
            db.execute(text("""
                INSERT INTO orders (id, external_id, codparc, recipient_name,
                    weight_kg, lat, lng, address, regiao, status, created_at)
                VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,
                    :addr, :regiao, 'pending', CURRENT_TIMESTAMP)
            """), {
                "id": order_id, "eid": p.external_id, "codparc": p.codparc,
                "nome": p.recipient_name, "kg": p.weight_kg,
                "lat": lat, "lng": lng, "addr": address, "regiao": regiao
            })
            importados += 1
            
            # Salva os itens
            for item in p.itens:
                db.execute(text("""
                    INSERT INTO order_items (id, codparc, top_app, item_tipo,
                        item_nome, peso_unit, qtd, dt_neg, created_at)
                    VALUES (:id, :codparc, :top_app, :tipo, :nome,
                        :peso, :qtd, :dt, CURRENT_TIMESTAMP)
                """), {
                    "id": str(uuid.uuid4()),
                    "codparc": p.codparc,
                    "top_app": p.external_id,
                    "tipo": item.cod,
                    "nome": item.nome,
                    "peso": item.peso_unit,
                    "qtd": item.qtd,
                    "dt": p.data or ""
                })
    
    db.commit()
    return {"importados": importados, "atualizados": atualizados}
'''

# Adiciona no final do arquivo
if 'bulk_planilha' not in content:
    # Garante imports necessários
    if 'List' not in content:
        content = content.replace('from typing import Optional', 'from typing import Optional, List')
    content += novo_endpoint
    print('Endpoint bulk_planilha adicionado!')
else:
    print('Endpoint já existe!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(path, doraise=True)
    print('orders.py VÁLIDO!')
except Exception as e:
    print(f'ERRO: {e}')
