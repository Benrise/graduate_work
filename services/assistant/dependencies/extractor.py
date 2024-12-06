
from db.redis import get_cache
from fastapi import Depends
from flair.models import SequenceTagger
from services.extractor import EntityExtractorService
from utils.abstract import AsyncCacheStorage

NER_MODEL: SequenceTagger = None


def get_entity_extractor_service(cache: AsyncCacheStorage = Depends(get_cache)) -> EntityExtractorService:
    return EntityExtractorService(
        cache=cache,
        model=NER_MODEL,
    )
