from uuid import UUID

from pydantic import BaseModel


class FilmType(str):
    movie = 'movie'
    tv_show = 'tv_show'


class PersonType(str):
    actor = 'actor'
    director = 'director'
    writer = 'writer'


class Model(BaseModel):
    id: UUID


class PersonInFilm(Model):
    name: str


class GenresES(Model):
    name: str


class PersonsES(PersonInFilm):
    role: list[PersonType] | None
    film_ids: list[UUID] | None


class MoviesES(Model):
    title: str
    imdb_rating: float | None
    type: FilmType
    description: str | None
    genres: list[GenresES] | None
    directors: list[PersonInFilm] | None
    actors: list[PersonInFilm] | None
    writers: list[PersonInFilm] | None
    file_path: str | None
