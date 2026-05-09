import sqlite3
conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')

# Verifica coluna route_id na tabela routes (pode ser diferente)
cols = [r[1] for r in conn.execute("PRAGMA table_info(routes)").fetchall()]
print(f'Colunas routes: {cols}')

# A chave primaria da routes pode ser 'id' nao 'route_id'
# Vamos usar 'id' como referencia

conn.execute("""
CREATE TABLE IF NOT EXISTS route_stops (
    stop_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    order_id TEXT,
    sequence INTEGER DEFAULT 0,
    recipient_name TEXT,
    address TEXT,
    lat REAL,
    lng REAL,
    weight_kg REAL DEFAULT 0,
    status TEXT DEFAULT 'pending',
    eta TEXT,
    ata TEXT,
    atd TEXT,
    failure_reason TEXT,
    lat_confirmacao REAL,
    lng_confirmacao REAL,
    codparc INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
print('Tabela route_stops criada!')

# Verifica se routes tem coluna 'route_id' ou so 'id'
if 'route_id' not in cols:
    # Adiciona alias route_id como coluna extra se nao existir
    print('ATENCAO: routes usa "id" como PK, nao "route_id"')
    print('O router precisa usar r.id como route_id')

conn.close()
print('Pronto!')
