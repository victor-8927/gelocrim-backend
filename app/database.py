from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL_SYNC

# check_same_thread so funciona no SQLite
is_sqlite = DATABASE_URL_SYNC.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine_sync = create_engine(DATABASE_URL_SYNC, connect_args=connect_args)
SyncSession = sessionmaker(engine_sync, expire_on_commit=False)

def get_db():
    with SyncSession() as session:
        yield session

def init_schema():
    pass
