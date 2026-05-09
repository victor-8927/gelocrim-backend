import sqlite3

def fix_post():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print("Cruzando pedidos TGFCAB com coordenadas...")
    # Garante que pedidos sem lat/lng busquem do cadastro de parceiros
    query = """
    UPDATE pedidos 
    SET latitude = (SELECT lat FROM clientes WHERE clientes.codparc = pedidos.codparc),
        longitude = (SELECT lng FROM clientes WHERE clientes.codparc = pedidos.codparc)
    WHERE latitude IS NULL OR latitude = 0
    """
    cursor.execute(query)
    conn.commit()
    print(f"Processamento concluído: {cursor.rowcount} pedidos atualizados no mapa.")
    conn.close()

if __name__ == "__main__":
    fix_post()