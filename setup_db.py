from app.database import engine_sync
from sqlalchemy import text
from passlib.context import CryptContext
import uuid

pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')

with engine_sync.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'driver', driver_id TEXT, is_active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL DEFAULT (datetime('now')))"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS vehicles (id TEXT PRIMARY KEY, plate TEXT NOT NULL UNIQUE, model TEXT NOT NULL, type TEXT NOT NULL DEFAULT 'truck', capacity_kg REAL NOT NULL DEFAULT 0, capacity_m3 REAL NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'active', created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')))"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS drivers (id TEXT PRIMARY KEY, vehicle_id TEXT, name TEXT NOT NULL, cpf TEXT, cnh TEXT, cnh_category TEXT, phone TEXT, status TEXT NOT NULL DEFAULT 'active', created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')))"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS recipients (id TEXT PRIMARY KEY, name TEXT NOT NULL, address TEXT NOT NULL, lat REAL NOT NULL, lng REAL NOT NULL, phone TEXT, created_at TEXT DEFAULT (datetime('now')))"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, external_id TEXT UNIQUE, source TEXT DEFAULT 'manual', recipient_id TEXT NOT NULL, lat REAL NOT NULL, lng REAL NOT NULL, weight_kg REAL DEFAULT 0, volume_m3 REAL DEFAULT 0, tw_start TEXT, tw_end TEXT, nfe_status TEXT DEFAULT 'pending', status TEXT DEFAULT 'pending', notes TEXT, created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')))"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS routes (id TEXT PRIMARY KEY, vehicle_id TEXT NOT NULL, driver_id TEXT, route_date TEXT NOT NULL, status TEXT DEFAULT 'draft', total_distance_km REAL, total_stops INTEGER, planned_start TEXT, planned_end TEXT, optimized_at TEXT, created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')))"))
    conn.execute(text("CREATE TABLE IF NOT EXISTS stops (id TEXT PRIMARY KEY, route_id TEXT NOT NULL, order_id TEXT NOT NULL, sequence INTEGER NOT NULL, lat REAL NOT NULL, lng REAL NOT NULL, eta TEXT, status TEXT DEFAULT 'pending', failure_reason TEXT, created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')))"))
    h = pwd.hash('Fleet2026')
    conn.execute(text("INSERT OR IGNORE INTO users (id,name,email,password_hash,role) VALUES (:id,:n,:e,:h,'admin')"),
                 {'id': str(uuid.uuid4()), 'n': 'Admin', 'e': 'distribuicaogelorotas@gmail.com', 'h': h})
    conn.commit()
    print('Banco configurado e admin criado!')
