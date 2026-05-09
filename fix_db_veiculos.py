import sqlite3

db = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db)
cur = conn.cursor()

# Ver colunas atuais
cur.execute("PRAGMA table_info(vehicles)")
cols = [r[1] for r in cur.fetchall()]
print('Colunas atuais:', cols)

# Colunas a adicionar
novas = [
    ('vda',            'TEXT'),
    ('fuel_type',      'TEXT DEFAULT "diesel"'),
    ('km_per_liter',   'REAL DEFAULT 4'),
    ('fuel_price',     'REAL DEFAULT 6.50'),
    ('ipva_anual',     'REAL DEFAULT 0'),
    ('manut_mes',      'REAL DEFAULT 0'),
    ('daily_cost',     'REAL DEFAULT 0'),
    ('pallets',        'INTEGER DEFAULT 0'),
    ('bau_comp',       'REAL DEFAULT 0'),
    ('bau_larg',       'REAL DEFAULT 0'),
    ('bau_alt',        'REAL DEFAULT 0'),
    ('oleo_ult_data',  'TEXT'),
    ('oleo_prox_data', 'TEXT'),
    ('oleo_custo',     'REAL DEFAULT 0'),
]

for col, tipo in novas:
    if col not in cols:
        try:
            cur.execute(f'ALTER TABLE vehicles ADD COLUMN {col} {tipo}')
            print(f'Coluna adicionada: {col}')
        except Exception as e:
            print(f'Erro em {col}: {e}')
    else:
        print(f'Já existe: {col}')

conn.commit()
conn.close()
print('\nBanco atualizado!')
