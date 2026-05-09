
import sys
sys.path.insert(0, r'C:\fleet-cloud')
from app.database import engine_sync
from sqlalchemy import text
with engine_sync.connect() as conn:
    for col in ['foto_boleto_url', 'foto_comodato_url', 'foto_outros_url']:
        try:
            conn.execute(text(f'ALTER TABLE route_stops ADD COLUMN {col} TEXT'))
            conn.commit()
            print(f'OK: coluna {col} adicionada!')
        except:
            print(f'coluna {col} ja existe')
