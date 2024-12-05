import httpx
from typing import Dict, Any

from fastapi import Request


class SearchService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def search(self, request: Request, index: str, query: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/service/search?index={index}"
        headers = {
            "X-Request-Id": request.headers.get("X-Request-Id"),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query, headers=headers)

        response.raise_for_status()
        return response.json()
