import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)

# Adiciona coluna codparc se não existir
cols = [c[1] for c in conn.execute("PRAGMA table_info(orders)").fetchall()]
if 'codparc' not in cols:
    conn.execute("ALTER TABLE orders ADD COLUMN codparc INTEGER")
    conn.commit()
    print('Coluna codparc adicionada!')
else:
    print('Coluna codparc já existe!')

# Verifica tabela clientes
cols_cli = [c[1] for c in conn.execute("PRAGMA table_info(clientes)").fetchall()]
print(f'\nColunas clientes: {cols_cli}')

conn.close()
print('\nPronto!')
