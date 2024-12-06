from core.config import settings
from services.search import SearchService
from utils.abstract import AsyncCacheStorage
from db.redis import get_cache
from fastapi import Depends


def get_search_service(cache: AsyncCacheStorage = Depends(get_cache)):
    return SearchService(cache, settings.search_service_url)
