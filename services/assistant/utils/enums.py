from enum import Enum


class Indecies(str, Enum):
    MOVIES = "movies"
    PERSONS = "persons"
    GENRES = "genres"
    ALL = "movies,persons,genres"


class Intents(str, Enum):
    GET_FILM_DURATION = "get_film_duration"
    GET_FILM_GENRE = "get_film_genre"
    GET_FILM_RATING = "get_film_rating"
    GET_FILM_ACTORS = "get_film_actors"
    GET_FILM_DIRECTORS = "get_film_directors"
    GET_FILM_BY_GENRE = "get_film_by_genre"
    GET_FILM_WRITERS = "get_film_writers"
    GET_FILM_DESCRIPTION = "get_film_description"
    GET_SIMILAR_FILMS = "get_similar_films"
