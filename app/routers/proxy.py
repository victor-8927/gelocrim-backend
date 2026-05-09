
from fastapi import APIRouter, Depends
import httpx

router_proxy = APIRouter(prefix="/api/v1/proxy", tags=["Proxy"])

@router_proxy.get("/directions")
async def directions_proxy(
    origin: str, destination: str, waypoints: str = ""
):
    key = "AIzaSyB47DpEZW4qbU74LxcG1ZD76cYLRlJw88M"
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "region": "br",
        "language": "pt-BR",
        "key": key
    }
    if waypoints:
        params["waypoints"] = waypoints
    
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params, timeout=30)
        return res.json()
