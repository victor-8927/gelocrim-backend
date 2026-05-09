import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)

# Recria a tabela sem NOT NULL em lat/lng e recipient_id
conn.executescript('''
PRAGMA foreign_keys=OFF;

-- Cria tabela nova sem NOT NULL problemáticos
CREATE TABLE IF NOT EXISTS orders_new (
  id           TEXT PRIMARY KEY,
  external_id  TEXT UNIQUE,
  source       TEXT DEFAULT 'manual',
  recipient_id TEXT,
  lat          REAL,
  lng          REAL,
  weight_kg    REAL DEFAULT 0,
  volume_m3    REAL DEFAULT 0,
  tw_start     TEXT,
  tw_end       TEXT,
  nfe_status   TEXT DEFAULT 'pending',
  status       TEXT DEFAULT 'pending',
  notes        TEXT,
  created_at   TEXT DEFAULT (datetime('now')),
  updated_at   TEXT DEFAULT (datetime('now')),
  priority     INTEGER DEFAULT 1,
  delivery_date TEXT,
  recipient_name TEXT,
  address      TEXT,
  order_type   TEXT,
  total_value  REAL,
  regiao       TEXT,
  time_window_start TEXT,
  time_window_end   TEXT
);

-- Copia dados existentes
INSERT OR IGNORE INTO orders_new SELECT * FROM orders;

-- Substitui a tabela
DROP TABLE orders;
ALTER TABLE orders_new RENAME TO orders;

PRAGMA foreign_keys=ON;
''')

conn.commit()
conn.close()

print('Tabela orders recriada sem NOT NULL em lat/lng!')
print('Reinicie o servidor e reimporte o XLS.')
