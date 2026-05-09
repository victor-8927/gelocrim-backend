import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Remove registro lixo
cur.execute("DELETE FROM vehicles WHERE plate LIKE 'TOTAL%' OR length(plate) > 20")
print(f'Lixo removido: {cur.rowcount}')

# 2. Para placas duplicadas (com/sem espaço, com/sem hífen)
# Mantém o que tem VDA (editado) e remove o antigo sem VDA
duplicatas = [
    ('JWU 7775', '        JWU 7775'),  # remove com espaço
    ('OAJ 2612', 'OAJ-2612'),          # mantém sem hífen, remove com hífen? 
    ('PHJ 3549', 'PHJ-3549'),
    ('NOM 5373', 'NOM 5413'),          # placas diferentes - não duplicata
]

# Remove registros sem VDA quando há um com VDA da mesma placa (normalizada)
cur.execute("SELECT id, vda, plate FROM vehicles ORDER BY plate")
rows = cur.fetchall()

# Normaliza placas para comparação
def normalizar(p):
    return p.strip().replace('-','').replace(' ','').upper()

from collections import defaultdict
grupos = defaultdict(list)
for id_, vda, plate in rows:
    grupos[normalizar(plate)].append((id_, vda, plate))

remover = []
for placa_norm, veics in grupos.items():
    if len(veics) > 1:
        print(f'\nDuplicata: {placa_norm}')
        for v in veics:
            print(f'  id={v[0][:8]} vda={v[1]} plate="{v[2]}"')
        # Mantém o que tem VDA, remove os sem VDA
        com_vda = [v for v in veics if v[1]]
        sem_vda = [v for v in veics if not v[1]]
        if com_vda:
            for v in sem_vda:
                remover.append(v[0])
                print(f'  → Remover {v[0][:8]} (sem VDA)')
        else:
            # Mantém o mais recente
            for v in veics[:-1]:
                remover.append(v[0])
                print(f'  → Remover {v[0][:8]} (mais antigo)')

for id_ in remover:
    cur.execute("DELETE FROM vehicles WHERE id=?", (id_,))
print(f'\nTotal removidos: {len(remover)}')

# Remove espaços das placas
cur.execute("UPDATE vehicles SET plate = TRIM(plate)")
print('Placas sem espaços extras!')

conn.commit()

# Resultado final
cur.execute("SELECT vda, plate, model, status FROM vehicles ORDER BY vda, plate")
rows = cur.fetchall()
print(f'\nVeículos finais: {len(rows)}')
for r in rows:
    print(f'  vda={r[0]} | plate={r[1]} | model={r[2][:25]} | {r[3]}')

conn.close()
