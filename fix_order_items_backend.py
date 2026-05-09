# 1. Cria tabela order_items no banco
import sqlite3
db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codparc INTEGER NOT NULL,
    top_app TEXT,
    item_tipo TEXT NOT NULL,  -- 'gelo5', 'gelo10', 'gelo20', 'gelo40'
    item_nome TEXT NOT NULL,  -- 'Gelo 5kg', etc
    peso_unit REAL NOT NULL,  -- peso real: 6, 11, 23, 45
    qtd INTEGER NOT NULL DEFAULT 0,
    peso_total REAL GENERATED ALWAYS AS (qtd * peso_unit) STORED,
    dt_neg TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

cur.execute("SELECT COUNT(*) FROM order_items")
print(f'Tabela order_items criada! Registros: {cur.fetchone()[0]}')
conn.close()
