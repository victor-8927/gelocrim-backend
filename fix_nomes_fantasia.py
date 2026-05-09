import sqlite3
import pandas as pd

conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = conn.cursor()

# Ler planilha
df = pd.read_excel(r'C:\fleet-cloud\Gelocrim_Importacao_Dados.xlsx',
                   sheet_name='Clientes TGFPAR', header=1, dtype=str)
df.columns = [c.strip().replace(' *','') for c in df.columns]
df = df.dropna(subset=['CODPARC'])

atualizados = 0
for _, row in df.iterrows():
    try:
        codparc = int(float(str(row['CODPARC']).strip()))
        nome_fantasia = str(row.get('NOMEFANTASIA','') or '').strip()
        nome_parceiro = str(row.get('NOMEPARC','') or '').strip()
        # Usar nome fantasia se disponivel e diferente
        nome = nome_fantasia if (nome_fantasia and nome_fantasia != 'nan' and len(nome_fantasia) > 2) else nome_parceiro
        if nome and nome != 'nan':
            cur.execute("UPDATE clientes SET nome=? WHERE codparc=?", (nome, codparc))
            if cur.rowcount > 0:
                atualizados += 1
    except: continue

conn.commit()

# Atualizar stops da rota com novos nomes
cur.execute("""
    UPDATE route_stops
    SET recipient_name = (
        SELECT c.nome FROM clientes c WHERE c.codparc = route_stops.codparc
    )
    WHERE codparc IS NOT NULL
""")
stops_atualizados = cur.rowcount
conn.commit()

print(f"Clientes atualizados: {atualizados}")
print(f"Stops atualizados: {stops_atualizados}")

# Verificar
cur.execute("""
    SELECT rs.sequence, rs.recipient_name, rs.codparc
    FROM routes r JOIN route_stops rs ON rs.route_id = r.id
    WHERE r.trip_number = 'VGM-260504-001'
    ORDER BY rs.sequence
""")
print("\nStops da rota:")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]} (cod:{r[2]})")

conn.close()
