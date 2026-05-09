import sqlite3, uuid, pandas as pd

conn = sqlite3.connect(r'C:\fleet-cloud\fleet.db')
cur = conn.cursor()

df = pd.read_excel(r'C:\fleet-cloud\Gelocrim_Importacao_Dados.xlsx', sheet_name='Veiculos', header=1, dtype=str)
df.columns = [str(c).strip().replace(' *','').replace('*','') for c in df.columns]
df = df.dropna(subset=['PLACA'])

ins = upd = 0
for _, row in df.iterrows():
    placa = str(row.get('PLACA','')).strip().upper()
    if not placa or placa == 'NAN':
        continue

    modelo = str(row.get('MODELO','') or 'Caminhao').strip()

    # Forcar float valido sem nan
    try:
        v = str(row.get('CAPACIDADE_KG','')).replace(',','.').strip()
        cap_kg = float(v) if v and v != 'nan' else 1000.0
        if cap_kg == 0: cap_kg = 1000.0
    except:
        cap_kg = 1000.0

    try:
        v = str(row.get('CAPACIDADE_M3','')).replace(',','.').strip()
        cap_m3 = float(v) if v and v != 'nan' else 8.0
        if cap_m3 == 0: cap_m3 = 8.0
    except:
        cap_m3 = 8.0

    print(f"  {placa} | {modelo} | {cap_kg}kg | {cap_m3}m3")

    existe = cur.execute('SELECT id FROM vehicles WHERE plate=?', (placa,)).fetchone()
    if existe:
        cur.execute('''UPDATE vehicles SET model=?,capacity_kg=?,capacity_m3=?,
            updated_at=CURRENT_TIMESTAMP WHERE plate=?''',
            (modelo, cap_kg, cap_m3, placa))
        upd += 1
    else:
        cur.execute('''INSERT INTO vehicles
            (id,plate,model,type,capacity_kg,capacity_m3,status,created_at,updated_at)
            VALUES(?,?,?,'caminhao',?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)''',
            (str(uuid.uuid4()), placa, modelo, cap_kg, cap_m3, 'active'))
        ins += 1

conn.commit()
conn.close()
print(f'\nVeiculos: {ins} inseridos, {upd} atualizados')
