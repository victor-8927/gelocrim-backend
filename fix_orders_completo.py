with open(r'C:\fleet-cloud\app\routers\orders.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza e remove tudo a partir de class ItemPlanilha
idx = content.find('\nclass ItemPlanilha')
if idx == -1:
    idx = content.find('class ItemPlanilha')

print(f'Encontrado em: {idx}')
content = content[:idx]

# Adiciona os modelos e endpoint corrigidos
content += '''

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
    top_app: Optional[str] = None

class BulkPlanilhaRequest(BaseModel):
    pedidos: List[PedidoPlanilha]

@router.post("/bulk_planilha")
def bulk_planilha(body: BulkPlanilhaRequest, db: Session = Depends(get_db)):
    import uuid as _uuid
    importados = 0
    atualizados = 0

    for p in body.pedidos:
        try:
            cli = db.execute(text(
                "SELECT lat, lng, bairro, cidade, regiao FROM clientes WHERE codparc = :c"
            ), {"c": p.codparc}).mappings().fetchone()

            lat = float(cli["lat"]) if cli and cli["lat"] else None
            lng = float(cli["lng"]) if cli and cli["lng"] else None
            bairro = (cli["bairro"] or "") if cli else ""
            cidade = (cli["cidade"] or "Manaus") if cli else "Manaus"
            regiao = (cli["regiao"] or "") if cli else ""
            address = f"{bairro}, {cidade}".strip(", ") if bairro else cidade

            existente = db.execute(text(
                "SELECT id, status FROM orders WHERE external_id = :eid"
            ), {"eid": str(p.external_id)}).fetchone()

            if existente:
                if existente[1] == 'pending':
                    db.execute(text("""
                        UPDATE orders SET weight_kg=:kg, recipient_name=:nome,
                        codparc=:codparc, lat=:lat, lng=:lng, address=:addr,
                        regiao=:regiao, updated_at=CURRENT_TIMESTAMP
                        WHERE external_id=:eid
                    """), {
                        "kg": float(p.weight_kg),
                        "nome": str(p.recipient_name),
                        "codparc": p.codparc,
                        "lat": lat, "lng": lng,
                        "addr": str(address),
                        "regiao": str(regiao),
                        "eid": str(p.external_id)
                    })
                    atualizados += 1
            else:
                order_id = str(_uuid.uuid4())
                db.execute(text("""
                    INSERT INTO orders (id, external_id, codparc, recipient_name,
                        weight_kg, lat, lng, address, regiao, status, created_at)
                    VALUES (:id, :eid, :codparc, :nome, :kg, :lat, :lng,
                        :addr, :regiao, 'pending', CURRENT_TIMESTAMP)
                """), {
                    "id": order_id,
                    "eid": str(p.external_id),
                    "codparc": p.codparc,
                    "nome": str(p.recipient_name),
                    "kg": float(p.weight_kg),
                    "lat": lat, "lng": lng,
                    "addr": str(address),
                    "regiao": str(regiao)
                })
                importados += 1

                for item in p.itens:
                    db.execute(text("""
                        INSERT INTO order_items (id, codparc, top_app, item_tipo,
                            item_nome, peso_unit, qtd, dt_neg, created_at)
                        VALUES (:id, :codparc, :top_app, :tipo, :nome,
                            :peso, :qtd, :dt, CURRENT_TIMESTAMP)
                    """), {
                        "id": str(_uuid.uuid4()),
                        "codparc": p.codparc,
                        "top_app": str(p.top_app or p.external_id),
                        "tipo": str(item.cod),
                        "nome": str(item.nome),
                        "peso": float(item.peso_unit),
                        "qtd": int(item.qtd),
                        "dt": str(p.data or "")[:10]
                    })
        except Exception as e:
            print(f"Erro no pedido {p.external_id}: {e}")
            continue

    db.commit()
    return {"importados": importados, "atualizados": atualizados}
'''

with open(r'C:\fleet-cloud\app\routers\orders.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(r'C:\fleet-cloud\app\routers\orders.py', doraise=True)
    print('VÁLIDO! Reinicie o servidor.')
except Exception as e:
    print(f'ERRO: {e}')
