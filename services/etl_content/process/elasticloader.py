import json
from typing import Any, Dict, Text

from utils.logger import logger
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "sentence-transformers/sentence-t5-base"


class ElasticLoader:
    """Class to load data to Elasticseach."""

    def __init__(self, client: object) -> None:
        self.client = client
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def get_sentence_embeddings(self, text: str) -> list:
        """
        Generate sentence embeddings using the configured model.
        """
        sentence_embeddings = self.embedding_model.encode(text).tolist()
        return sentence_embeddings

    def create_index(self, index: str, index_data: Text) -> bool:
        """Method to create an index in Elasticsearch."""

        if self.client.ping():
            logger.info(
                'Response received successfully. Elastichsearch is working.'
            )

            exists_index = self.client.indices.exists(index=index)

            if not exists_index:
                with open(index_data, 'r') as file:
                    data = file.read()
                    idx = json.loads(data)
                    settings = idx['settings']
                    mappings = idx['mappings']

                create_index = self.client.indices.create(
                    index=index, settings=settings, mappings=mappings
                )
                if create_index['acknowledged']:
                    logger.info(
                        f'The index {index} was successfully created.'
                    )
            else:
                logger.info(f'The index {index} already exists.')
            return True
        else:
            logger.warning(
                'The request could not be made. Elasticsearch is not working.'
            )
            return False

    def _check_doc_exists(self, index: str, id: str) -> bool:
        """
        Private method to check the existence of the
        document in Elastichsearch.

        Return True if exists, otherwise False.
        """
        check = self.client.exists(index=index, id=id)
        return check

    def add_movie(self, index: str, data: Dict[str, Any]) -> None:
        """Method to create a film."""
        id = data['uuid']
        rating = 0.0 if not data['imdb_rating'] else data['imdb_rating']
        rating = float(rating)

        if not self._check_doc_exists(index, id):
            combined_text = self.generate_combined_text_movie(data)
            embedding_vector = self.get_sentence_embeddings(combined_text)

            self.client.index(
                index=index,
                id=id,
                body={
                    "uuid": f"{id}",
                    "title": data["title"],
                    "imdb_rating": float(data["imdb_rating"] or 0.0),
                    "description": data["description"],
                    "genres": data["genres"],
                    "actors": data["actors"],
                    "writers": data["writers"],
                    "directors": data["directors"],
                    "embedding_vectors": embedding_vector
                },
            )

            logger.info(f"Added movie: {data['title']}")

    def add_person(self, index: str, data: Dict[str, Any]) -> None:
        """Add all information about the persons."""
        person_id = data['uuid']

        if not self._check_doc_exists(index, person_id):
            combined_text = self.generate_combined_text_movie(data)
            embedding_vector = self.get_sentence_embeddings(combined_text)

            self.client.index(
                index=index,
                id=person_id,
                body={
                    "uuid": f"{person_id}",
                    "full_name": data["full_name"],
                    "films": data["films"],
                    "embedding_vectors": embedding_vector
                },
            )

            logger.info(f"Added person: {data['full_name']}")

    def add_genre(self, index: str, data: Dict[str, Any]) -> None:
        """Method to add all related data to genres."""
        genre_id = data['uuid']

        if not self._check_doc_exists(index, genre_id):
            combined_text = self.generate_combined_text_genre(data)
            embedding_vector = self.get_sentence_embeddings(combined_text)

            self.client.index(
                index=index,
                id=genre_id,
                body={
                    "uuid": f"{genre_id}",
                    "name": data["name"],
                    "combined_text": combined_text,
                    "embedding_vectors": embedding_vector
                },
            )

            logger.info(f"Added genre: {data['name']}")

    def generate_combined_text_movie(self, data: Dict[str, Any]) -> str:
        """
        Generate combined text for movies.
        """
        def extract_names(items):
            return [
                item.get('name') or item.get('full_name') if isinstance(item, dict) else str(item)
                for item in items
            ]

        return (
            f"Title: {data['title']}. "
            f"Description: {data['description'] or ''}. "
            f"Genres: {', '.join(extract_names(data['genres']))}. "
            f"Actors: {', '.join(extract_names(data['actors']))}. "
            f"Writers: {', '.join(extract_names(data['writers']))}. "
            f"Directors: {', '.join(extract_names(data['directors']))}."
        )

    def generate_combined_text_person(self, data: Dict[str, Any]) -> str:
        """
        Generate combined text for persons.
        """
        return (
            f"Name: {data['full_name']}. "
            f"Films: {', '.join(data['films'])}."
        )

    def generate_combined_text_genre(self, data: Dict[str, Any]) -> str:
        """
        Generate combined text for genres.
        """
        return f"Genre: {data['name']}."
