import sys, os, uuid, sqlite3
import pandas as pd

DB_PATH = r'C:\fleet-cloud\fleet.db'

PESO_ITEM = {'370': 6, '371': 11, '372': 23, '373': 45}
NOME_ITEM = {'370': 'GELO 05KG', '371': 'GELO 10KG', '372': 'GELO 20KG', '373': 'GELO 40KG'}

def extr_codparc_nome(v):
    p = str(v).split(' - ', 1)
    try:
        cod = int(p[0].strip())
        nome = p[1].strip() if len(p) > 1 else ''
        return cod, nome
    except:
        return None, str(v).strip()

def extr_cod_item(v):
    p = str(v).split(' - ', 1)
    try: return str(int(p[0].strip()))
    except: return None

def extr_top(v):
    p = str(v).split(' - ', 1)
    try: return str(int(p[0].strip()))
    except: return '1000'

def importar(xlsx_path):
    if not os.path.exists(xlsx_path):
        print(f'ERRO: Arquivo nao encontrado: {xlsx_path}')
        return

    print(f'Lendo: {xlsx_path}')
    df = pd.read_excel(xlsx_path, dtype=str)

    col_nunota = None
    for col in df.columns:
        if 'nro' in col.lower() and ('nico' in col.lower() or 'unico' in col.lower()):
            col_nunota = col
            break
    if not col_nunota:
        print('ERRO: Coluna Nro. Unico nao encontrada')
        return

    df = df.dropna(subset=[col_nunota])
    print(f'{len(df)} linhas encontradas')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Pesos reais do banco
    pesos_db = {}
    for r in cur.execute("SELECT nome, peso FROM itens_producao").fetchall():
        n = r[0].lower()
        if '5' in n and 'kg' in n: pesos_db['370'] = float(r[1])
        elif '10' in n and 'kg' in n: pesos_db['371'] = float(r[1])
        elif '20' in n and 'kg' in n: pesos_db['372'] = float(r[1])
        elif '40' in n and 'kg' in n: pesos_db['373'] = float(r[1])
    if pesos_db:
        PESO_ITEM.update(pesos_db)
        print(f'   Pesos: {PESO_ITEM}')

    # Clientes do banco (nome e dados)
    clientes_db = {}
    for r in cur.execute('SELECT codparc, lat, lng, bairro, cidade, regiao, tempo_entrega, nome FROM clientes').fetchall():
        clientes_db[int(r[0])] = dict(
            lat=r[1], lng=r[2], bairro=r[3] or '',
            cidade=r[4] or 'Manaus', regiao=r[5] or '',
            tempo_entrega=r[6] or '', nome=r[7] or ''
        )

    # Valores da TGFCAB ja no banco
    valores_db = {}
    for r in cur.execute('SELECT external_id, total_value FROM orders WHERE total_value IS NOT NULL').fetchall():
        valores_db[str(r[0])] = float(r[1])

    # Processar linhas
    notas = {}
    for _, row in df.iterrows():
        try:
            nunota   = str(int(float(str(row[col_nunota]).strip())))
            parceiro = str(row.get('Parceiro', '') or '')
            item_raw = str(row.get('Item', '') or '')
            qtd_raw  = str(row.get('Quantidade', '0') or '0')
            top_raw  = str(row.get('TOP', '1000') or '1000')
            data_raw = str(row.get('Data', '') or '')

            codparc, nome_raw = extr_codparc_nome(parceiro)
            cod_item = extr_cod_item(item_raw)
            top      = extr_top(top_raw)
            nome_item = NOME_ITEM.get(cod_item, item_raw)
            peso_unit = PESO_ITEM.get(cod_item, 0)

            # Nome: usar cadastro de clientes se nome_raw for so numeros ou vazio
            if codparc and (not nome_raw or nome_raw.strip().lstrip('-').isdigit()):
                nome = clientes_db.get(codparc, {}).get('nome', '') or nome_raw
            else:
                nome = nome_raw

            try: qtd = int(float(qtd_raw.replace(',', '.')))
            except: qtd = 0

            try: data = pd.to_datetime(data_raw).strftime('%Y-%m-%d')
            except: data = ''

            if nunota not in notas:
                notas[nunota] = {
                    'codparc': codparc, 'nome': nome,
                    'top': top, 'data': data, 'itens': {}
                }

            key_item = (top, cod_item)
            if key_item not in notas[nunota]['itens']:
                notas[nunota]['itens'][key_item] = {
                    'cod': cod_item, 'nome': nome_item,
                    'peso_unit': peso_unit, 'qtd': 0, 'top': top
                }
            notas[nunota]['itens'][key_item]['qtd'] += qtd
        except:
            continue

    print(f'{len(notas)} notas identificadas')

    # Resumo por cliente
    por_cliente = {}
    for nunota, nota in notas.items():
        cp = nota['codparc']
        if cp not in por_cliente:
            por_cliente[cp] = {'nome': nota['nome'], 'notas': [], 'itens_top': {}}
        por_cliente[cp]['notas'].append(nunota)
        for (top, cod), item in nota['itens'].items():
            if top not in por_cliente[cp]['itens_top']:
                por_cliente[cp]['itens_top'][top] = {}
            if cod not in por_cliente[cp]['itens_top'][top]:
                por_cliente[cp]['itens_top'][top][cod] = {'nome': item['nome'], 'qtd': 0, 'peso_unit': item['peso_unit']}
            por_cliente[cp]['itens_top'][top][cod]['qtd'] += item['qtd']

    print()
    print(f'{"CLIENTE":<38} {"NOTAS":>5}  ITENS POR TOP')
    print('-' * 80)
    for cp, cli in sorted(por_cliente.items(), key=lambda x: x[0] or 0):
        nome = cli['nome'][:37]
        n_notas = len(cli['notas'])
        itens_str = []
        for top in sorted(cli['itens_top'].keys()):
            it = cli['itens_top'][top]
            peso = sum(v['qtd'] * v['peso_unit'] for v in it.values())
            lista = ', '.join(f"{v['qtd']}x{v['nome']}" for v in it.values())
            itens_str.append(f"TOP{top}[{lista} = {peso}kg]")
        print(f'{nome:<38} {n_notas:>5}  {" | ".join(itens_str)}')

    print()
    print('Salvando no banco...')

    imp_orders = upd_orders = imp_items = 0

    for nunota, nota in notas.items():
        codparc = nota['codparc']
        nome    = nota['nome']
        data    = nota['data']
        top_nota = nota['top']

        peso_total = sum(item['qtd'] * item['peso_unit'] for item in nota['itens'].values())

        cli     = clientes_db.get(codparc, {})
        lat     = cli.get('lat')
        lng     = cli.get('lng')
        bairro  = cli.get('bairro', '')
        cidade  = cli.get('cidade', 'Manaus')
        regiao  = cli.get('regiao', '')
        address = f'{bairro}, {cidade}'.strip(', ') if bairro else cidade

        # Janela de entrega
        tempo = cli.get('tempo_entrega', '') or ''
        try:
            mins = int(tempo)
            tw_start = '07:00'
            tw_end   = f"{7 + mins//60:02d}:{mins%60:02d}"
        except:
            tw_start = '07:00'
            tw_end   = '18:00'

        valor_nota = valores_db.get(str(nunota))

        existente = cur.execute('SELECT id, status, recipient_name FROM orders WHERE external_id=?', (nunota,)).fetchone()

        if existente:
            if existente[1] == 'pending':
                # Preservar nome existente se for melhor
                nome_banco = existente[2] or ''
                if nome_banco and not nome_banco.strip().lstrip('-').isdigit() and len(nome_banco) > 5:
                    nome_final = nome_banco
                else:
                    nome_final = nome

                cur.execute('''UPDATE orders SET weight_kg=?, recipient_name=?,
                    codparc=?, lat=?, lng=?, address=?, regiao=?,
                    delivery_date=?, tw_start=?, tw_end=?, order_type=?,
                    updated_at=CURRENT_TIMESTAMP
                    WHERE external_id=?''',
                    (peso_total, nome_final, codparc, lat, lng, address, regiao,
                     data, tw_start, tw_end, top_nota, nunota))
                # Atualizar valor so se nao tiver
                if valor_nota:
                    cur.execute('UPDATE orders SET total_value=COALESCE(total_value,?) WHERE external_id=?',
                                (valor_nota, nunota))
                upd_orders += 1
            order_id = existente[0]
        else:
            order_id = str(uuid.uuid4())
            cur.execute('''INSERT INTO orders
                (id, external_id, codparc, recipient_name, weight_kg,
                 lat, lng, address, regiao, delivery_date, total_value,
                 tw_start, tw_end, order_type, status, created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,'pending',CURRENT_TIMESTAMP)''',
                (order_id, nunota, codparc, nome, peso_total,
                 lat, lng, address, regiao, data, valor_nota,
                 tw_start, tw_end, top_nota))
            imp_orders += 1

        # Itens vinculados ao NUNOTA
        cur.execute('DELETE FROM order_items WHERE nunota=?', (nunota,))
        for (top_k, cod_k), item in nota['itens'].items():
            if item['qtd'] <= 0:
                continue
            cur.execute('''INSERT INTO order_items
                (codparc, nunota, top_app, item_tipo, item_nome, peso_unit, qtd, dt_neg, created_at)
                VALUES(?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)''',
                (int(codparc), str(nunota), str(top_k), str(item['cod']),
                 str(item['nome']), float(item['peso_unit']),
                 int(item['qtd']), str(data)))
            imp_items += 1

    conn.commit()
    conn.close()

    print(f'Orders: {imp_orders} inseridos, {upd_orders} atualizados')
    print(f'Itens:  {imp_items} inseridos (vinculados por NUNOTA)')
    print()
    print('Concluido!')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        importar(sys.argv[1])
    else:
        print('Uso: python importar_ti.py caminho\\planilha.xlsx')
