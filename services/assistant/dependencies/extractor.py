
from flair.models import SequenceTagger

from fastapi import Depends
from utils.abstract import AsyncCacheStorage
from db.redis import get_cache
from services.extractor import EntityExtractorService

NER_MODEL: SequenceTagger = None


def get_entity_extractor_service(cache: AsyncCacheStorage = Depends(get_cache)) -> EntityExtractorService:
    return EntityExtractorService(
        cache=cache,
        model=NER_MODEL,
    )
