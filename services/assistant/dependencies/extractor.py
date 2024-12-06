

from typing import List
from services.extractor import EntityExtractorService
from utils.logger import logger
from core.config import settings
from services.search import SearchService

GENRES_TITLES_LIST: List[str] = None
FILMS_TITLES_LIST: List[str] = None


def get_entity_extractor_service() -> EntityExtractorService:
    return EntityExtractorService(
        model='en_core_web_sm',
        genres=GENRES_TITLES_LIST,
        films=FILMS_TITLES_LIST
    )


async def update_data_titles():
    global GENRES_TITLES_LIST, FILMS_TITLES_LIST
    search_service = SearchService(settings.search_service_url)
    GENRES_TITLES_LIST = await search_service.get_genres_titles()
    FILMS_TITLES_LIST = await search_service.get_films_titles()
    logger.info("Genres and Films titles was successfully updated")
