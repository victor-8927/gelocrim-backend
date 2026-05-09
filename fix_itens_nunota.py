"""
Corrige order_items para vincular por NUNOTA em vez de CODPARC+TOP
"""
import sqlite3, uuid

conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = conn.cursor()

# Verificar se coluna nunota existe em order_items
cols = [r[1] for r in cur.execute("PRAGMA table_info(order_items)").fetchall()]
print("Colunas atuais:", cols)

if 'nunota' not in cols:
    print("Adicionando coluna nunota...")
    cur.execute("ALTER TABLE order_items ADD COLUMN nunota TEXT")
    conn.commit()
    print("OK - coluna nunota adicionada!")
else:
    print("Coluna nunota ja existe.")

conn.close()
print("Pronto! Agora rode: python importar_ti.py novamente")
