import sqlite3

c = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = c.cursor()

# Ver situacao atual
print('=== SITUACAO ATUAL ===')
cur.execute("SELECT COUNT(*) FROM orders")
print('Total orders:', cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM orders WHERE external_id LIKE 'SNK-%'")
print('Orders com prefixo SNK-:', cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM orders WHERE codparc IS NULL")
print('Orders sem CODPARC:', cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM order_items WHERE qtd < 0")
print('Itens com qtd negativa:', cur.fetchone()[0])

print()
print('Limpando dados antigos e incorretos...')

# Remover pedidos com prefixo SNK- (importacao antiga)
cur.execute("DELETE FROM orders WHERE external_id LIKE 'SNK-%'")
print('Removidos orders SNK-:', cur.rowcount)

# Remover pedidos sem codparc e sem nome (dados invalidos)
cur.execute("DELETE FROM orders WHERE codparc IS NULL AND (recipient_name IS NULL OR recipient_name='')")
print('Removidos orders invalidos:', cur.rowcount)

# Remover itens com quantidade negativa
cur.execute("DELETE FROM order_items WHERE qtd < 0")
print('Removidos itens negativos:', cur.rowcount)

# Remover itens sem codparc valido
cur.execute("DELETE FROM order_items WHERE codparc IS NULL OR codparc = 0")
print('Removidos itens sem codparc:', cur.rowcount)

c.commit()

print()
print('=== SITUACAO FINAL ===')
cur.execute("SELECT COUNT(*) FROM orders")
print('Total orders:', cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM orders WHERE status='pending'")
print('Orders pendentes:', cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM order_items")
print('Total itens:', cur.fetchone()[0])

cur.execute("SELECT COUNT(DISTINCT codparc) FROM orders WHERE status='pending' AND codparc IS NOT NULL")
print('Clientes unicos pendentes:', cur.fetchone()[0])

c.close()
print()
print('Pronto! Agora rode: python importar_planilha.py')
print('Para reimportar os pedidos corretamente.')
