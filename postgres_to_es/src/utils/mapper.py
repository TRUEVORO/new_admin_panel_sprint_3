from dataclasses import dataclass
from typing import Literal

from psycopg2.sql import SQL

from models import Genre, Movie, Person


@dataclass
class Mapper:
    """Mapper class for etl."""

    index: Literal['genres', 'movies', 'persons']
    table: Literal['genre', 'film_work', 'person']
    query: SQL | property
    model: type[Genre | Movie | Person]
