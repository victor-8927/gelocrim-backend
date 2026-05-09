import sys, os
sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text

with engine_sync.connect() as conn:
    cols = conn.execute(text('PRAGMA table_info(drivers)')).fetchall()
    print('COLUNAS:', [c[1] for c in cols])
    print()
    rows = conn.execute(text('SELECT * FROM drivers')).fetchall()
    col_names = [c[1] for c in cols]
    print(f'TOTAL: {len(rows)} motoristas')
    print()
    for r in rows:
        d = dict(zip(col_names, r))
        print(f"  Nome: {d.get('name')} | ID: {str(d.get('id',''))[:8]}...")
