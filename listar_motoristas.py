import sys, os
sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text

with engine_sync.connect() as conn:
    # Lista motoristas existentes
    rows = conn.execute(text('SELECT id, name, license_number FROM drivers')).fetchall()
    print('MOTORISTAS NO BANCO:')
    for r in rows:
        print(f'  ID: {r[0]}')
        print(f'  Nome: {r[1]}')
        print(f'  CNH: {r[2]}')
        print()
