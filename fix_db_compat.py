import os
from datetime import datetime, timezone

with open(r'C:\fleet-cloud\app\db_compat.py', 'w', encoding='utf-8') as f:
    f.write('''import os
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///")
IS_SQLITE = DATABASE_URL.startswith("sqlite")

def now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
''')

print('db_compat.py criado!')
