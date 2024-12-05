from enum import Enum


class Indecies(str, Enum):
    MOVIES = "movies"
    PERSONS = "persons"
    GENRES = "genres"
    ALL = "movies,persons,genres"
