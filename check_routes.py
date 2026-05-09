import sys, os
sys.path.insert(0, r'C:\fleet-cloud')
os.chdir(r'C:\fleet-cloud')

from app.database import engine_sync
from sqlalchemy import text

with engine_sync.connect() as conn:
    cols = conn.execute(text('PRAGMA table_info(routes)')).fetchall()
    print('COLUNAS DA TABELA ROUTES:')
    for c in cols:
        print(f'  {c[1]} ({c[2]})')

    print('\nDADOS:')
    rows = conn.execute(text('SELECT * FROM routes LIMIT 5')).fetchall()
    for r in rows:
        print(dict(zip([c[1] for c in cols], r)))
