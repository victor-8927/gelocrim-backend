caminho = r"C:\fleet-cloud\app\routers\orders.py"
with open(caminho, encoding="utf-8") as f:
    data = f.read()

# Encontrar e substituir o endpoint inteiro
idx_start = data.find('@router.get("/resumo-itens")')
if idx_start < 0:
    print("Endpoint nao encontrado")
else:
    # Encontrar o proximo @router depois desse
    idx_next = data.find('@router.', idx_start + 10)
    trecho_atual = data[idx_start:idx_next]
    print("=== TRECHO ATUAL ===")
    print(trecho_atual)
    print("=== FIM ===")
    
    novo = '''@router.get("/resumo-itens")
def resumo_itens(
    data: Optional[str] = Query(None),
    _=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from datetime import date as _date
    dt = data or _date.today().isoformat()
    rows = db.execute(text("""
        SELECT oi.item_nome, oi.item_tipo,
               SUM(oi.qtd) AS total_qtd,
               ROUND(SUM(oi.qtd * oi.peso_unit)) AS total_kg
        FROM order_items oi
        INNER JOIN orders o ON o.external_id = oi.nunota
        WHERE oi.item_tipo IN ('370','371','372','373')
          AND o.delivery_date = :dt
        GROUP BY oi.item_tipo, oi.item_nome
        ORDER BY oi.item_tipo
    """), {"dt": dt}).fetchall()
    return [dict(r._mapping) for r in rows]

'''
    data = data[:idx_start] + novo + data[idx_next:]
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(data)
    print("OK - endpoint substituido!")
