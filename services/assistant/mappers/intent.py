from typing import Dict, Callable, Awaitable, Union

from utils.enums import Intents, Indecies
from services.search import SearchService

ActionMethodType = Callable[[SearchService, list[str]], Awaitable[Dict]]
ResponseType = Callable[[Dict, list[str]], str]

INTENT_TO_ACTION_MAPPING: Dict[Intents, Dict[str, Union[ActionMethodType, ResponseType]]] = {
    Intents.GET_FILM_DURATION.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Фильм '{result['hits']['hits'][0]['_source']['title']}' длится {result['hits']['hits'][0]['_source'].get('duration', 'неизвестно')} минут."
            if result.get('hits', {}).get('hits') else f"К сожалению, информацию о длительности фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_GENRE.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Жанр фильма '{result['hits']['hits'][0]['_source']['title']}': {', '.join([genre['name'] for genre in result['hits']['hits'][0]['_source'].get('genres', [])])}."
            if result.get('hits', {}).get('hits') else f"К сожалению, жанр фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_RATING.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Рейтинг фильма '{result['hits']['hits'][0]['_source']['title']}' составляет {result['hits']['hits'][0]['_source'].get('imdb_rating', 'неизвестно')}."
            if result.get('hits', {}).get('hits') else f"К сожалению, рейтинг фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_ACTORS.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"В фильме '{result['hits']['hits'][0]['_source']['title']}' снимались: {', '.join([actor['full_name'] for actor in result['hits']['hits'][0]['_source'].get('actors', [])])}."
            if result.get('hits', {}).get('hits') else f"К сожалению, информацию об актерах фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_DIRECTORS.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Режиссер(ы) фильма '{result['hits']['hits'][0]['_source']['title']}': {', '.join([director['full_name'] for director in result['hits']['hits'][0]['_source'].get('directors', [])])}."
            if result.get('hits', {}).get('hits') else f"К сожалению, информацию о режиссере фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_BY_GENRE.value: {
        "method": lambda search_service, genres: search_service.search(index=Indecies.MOVIES.value, query={"match": {"genres.name": genres[0]}} if genres else {}),
        "response": lambda result, genres: (
            f"Фильмы в жанре '{genres[0]}': {', '.join([film['_source']['title'] for film in result['hits']['hits']])}."
            if result.get('hits', {}).get('hits') else f"К сожалению, фильмы в жанре '{genres[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_WRITERS.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Сценарист(ы) фильма '{result['hits']['hits'][0]['_source']['title']}': {', '.join([writer['full_name'] for writer in result['hits']['hits'][0]['_source'].get('writers', [])])}."
            if result.get('hits', {}).get('hits') else f"К сожалению, информацию о сценаристах фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_FILM_DESCRIPTION.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Описание фильма '{result['hits']['hits'][0]['_source']['title']}': {result['hits']['hits'][0]['_source'].get('description', 'неизвестно')}."
            if result.get('hits', {}).get('hits') else f"К сожалению, описание фильма '{films[0]}' найти не удалось."
        ),
    },
    Intents.GET_SIMILAR_FILMS.value: {
        "method": lambda search_service, films: search_service.search(index=Indecies.MOVIES.value, query={"match": {"title": films[0]}} if films else {}),
        "response": lambda result, films: (
            f"Похожие фильмы на '{result['hits']['hits'][0]['_source']['title']}': {', '.join(result['hits']['hits'][0]['_source'].get('similar_films', ['неизвестно']))}."
            if result.get('hits', {}).get('hits') else f"К сожалению, похожие фильмы на '{films[0]}' найти не удалось."
        ),
    },
}
