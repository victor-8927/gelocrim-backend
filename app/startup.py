from sqlalchemy import text
from app.database import engine_sync

def garantir_colunas():
    cmds = [
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS cnh_category TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS veiculo_fixo TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS daily_cost REAL",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS data_admissao TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS observacoes TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS foto TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS cnh_foto TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS dia_folga TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS carga_horaria TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS hora_almoco TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS vda TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS ajudante_id TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS jornada TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS custo_dia REAL",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS total_stops INTEGER DEFAULT 0",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS delivered_stops INTEGER DEFAULT 0",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS ajudante1_id TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS ajudante2_id TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS last_lat REAL",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS last_lng REAL",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS last_seen TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS optimized_at TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS source TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS notes TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS priority INTEGER",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_date TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_type TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_value REAL",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS regiao TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS nfe_status TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS nunota TEXT",
        "ALTER TABLE route_stops ADD COLUMN IF NOT EXISTS foto_boleto_url TEXT",
        "ALTER TABLE route_stops ADD COLUMN IF NOT EXISTS foto_comodato_url TEXT",
        "ALTER TABLE route_stops ADD COLUMN IF NOT EXISTS foto_outros_url TEXT",
        "ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS updated_at TEXT",
        """CREATE TABLE IF NOT EXISTS pallets (
            id TEXT PRIMARY KEY, nome TEXT, comprimento REAL,
            largura REAL, altura REAL, peso_max REAL, created_at TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS itens (
            id TEXT PRIMARY KEY, nome TEXT, codigo TEXT,
            peso_unit REAL, unidade TEXT, created_at TEXT
        )""",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS gravidade TEXT DEFAULT 'info'",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS pedido TEXT",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS cliente TEXT",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS veiculo TEXT",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS foto TEXT",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS assinatura TEXT",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS gerar_devolucao INTEGER DEFAULT 0",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS atualizar_estoque INTEGER DEFAULT 0",
        "ALTER TABLE ocorrencias ADD COLUMN IF NOT EXISTS updated_at TEXT",
        """CREATE TABLE IF NOT EXISTS ocorrencias (
            id TEXT PRIMARY KEY, route_id TEXT, stop_id TEXT,
            tipo TEXT, descricao TEXT, status TEXT DEFAULT 'pendente',
            created_at TEXT, resolved_at TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS itens_producao (
            id TEXT PRIMARY KEY, nome TEXT, peso REAL DEFAULT 0,
            comprimento REAL DEFAULT 0, largura REAL DEFAULT 0,
            altura REAL DEFAULT 0, un_pallet INTEGER DEFAULT 0,
            top TEXT DEFAULT '1000', observacao TEXT,
            created_at TEXT, updated_at TEXT
        )""",
    ]
    with engine_sync.connect() as conn:
        for sql in cmds:
            try:
                conn.execute(text(sql))
            except Exception:
                pass
        conn.commit()
