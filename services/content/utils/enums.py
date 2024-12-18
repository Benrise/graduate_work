from enum import Enum


class Sort(str, Enum):
    asc = 'asc',
    desc = 'desc'


class EventType(str, Enum):
    MOVIE_PROGRESS = "movie_progress"
    MOVIE_DETAILS = "movie_details"
    MOVIE_FILTERS = "movie_filters"

    def __str__(self):
        return self.value


class Indecies(str, Enum):
    MOVIES = "movies"
    PERSONS = "persons"
    GENRES = "genres"
    ALL = "movies,persons,genres"
