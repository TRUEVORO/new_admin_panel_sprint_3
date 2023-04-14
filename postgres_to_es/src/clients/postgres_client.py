import psycopg2
from psycopg2.errors import ConnectionFailure
from psycopg2.extensions import connection as postgres_connection
from psycopg2.extensions import cursor as postgres_cursor
from psycopg2.extras import DictCursor
from psycopg2.sql import Composable
from pydantic import PostgresDsn

from utils import backoff

from .base_client import BaseClient


class PostgresClient(BaseClient):
    """Postgres client."""

    def __init__(self, dsn: PostgresDsn, connection: postgres_connection | None = None):
        """Initialization of Postgres client."""

        super().__init__(dsn, connection)

        self.cursor: postgres_cursor = self.connection.cursor()

    @backoff(ConnectionFailure)
    def _reconnect(self) -> postgres_connection:
        """Reconnect to Postgres client if no connection exists."""

        return psycopg2.connect(self.dsn, cursor_factory=DictCursor)

    def close(self) -> None:
        """Close Postgres client connection."""

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute(self, query: str | bytes | Composable, *args, **kwargs) -> None:
        """Postgres client execute query."""

        self.cursor.execute(query, *args, **kwargs)

    def fetchmany(self, size: int) -> list:
        """Postgres client execute fetchmany."""

        return self.cursor.fetchmany(size=size)
