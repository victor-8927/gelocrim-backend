from app.database import engine_sync
from sqlalchemy import text

with engine_sync.connect() as conn:
    conn.execute(text('''CREATE TABLE IF NOT EXISTS route_gps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id TEXT NOT NULL,
        lat REAL, lng REAL, speed REAL, heading REAL,
        ts TEXT
    )'''))
    try:
        conn.execute(text('ALTER TABLE routes ADD COLUMN last_lat REAL'))
        print('OK: last_lat')
    except: print('last_lat ja existe')
    try:
        conn.execute(text('ALTER TABLE routes ADD COLUMN last_lng REAL'))
        print('OK: last_lng')
    except: print('last_lng ja existe')
    try:
        conn.execute(text('ALTER TABLE routes ADD COLUMN last_seen TEXT'))
        print('OK: last_seen')
    except: print('last_seen ja existe')
    conn.commit()
    print('PRONTO!')
