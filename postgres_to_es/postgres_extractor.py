from typing import Iterator

import psycopg2
from pydantic import BaseModel
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from models import GenresES, MoviesES, PersonsES
from settings import backoff, PostgresDsn


INDEX_MAPPER = {
    'movies': MoviesES,
    'genres': GenresES,
    'persons': PersonsES,
}


class PostgresExtractor:
    def __init__(
        self,
        dsn: PostgresDsn,
        postgres_connection: _connection | None = None,
    ):
        self._dsn = dsn
        self._postgres_connection = postgres_connection

    @property
    def postgres_connection(self) -> _connection:
        """Создает новый объект сессии, если он еще не инициализирован либо закрыт"""
        if self._postgres_connection is None or self._postgres_connection.closed:
            self._postgres_connection = self._create_connection()

        return self._postgres_connection

    @backoff()
    def _create_connection(self) -> _connection:
        """Переподключение к бд."""
        if self._postgres_connection is not None:
            self._postgres_connection.close()

        return psycopg2.connect(**self._dsn.dict(), cursor_factory=DictCursor)

    @backoff()
    def _get_generator(self, model: type[BaseModel], query: str, itersize: int) -> Iterator[tuple]:
        """Форматирование данных под ES."""
        cur = self.postgres_connection.cursor()
        cur.itersize = itersize
        cur.execute(query)

        for row in cur:
            instance = model(**row).dict()
            instance['_id'] = instance['id']
            yield instance, str(row['updated_at'])

    def extract_data(self, index: str, query: str, itersize: int) -> Iterator[tuple]:
        model = INDEX_MAPPER.get(index) or BaseModel

        if model != BaseModel:
            return self._get_generator(model, query, itersize)

        raise ValueError(f'No extract process for index {index}')
