"""
Autenticacao Sankhya via API REST OAuth2 + fallback legado.
Configure no .env:
    SANKHYA_GATEWAY_URL, SANKHYA_CLIENT_ID, SANKHYA_CLIENT_SECRET,
    SANKHYA_TOKEN, SANKHYA_USERNAME, SANKHYA_PASSWORD
"""
import os, time, logging, httpx
logger = logging.getLogger(__name__)

GATEWAY_URL   = os.getenv("SANKHYA_GATEWAY_URL", "https://api.sankhya.com.br")
CLIENT_ID     = os.getenv("SANKHYA_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SANKHYA_CLIENT_SECRET", "")
X_TOKEN       = os.getenv("SANKHYA_TOKEN", "")
USERNAME      = os.getenv("SANKHYA_USERNAME", "")
PASSWORD      = os.getenv("SANKHYA_PASSWORD", "")

_cache = {"token": None, "expires_at": 0}

async def get_access_token() -> str:
    if _cache["token"] and time.time() < _cache["expires_at"] - 60:
        return _cache["token"]
    if CLIENT_ID and CLIENT_SECRET:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.post(f"{GATEWAY_URL}/auth/oauth/token",
                    headers={"Content-Type":"application/x-www-form-urlencoded","token":X_TOKEN},
                    data={"grant_type":"client_credentials","client_id":CLIENT_ID,"client_secret":CLIENT_SECRET})
                r.raise_for_status()
                d = r.json()
                _cache["token"] = d["access_token"]
                _cache["expires_at"] = time.time() + d.get("expires_in", 3600)
                return _cache["token"]
        except Exception as e:
            logger.warning(f"OAuth falhou: {e}")
    if USERNAME and PASSWORD:
        try:
            async with httpx.AsyncClient(timeout=15) as c:
                r = await c.post(f"{GATEWAY_URL}/mge/service.sbr?serviceName=MobileLoginSP.login&outputType=json",
                    json={"serviceName":"MobileLoginSP.login","requestBody":{"NOMUSU":{"$":USERNAME},"INTERNO":{"$":"S"},"NUNOTA":{"$":"0"}}})
                r.raise_for_status()
                t = r.json().get("responseBody",{}).get("jsessionid",{}).get("$")
                if t:
                    _cache["token"] = t
                    _cache["expires_at"] = time.time() + 3600
                    return t
        except Exception as e:
            logger.error(f"Login legado falhou: {e}")
    raise RuntimeError("Nao foi possivel obter token Sankhya. Verifique credenciais no .env")

async def get_headers() -> dict:
    token = await get_access_token()
    return {"Authorization": f"Bearer {token}", "token": X_TOKEN, "Content-Type": "application/json"}

async def test_connection() -> dict:
    try:
        headers = await get_headers()
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{GATEWAY_URL}/mge/service.sbr?serviceName=AwsUtil.ping&outputType=json", headers=headers)
            if r.status_code < 400:
                return {"status": "ok", "message": f"Conexao Sankhya estabelecida! ({GATEWAY_URL})"}
            return {"status": "error", "message": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
