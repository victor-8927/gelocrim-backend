"""
GELOCRIM - Importador Completo da Planilha Sankhya
===================================================
Lê as 3 abas da planilha Gelocrim_Importacao_Dados.xlsx:
  - Clientes TGFPAR  -> tabela clientes
  - Pedidos TGFCAB   -> tabela orders (agrupado por CODPARC = 1 parada)
  - Veiculos         -> tabela vehicles

Uso:
  python importar_planilha.py
  python importar_planilha.py C:\\caminho\\para\\planilha.xlsx
"""

import sys, os, uuid, sqlite3
import pandas as pd
from datetime import datetime

DB_PATH     = r"C:\fleet-cloud\fleet.db"
XLSX_PADRAO = r"C:\fleet-cloud\Gelocrim_Importacao_Dados.xlsx"

def limpar_lat_lng(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    try:
        return float(str(val).replace(",", ".").strip())
    except:
        return None

def importar_clientes(xlsx, conn):
    print("\n Importando clientes (TGFPAR)...")
    try:
        df = pd.read_excel(xlsx, sheet_name="Clientes TGFPAR", header=1, dtype=str)
    except Exception as e:
        print(f"   ERRO: {e}")
        return

    df.columns = [str(c).strip().replace(" *", "").replace("*", "") for c in df.columns]
    df = df.dropna(subset=["CODPARC"])
    cur = conn.cursor()
    inseridos = atualizados = 0

    for _, row in df.iterrows():
        try:
            codparc = int(float(str(row.get("CODPARC", "")).strip()))
        except:
            continue

        nome     = str(row.get("NOMEPARC",    "") or "").strip()
        fantasia = str(row.get("NOMEFANTASIA","") or "").strip()
        cpf_cnpj = str(row.get("CGC_CPF",     "") or "").strip()
        telefone = str(row.get("TELEFONE",    "") or "").strip()
        endereco = str(row.get("ENDERECO",    "") or "").strip()
        bairro   = str(row.get("BAIRRO",      "") or "").strip()
        cep      = str(row.get("CEP",         "") or "").strip()
        cidade_r = str(row.get("CIDADE", "Manaus - AM") or "Manaus - AM").strip()
        cidade   = cidade_r.split(" - ")[0].strip()
        lat      = limpar_lat_lng(row.get("LATITUDE"))
        lng      = limpar_lat_lng(row.get("LONGITUDE"))

        existe = cur.execute("SELECT id FROM clientes WHERE codparc=?", (codparc,)).fetchone()
        dados = dict(codparc=codparc, nome=nome or fantasia, razao_social=nome,
                     endereco=endereco, bairro=bairro, cidade=cidade, cep=cep,
                     lat=lat, lng=lng, cpf_cnpj=cpf_cnpj, telefone=telefone, ativo="S")

        if existe:
            cur.execute("""UPDATE clientes SET nome=:nome,razao_social=:razao_social,
                endereco=:endereco,bairro=:bairro,cidade=:cidade,cep=:cep,
                lat=:lat,lng=:lng,cpf_cnpj=:cpf_cnpj,telefone=:telefone
                WHERE codparc=:codparc""", dados)
            atualizados += 1
        else:
            cur.execute("""INSERT INTO clientes
                (codparc,nome,razao_social,endereco,bairro,cidade,cep,lat,lng,cpf_cnpj,telefone,ativo)
                VALUES(:codparc,:nome,:razao_social,:endereco,:bairro,:cidade,:cep,
                       :lat,:lng,:cpf_cnpj,:telefone,:ativo)""", dados)
            inseridos += 1

    conn.commit()
    total   = cur.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    com_gps = cur.execute("SELECT COUNT(*) FROM clientes WHERE lat IS NOT NULL AND lng IS NOT NULL").fetchone()[0]
    print(f"   OK: {inseridos} inseridos, {atualizados} atualizados")
    print(f"   GPS: {com_gps}/{total} clientes com coordenadas | {total-com_gps} sem GPS")

def importar_pedidos(xlsx, conn):
    print("\n Importando pedidos (TGFCAB)...")
    try:
        df = pd.read_excel(xlsx, sheet_name="Pedidos TGFCAB", header=1, dtype=str)
    except Exception as e:
        print(f"   ERRO: {e}")
        return

    df.columns = [str(c).strip().replace(" *", "").replace("*", "") for c in df.columns]
    df = df.dropna(subset=["NUNOTA"])
    cur = conn.cursor()

    # Carregar GPS dos clientes
    clientes_db = {}
    for r in cur.execute("SELECT codparc,lat,lng,bairro,cidade,regiao FROM clientes").fetchall():
        clientes_db[int(r[0])] = dict(lat=r[1],lng=r[2],bairro=r[3] or "",cidade=r[4] or "Manaus",regiao=r[5] or "")

    importados = atualizados = ignorados = 0

    for _, row in df.iterrows():
        try:
            nunota  = str(int(float(str(row.get("NUNOTA","")).strip())))
            codparc = int(float(str(row.get("CODPARC","")).strip()))
        except:
            continue

        nome = str(row.get("NOMEPARC","") or "").strip()

        try:
            peso = float(str(row.get("PESOLIQ","0") or "0").replace(",","."))
            if peso == 0:
                peso = float(str(row.get("PESOBRUT","0") or "0").replace(",","."))
        except:
            peso = 0

        try:
            vlr = float(str(row.get("VLRNOTA","0") or "0").replace(",","."))
        except:
            vlr = 0

        try:
            top = str(int(float(str(row.get("TOP","1000") or "1000").strip())))
        except:
            top = "1000"

        try:
            data_ent = pd.to_datetime(str(row.get("DATA_ENTREGA",""))).strftime("%Y-%m-%d")
        except:
            data_ent = datetime.now().strftime("%Y-%m-%d")

        cli     = clientes_db.get(codparc, {})
        lat     = cli.get("lat")
        lng     = cli.get("lng")
        bairro  = cli.get("bairro","")
        cidade  = cli.get("cidade","Manaus")
        regiao  = cli.get("regiao","")
        address = f"{bairro}, {cidade}".strip(", ") if bairro else cidade

        existente = cur.execute("SELECT id,status FROM orders WHERE external_id=?", (nunota,)).fetchone()

        if existente:
            if existente[1] == "pending":
                cur.execute("""UPDATE orders SET weight_kg=?,recipient_name=?,codparc=?,
                    lat=?,lng=?,address=?,regiao=?,total_value=?,delivery_date=?,
                    updated_at=CURRENT_TIMESTAMP WHERE external_id=?""",
                    (peso,nome,codparc,lat,lng,address,regiao,vlr,data_ent,nunota))
                atualizados += 1
            else:
                ignorados += 1
            continue

        oid = str(uuid.uuid4())
        cur.execute("""INSERT INTO orders
            (id,external_id,codparc,recipient_name,weight_kg,lat,lng,
             address,regiao,total_value,delivery_date,status,created_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,'pending',CURRENT_TIMESTAMP)""",
            (oid,nunota,codparc,nome,peso,lat,lng,address,regiao,vlr,data_ent))

        cur.execute("""INSERT INTO order_items
            (codparc,top_app,item_tipo,item_nome,peso_unit,qtd,dt_neg,created_at)
            VALUES(?,?,?,?,?,?,?,CURRENT_TIMESTAMP)""",
            (int(codparc),str(top),str(top),
             f"Nota {nunota}",float(peso),1,str(data_ent)))

        importados += 1

    conn.commit()

    # Resumo por cliente
    resumo = cur.execute("""
        SELECT codparc, recipient_name, COUNT(*) as notas,
               SUM(weight_kg) as peso, SUM(total_value) as valor, lat, lng
        FROM orders WHERE status='pending'
        GROUP BY codparc ORDER BY peso DESC
    """).fetchall()

    print(f"\n   {'CLIENTE':<38} {'NOTAS':>5} {'PESO kg':>8} {'VALOR R$':>10} {'GPS':>5}")
    print(f"   {'-'*70}")
    for r in resumo:
        gps  = "OK" if r[5] and r[6] else "X"
        nome_c = (r[1] or "SEM NOME")[:37]
        print(f"   {nome_c:<38} {r[2]:>5} {r[3]:>8.0f} {(r[4] or 0):>10.2f} {gps:>5}")

    sem_gps = sum(1 for r in resumo if not r[5] or not r[6])
    print(f"\n   OK: {importados} importados | {atualizados} atualizados | {ignorados} ignorados")
    print(f"   PARADAS: {len(resumo)} clientes unicos | {sem_gps} sem GPS")

def importar_veiculos(xlsx, conn):
    print("\n Importando veiculos...")
    try:
        df = pd.read_excel(xlsx, sheet_name="Veiculos", header=1, dtype=str)
    except Exception as e:
        print(f"   ERRO: {e}")
        return

    df.columns = [str(c).strip().replace(" *", "").replace("*", "") for c in df.columns]
    df = df.dropna(subset=["PLACA"])
    cur = conn.cursor()
    inseridos = atualizados = 0

    for _, row in df.iterrows():
        placa = str(row.get("PLACA","") or "").strip().upper()
        if not placa or placa == "NAN":
            continue

        modelo = str(row.get("MODELO","") or "").strip()
        tipo   = str(row.get("TIPO","caminhao") or "caminhao").strip().lower()
        status_r = str(row.get("STATUS","active") or "active").strip().lower()
        status = "active" if status_r in ("ativo","active") else "inactive"

        try:
            cap_kg = float(str(row.get("CAPACIDADE_KG","1000") or "1000").replace(",","."))
            if cap_kg == 0: cap_kg = 1000.0
        except:
            cap_kg = 1000.0
        try:
            cap_m3 = float(str(row.get("CAPACIDADE_M3","8") or "8").replace(",","."))
            if cap_m3 == 0: cap_m3 = 8.0
        except:
            cap_m3 = 8.0

        existe = cur.execute("SELECT id FROM vehicles WHERE plate=?", (placa,)).fetchone()
        if existe:
            cur.execute("""UPDATE vehicles SET model=?,type=?,capacity_kg=?,
                capacity_m3=?,status=?,updated_at=CURRENT_TIMESTAMP WHERE plate=?""",
                (modelo,tipo,cap_kg,cap_m3,status,placa))
            atualizados += 1
        else:
            cur.execute("""INSERT INTO vehicles
                (id,plate,model,type,capacity_kg,capacity_m3,status,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)""",
                (str(uuid.uuid4()),placa,modelo,tipo,cap_kg,cap_m3,status))
            inseridos += 1

    conn.commit()
    print(f"   OK: {inseridos} inseridos, {atualizados} atualizados")

def main():
    xlsx = sys.argv[1] if len(sys.argv) > 1 else XLSX_PADRAO

    if not os.path.exists(xlsx):
        print(f"ERRO: Arquivo nao encontrado: {xlsx}")
        return

    print(f"Planilha: {xlsx}")
    conn = sqlite3.connect(DB_PATH)

    importar_clientes(xlsx, conn)
    importar_pedidos(xlsx, conn)
    importar_veiculos(xlsx, conn)

    conn.close()
    print("\nImportacao concluida!")
    print("Proximo passo: va em Roteirizacao e selecione os clientes no mapa.")

if __name__ == "__main__":
    main()
