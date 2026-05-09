import sqlite3
import pandas as pd

def fix_importador():
    conn = sqlite3.connect('database.db') # Ajuste para o seu banco se necessário
    print("Conectado ao banco para ajuste de CODPARC...")
    # Lógica para garantir que o CODPARC seja a chave de cruzamento
    conn.execute("UPDATE clientes SET codparc = TRIM(codparc)")
    conn.commit()
    print("Cruzamento de Base de Clientes preparado com sucesso!")
    conn.close()

if __name__ == "__main__":
    fix_importador()