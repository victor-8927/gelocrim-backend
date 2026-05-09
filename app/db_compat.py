import os
from datetime import datetime, timezone

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///")
IS_SQLITE = DATABASE_URL.startswith("sqlite")

def now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
