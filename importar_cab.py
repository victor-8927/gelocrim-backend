"""
GELOCRIM - Importador Cabecalho da Nota (formato Sankhya exportado)
Cabecalho real na linha 2 (linhas 0 e 1 sao titulo/emissao)
"""
import sys, os, uuid, sqlite3
import pandas as pd

DB_PATH = r'C:\fleet-cloud\fleet.db'

def importar(xlsx_path):
    if not os.path.exists(xlsx_path):
        print(f'ERRO: Arquivo nao encontrado: {xlsx_path}')
        return

    print(f'Lendo: {xlsx_path}')
    df = pd.read_excel(xlsx_path, header=0, dtype=str)
    df = df.dropna(subset=['Nro. Unico' if 'Nro. Unico' in df.columns else 'Nro. \u00danico'])
    print(f'{len(df)} pedidos encontrados')

    # Normalizar nome coluna nunota
    col_nunota = None
    for col in df.columns:
        if 'nro' in col.lower() and ('nico' in col.lower() or 'unico' in col.lower()):
            col_nunota = col
            break
    if not col_nunota:
        print('ERRO: Coluna Nro. Unico nao encontrada')
        print('Colunas:', list(df.columns))
        return

    df = df.dropna(subset=[col_nunota])

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clientes
    clientes_db = {}
    for r in cur.execute('SELECT codparc, lat, lng, bairro, cidade, regiao, tempo_entrega, nome FROM clientes').fetchall():
        clientes_db[int(r[0])] = dict(lat=r[1], lng=r[2], bairro=r[3] or '',
            cidade=r[4] or 'Manaus', regiao=r[5] or '',
            tempo_entrega=r[6] or '', nome=r[7] or '')

    TOP_LABEL = {'1000':'Venda','1009':'Troca','1007':'Bonif.','1010':'Pre-ped.','1008':'Consig.'}

    imp = upd = ign = 0
    print()
    print(f'{"CLIENTE":<38} {"NUNOTA":>8} {"PESO kg":>8} {"VALOR R$":>10} {"TOP":>8}')
    print('-' * 78)

    for _, row in df.iterrows():
        try:
            nunota  = str(int(float(str(row[col_nunota]).strip())))
            codparc = int(float(str(row.get('Parceiro', '0') or '0').strip()))
            nome    = str(row.get('Nome Parceiro (Parceiro)', '') or '').strip()
            top_raw = str(row.get('Tipo Opera\u00e7\u00e3o', '1000') or '1000').strip()
            data_raw = str(row.get('Dt. Neg.', '') or '').strip()
            peso_raw = str(row.get('Peso', '0') or '0').strip()
            vlr_raw  = str(row.get('Vlr. Nota', '0') or '0').strip()
        except:
            continue

        try: top = str(int(float(top_raw)))
        except: top = '1000'

        try: data = pd.to_datetime(data_raw).strftime('%Y-%m-%d')
        except: data = ''

        try: peso = float(peso_raw.replace('.','').replace(',','.'))
        except: peso = 0

        try:
            # Valor pode vir como '488.7' (ponto decimal) ou '1.500,00' (formato BR)
            vlr_clean = vlr_raw.strip()
            if ',' in vlr_clean and '.' in vlr_clean:
                # Formato BR: 1.500,00 -> remover ponto milhar, trocar virgula
                vlr_clean = vlr_clean.replace('.','').replace(',','.')
            elif ',' in vlr_clean:
                # Apenas virgula: 488,70 -> trocar por ponto
                vlr_clean = vlr_clean.replace(',','.')
            # Se so tem ponto: 488.7 -> ja esta correto
            vlr = float(vlr_clean) if vlr_clean else 0
        except: vlr = 0

        # Dados do cliente
        cli     = clientes_db.get(codparc, {})
        lat     = cli.get('lat')
        lng     = cli.get('lng')
        bairro  = cli.get('bairro', '')
        cidade  = cli.get('cidade', 'Manaus')
        regiao  = cli.get('regiao', '')
        address = f'{bairro}, {cidade}'.strip(', ') if bairro else cidade

        # Janela
        try:
            mins = int(cli.get('tempo_entrega', '') or 0)
            tw_start = '07:00'
            tw_end   = f"{7 + mins//60:02d}:{mins%60:02d}"
        except:
            tw_start = '07:00'
            tw_end   = '18:00'

        # Nome: usar cadastro se vier vazio
        if not nome or nome.strip().lstrip('-').isdigit():
            nome = cli.get('nome', '') or nome

        print(f'{nome[:37]:<38} {nunota:>8} {peso:>8.0f} {vlr:>10.2f} {TOP_LABEL.get(top,top):>8}')

        existente = cur.execute('SELECT id, status FROM orders WHERE external_id=?', (nunota,)).fetchone()
        if existente:
            if existente[1] == 'pending':
                cur.execute('''UPDATE orders SET weight_kg=?, recipient_name=?, codparc=?,
                    lat=?, lng=?, address=?, regiao=?, delivery_date=?,
                    total_value=?, tw_start=?, tw_end=?, order_type=?,
                    updated_at=CURRENT_TIMESTAMP WHERE external_id=?''',
                    (peso, nome, codparc, lat, lng, address, regiao,
                     data, vlr, tw_start, tw_end, top, nunota))
                upd += 1
            else:
                ign += 1
        else:
            order_id = str(uuid.uuid4())
            cur.execute('''INSERT INTO orders
                (id, external_id, codparc, recipient_name, weight_kg,
                 lat, lng, address, regiao, delivery_date, total_value,
                 tw_start, tw_end, order_type, status, created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,'pending',CURRENT_TIMESTAMP)''',
                (order_id, nunota, codparc, nome, peso,
                 lat, lng, address, regiao, data, vlr,
                 tw_start, tw_end, top))
            imp += 1

    conn.commit()
    conn.close()
    print()
    print(f'OK: {imp} importados | {upd} atualizados | {ign} ignorados')
    print(f'Proximo: python importar_ti.py "arquivo_itens.xlsx"')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        importar(sys.argv[1])
    else:
        print('Uso: python importar_cab.py "caminho\\arquivo.xlsx"')
