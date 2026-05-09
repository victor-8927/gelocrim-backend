import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Fix cidade: extrai antes da "/" ou pega "Manaus" do endereço
cur.execute("SELECT id, cidade, endereco, regiao FROM clientes")
rows = cur.fetchall()
atualizados = 0
for row in rows:
    id_, cidade, endereco, regiao = row
    nova_cidade = cidade or ''
    
    if not nova_cidade or nova_cidade.strip() == '':
        # Tenta extrair do endereço
        if endereco and 'Manaus' in endereco:
            nova_cidade = 'Manaus'
        elif endereco and ' - AM' in endereco:
            # Pega o que vem antes de " - AM"
            parts = endereco.split(' - AM')
            if parts:
                nova_cidade = 'Manaus'
        else:
            nova_cidade = 'Manaus'  # default AM
        
        cur.execute("UPDATE clientes SET cidade=? WHERE id=?", (nova_cidade, id_))
        atualizados += 1

print(f'Cidades atualizadas: {atualizados}')

# Verifica resultado
cur.execute("SELECT codparc, nome, cidade, tempo_entrega, rota FROM clientes LIMIT 5")
rows = cur.fetchall()
print('\nAmostra após correção:')
for r in rows:
    print(f'  {r[0]} | {r[1][:30]} | cidade={r[2]} | tempo={r[3]} | rota={r[4]}')

conn.commit()
conn.close()
print('\nPronto! Ctrl+Shift+R.')
