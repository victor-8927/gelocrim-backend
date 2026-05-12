from sqlalchemy import text
from app.database import engine_sync

def garantir_colunas():
    cmds = [
        # stops table
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS photo_nf TEXT",
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS photo_receipt TEXT",
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS photo_loan TEXT",
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS photo_other TEXT",
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS lat_confirmed DOUBLE PRECISION",
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS lng_confirmed DOUBLE PRECISION",
        "ALTER TABLE stops ADD COLUMN IF NOT EXISTS segment TEXT",

        # routes table
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS total_stops INTEGER DEFAULT 0",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS delivered_stops INTEGER DEFAULT 0",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS assistant1_id TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS assistant2_id TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS last_lat DOUBLE PRECISION",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS last_lng DOUBLE PRECISION",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS last_seen TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS optimized_at TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS km_start INTEGER",
        "ALTER TABLE routes ADD COLUMN IF NOT EXISTS km_end INTEGER",

        # orders table
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS source TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS notes TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 1",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_date DATE",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_type TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_value DOUBLE PRECISION",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS region TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS invoice_status TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS invoice_number TEXT",

        # drivers table
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS license_category TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS fixed_vehicle TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS daily_cost DOUBLE PRECISION",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS hire_date TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS notes TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS photo TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS license_photo TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS day_off TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS work_hours TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS lunch_time TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS updated_at TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS vda TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS assistant_id TEXT",
        "ALTER TABLE drivers ADD COLUMN IF NOT EXISTS shift TEXT",

        # vehicles table
        "ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS updated_at TEXT",

        # clients table
        "ALTER TABLE clients ADD COLUMN IF NOT EXISTS updated_at TEXT",

        # ocorrencias table
        """CREATE TABLE IF NOT EXISTS incidents (
            id TEXT PRIMARY KEY,
            route_id TEXT,
            stop_id TEXT,
            type TEXT,
            description TEXT,
            status TEXT DEFAULT 'pending',
            severity TEXT DEFAULT 'info',
            invoice TEXT,
            client TEXT,
            vehicle TEXT,
            photo TEXT,
            signature TEXT,
            lat DOUBLE PRECISION,
            lng DOUBLE PRECISION,
            created_at TEXT,
            resolved_at TEXT,
            updated_at TEXT
        )""",

        # gps_logs partitions for future months
        """CREATE TABLE IF NOT EXISTS gps_logs_2026_07
            PARTITION OF gps_logs
            FOR VALUES FROM ('2026-07-01') TO ('2026-08-01')""",
        """CREATE TABLE IF NOT EXISTS gps_logs_2026_08
            PARTITION OF gps_logs
            FOR VALUES FROM ('2026-08-01') TO ('2026-09-01')""",
    ]

    with engine_sync.connect() as conn:
        for sql in cmds:
            try:
                conn.execute(text(sql))
            except Exception:
                pass
        conn.commit()
