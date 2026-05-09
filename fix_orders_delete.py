path = r'C:\fleet-cloud\app\routers\orders.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'DELETE' in content or 'delete' in content.lower():
    print('DELETE encontrado!')
    import re
    for m in re.finditer(r'@router\.(delete|DELETE)[^\n]*\n[^\n]*', content, re.IGNORECASE):
        print(m.group())
else:
    print('DELETE NAO existe! Adicionando...')
    # Adiciona ao final do arquivo
    delete_route = '''

@router.delete("/{order_id}")
def delete_order(order_id: int, db: sqlite3.Connection = Depends(get_db)):
    db.execute("DELETE FROM orders WHERE id=?", (order_id,))
    db.commit()
    return {"deleted": order_id}

@router.delete("")
def delete_orders_pending(db: sqlite3.Connection = Depends(get_db)):
    result = db.execute("DELETE FROM orders WHERE status='pending'")
    db.commit()
    return {"deleted": result.rowcount}
'''
    content += delete_route
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Rotas DELETE adicionadas!')
