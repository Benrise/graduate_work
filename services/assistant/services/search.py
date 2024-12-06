import json
import httpx
import uuid
from typing import Dict, Union, Any

from utils.abstract import AsyncCacheStorage
from core.config import settings


SEARCH_SERVICE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class SearchService:
    def __init__(self, cache: AsyncCacheStorage, base_url: str):
        self.base_url = base_url
        self.cache = cache

    async def search(self, index: str, query: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/service/search?index={index}"
        cache_key = f"search:{index}:{query}"
        headers = {
            "X-Request-Id": str(uuid.uuid4()),
        }

        cached_data = await self._get_from_cache(cache_key)
        if cached_data:
            return cached_data

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=query, headers=headers)

        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        await self._set_to_cache(cache_key, data)
        return data

    async def get_films_titles(self, force_update: bool = False) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/films/titles/"
        cache_key = settings.titles_films_cache_key
        headers = {
            "X-Request-Id": str(uuid.uuid4()),
        }

        cached_data = await self._get_from_cache(cache_key)
        if cached_data and not force_update:
            return cached_data

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        await self._set_to_cache(cache_key, data)
        return data

    async def get_genres_titles(self, force_update: bool = False) -> Dict[str, Any]:
        url = f"{self.base_url}/movies/api/v1/genres/titles/"
        cache_key = settings.titles_genres_cache_key
        headers = {
            "X-Request-Id": str(uuid.uuid4()),
        }

        cached_data = await self._get_from_cache(cache_key)
        if cached_data and not force_update:
            return cached_data

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        await self._set_to_cache(cache_key, data)
        return data

    async def _set_to_cache(self, key: str, value: Any, expire: int = 3600) -> None:
        serialized_value = json.dumps(value)
        await self.cache.set(key, serialized_value, expire)

    async def _get_from_cache(self, key: str) -> Union[Dict[str, Any], None]:
        cached_data: Dict[str, Any] = await self.cache.get(key)
        if not cached_data:
            return None
        if isinstance(cached_data, str):
            cached_data = json.loads(cached_data)
        return cached_data
