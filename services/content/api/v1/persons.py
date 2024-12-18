from http import HTTPStatus
from typing import List

import core.config as config
from fastapi import APIRouter, Depends, HTTPException, Query
from models.abstract import PaginatedParams
from models.film import FilmRating
from models.person import PersonFilms
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/{person_id}',
            response_model=PersonFilms,
            summary='Получить информацию о жанре людях по его uuid',
            description='''
                Формат данных ответа:
                        uuid,
                        full_name,
                        films
                    ''')
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonFilms:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return PersonFilms(uuid=person.uuid, full_name=person.full_name, films=person.films)


@router.get('/search/',
            response_model=List[PersonFilms],
            summary='Получить список людей',
            description='Формат массива данных ответа: uuid, full_name, films')
async def persons_list(
        query: str = Query(
            default='Lucas',
            alias=config.QUERY_ALIAS,
            description=config.QUERY_DESC
        ),
        pagination: PaginatedParams = Depends(),
        person_service: PersonService = Depends(get_person_service)) -> List[PersonFilms]:
    persons: List[PersonFilms] = await person_service.get_persons(
        query,
        pagination.page,
        pagination.size,
    )
    if not persons:
        persons = []
    return persons


@router.get('/{person_id}/film', response_model=List[FilmRating])
async def person_by_films(person_id: str, person_service: PersonService = Depends(get_person_service)) -> List[FilmRating]:
    person_films = await person_service.get_person_film_rating(person_id)
    if not person_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return [FilmRating(uuid=person_id, title=p_film.title, imdb_rating=p_film.imdb_rating) for p_film in person_films]
