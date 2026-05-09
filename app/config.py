import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "fleet-routing-chave-secreta-2026-gelocrim")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_TTL = 60
REFRESH_TOKEN_TTL = 7 * 24 * 60
DEPOT_LAT = float(os.getenv("DEPOT_LAT", "-3.093544"))
DEPOT_LNG = float(os.getenv("DEPOT_LNG", "-60.075812"))
VRP_TIME_LIMIT = int(os.getenv("VRP_TIME_LIMIT_SEC", "30"))
DATABASE_URL_SYNC = os.getenv("DATABASE_URL", "sqlite:///C:/fleet-cloud/fleet.db")
