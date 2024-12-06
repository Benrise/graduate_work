from flair.models import SequenceTagger

from services.search import SearchService
from utils.logger import logger
from utils.abstract import AsyncCacheStorage
from core.config import settings
from dependencies import extractor


class LifespanManager:
    def __init__(self, cache: AsyncCacheStorage):
        self.cache = cache

    async def update_data_titles(self):
        search_service = SearchService(self.cache, settings.search_service_url)
        genres_titles = await search_service.get_genres_titles(force_update=True)
        films_titles = await search_service.get_films_titles(force_update=True)
        logger.info(f"Genres [{len(genres_titles)}] and Films [{len(films_titles)}] titles was successfully updated")

    async def upload_ner_model(self):
        logger.info("Starting to load NER model...")
        extractor.NER_MODEL = SequenceTagger.load("ner")
        logger.info("NER model successfully loaded.")
