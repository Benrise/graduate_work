import spacy
import re
from typing import List


class EntityExtractorService:
    def __init__(self, model: str, genres: List[str], films: List[str]):
        self.nlp = spacy.load(model)
        self.genres_titles = genres
        self.films_titles = films

    def extract_persons(self, text: str) -> List[str]:
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    def extract_genres(self, text: str) -> List[str]:
        doc = self.nlp(text)
        genres = []
        for genre in self.genres_titles:
            pattern = re.compile(rf"\b{re.escape(genre.lower())}\b", re.IGNORECASE)
            if pattern.search(doc.text):
                genres.append(genre)
        return genres

    def extract_films(self, text: str) -> List[str]:
        doc = self.nlp(text)
        films = []
        for film in self.films_titles:
            pattern = re.compile(rf"\b{re.escape(film.lower())}\b", re.IGNORECASE)
            if pattern.findall(doc.text):
                films.append(film)
        return films
