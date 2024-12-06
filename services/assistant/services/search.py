import httpx
import uuid
from typing import Dict, Any


class SearchService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def search(self, index: str, query: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/service/search?index={index}"
        headers = {
            "X-Request-Id": str(uuid.uuid4()),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query, headers=headers)

        response.raise_for_status()
        return response.json()

    async def get_films_titles(self) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/films/titles/"
        headers = {
            "X-Request-Id": str(uuid.uuid4()),
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()

        return response.json()

    async def get_genres_titles(self) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/genres/titles/"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        response.raise_for_status()

        return response.json()
