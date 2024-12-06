import re
from typing import List

import orjson
from core.config import settings
from flair.data import Sentence
from flair.models import SequenceTagger
from utils.abstract import AsyncCacheStorage


class EntityExtractorService:
    def __init__(self, cache: AsyncCacheStorage, model: SequenceTagger):
        self.model = model
        self.cache = cache

    async def extract_persons(self, text: str) -> List[str]:
        sentence = Sentence(text)
        self.model.predict(sentence)

        return [entity.text for entity in sentence.get_spans('ner') if entity.get_label("ner").value == "PER"]

    async def extract_genres(self, text: str) -> List[str]:
        genres = []
        genres_titles = await self._get_titles_from_cache(settings.titles_genres_cache_key)
        for genre in genres_titles:
            pattern = re.compile(rf"\b{re.escape(genre.lower())}\b", re.IGNORECASE)
            if pattern.search(text):
                genres.append(genre)
        return genres

    async def extract_films(self, text: str) -> List[str]:
        films = []
        films_titles = await self._get_titles_from_cache(settings.titles_films_cache_key)
        for film in films_titles:
            pattern = re.compile(rf"\b{re.escape(film.lower())}\b", re.IGNORECASE)
            if pattern.findall(text) and film not in films:
                films.append(film)
        return films

    async def _get_titles_from_cache(self, cache_key: str):
        titles = await self.cache.get(cache_key)
        if not titles:
            return None
        return orjson.loads(titles)
