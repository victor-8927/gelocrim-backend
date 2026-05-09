# Adiciona endpoint DELETE no router de rotas
path = r'C:\fleet-cloud\app\routers\routes.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adiciona antes do último @router.patch
new_endpoint = '''
@router.delete("/{route_id}")
def delete_route(route_id: str, db: Session = Depends(get_db)):
    # Verifica se pode excluir
    route = db.execute(text(
        "SELECT status FROM routes WHERE id = :id"
    ), {"id": route_id}).fetchone()
    if not route:
        raise HTTPException(404, "Rota não encontrada")
    if route[0] in ("executing", "done"):
        raise HTTPException(400, "Não é possível excluir rota em execução ou concluída")

    # Devolve pedidos para pending
    stops = db.execute(text(
        "SELECT order_id FROM route_stops WHERE route_id = :id"
    ), {"id": route_id}).fetchall()
    for stop in stops:
        if stop[0]:
            db.execute(text(
                "UPDATE orders SET status = 'pending' WHERE id = :id"
            ), {"id": stop[0]})

    # Remove stops e rota
    db.execute(text("DELETE FROM route_stops WHERE route_id = :id"), {"id": route_id})
    db.execute(text("DELETE FROM routes WHERE id = :id"), {"id": route_id})
    db.commit()
    return {"deleted": True}

'''

# Insere antes do @router.patch
old = '@router.patch("/{route_id}/stops/{stop_id}")'
if old in content:
    content = content.replace(old, new_endpoint + old)
    print('Endpoint DELETE adicionado!')
else:
    print('Padrão não encontrado!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Também volta os pedidos das rotas antigas para pending
import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
# Pedidos com status routed que não têm stop ativo
routed = conn.execute("""
    SELECT id FROM orders WHERE status = 'routed'
    AND id NOT IN (
        SELECT order_id FROM route_stops 
        WHERE route_id IN (SELECT id FROM routes WHERE status IN ('released','executing','done'))
    )
""").fetchall()
for r in routed:
    conn.execute("UPDATE orders SET status = 'pending' WHERE id = ?", (r[0],))
print(f'{len(routed)} pedidos devolvidos para pending!')
conn.commit()
conn.close()
print('Pronto! Reinicie o servidor.')
