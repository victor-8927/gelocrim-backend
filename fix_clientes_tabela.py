import sqlite3

db_path = r'C:\fleet-cloud\fleet.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Verifica estrutura atual
cur.execute("PRAGMA table_info(clientes)")
cols = cur.fetchall()
col_names = [c[1] for c in cols]
print('Colunas atuais:', col_names)

# Colunas necessárias
needed = {
    'codparc': 'INTEGER',
    'nome': 'TEXT',
    'razao_social': 'TEXT',
    'endereco': 'TEXT',
    'cep': 'TEXT',
    'bairro': 'TEXT',
    'cidade': 'TEXT',
    'lat': 'REAL',
    'lng': 'REAL',
    'cpf_cnpj': 'TEXT',
    'segmento': 'TEXT',
    'zona_geo': 'TEXT',
    'regiao': 'TEXT',
    'comodatos': 'TEXT',
    'tempo_entrega': 'TEXT',
    'rota': 'TEXT',
    'telefone': 'TEXT',
    'ativo': 'TEXT DEFAULT "S"',
}

# Adiciona colunas faltando
for col, tipo in needed.items():
    if col not in col_names:
        try:
            cur.execute(f'ALTER TABLE clientes ADD COLUMN {col} {tipo}')
            print(f'Coluna adicionada: {col}')
        except Exception as e:
            print(f'Erro em {col}: {e}')

# Verifica se tabela existe, se não cria
if not cols:
    print('Criando tabela clientes...')
    cur.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codparc INTEGER UNIQUE,
        nome TEXT, razao_social TEXT, endereco TEXT,
        cep TEXT, bairro TEXT, cidade TEXT,
        lat REAL, lng REAL, cpf_cnpj TEXT,
        segmento TEXT, zona_geo TEXT, regiao TEXT,
        comodatos TEXT, tempo_entrega TEXT, rota TEXT,
        telefone TEXT, ativo TEXT DEFAULT "S"
    )''')
    print('Tabela criada!')

conn.commit()
conn.close()
print('Pronto!')
