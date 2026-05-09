caminho = r"C:\fleet-cloud\app\routers\orders.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

idx = data.find('@router.get("/resumo-itens")')
idx_next = data.find('@router.', idx + 10)

novo = '''@router.get("/resumo-itens")
def resumo_itens(
    _=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resumo de quantidades de todos os pedidos do dia (qualquer status)"""
    rows = db.execute(text("""
        SELECT oi.item_nome, oi.item_tipo,
               SUM(oi.qtd) AS total_qtd,
               ROUND(SUM(oi.qtd * oi.peso_unit)) AS total_kg
        FROM order_items oi
        INNER JOIN orders o ON o.external_id = oi.nunota
        WHERE oi.item_tipo IN ('370','371','372','373')
          AND o.delivery_date = (
              SELECT MAX(delivery_date) FROM orders
              WHERE status IN ('pending','routed')
          )
        GROUP BY oi.item_tipo, oi.item_nome
        ORDER BY oi.item_tipo
    """)).fetchall()
    return [dict(r._mapping) for r in rows]

'''

data = data[:idx] + novo + data[idx_next:]
with open(caminho, "w", encoding="utf-8") as f:
    f.write(data)
print("OK - resumo por data maxima de entrega!")
