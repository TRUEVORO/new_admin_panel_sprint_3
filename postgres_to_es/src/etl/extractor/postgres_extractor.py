import logging
import threading
from logging import config as logging_config
from typing import Generator

from psycopg2.errors import ConnectionFailure
from psycopg2.sql import SQL, Identifier, Placeholder

from clients import PostgresClient
from state import State
from utils import LOGGING_CONFIG, Mapper, backoff

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class PostgresExtractor:
    """Class for extracting data from Postgres."""

    def __init__(self, postgres_client: PostgresClient, state: State, mapper: Mapper, batch_size: int):
        """Initialization of PostgresExtractor."""

        self.client = postgres_client
        self.state = state
        self.mapper = mapper
        self.batch_size = batch_size
        self.monitor_query = SQL(
            '''
            SELECT MAX(modified) AS last_modified
            FROM {table}
            WHERE modified > {last_modified}
            '''
        ).format(table=Identifier('content', self.mapper.table), last_modified=Placeholder())

    @backoff(ConnectionFailure)
    def _monitor(self, previously_modified: str) -> str | None:
        """Monitor data from Postgres by modified field."""

        logger.info('Monitoring new %s data', self.mapper.index)

        self.client.execute(
            self.monitor_query,
            [
                previously_modified,
            ],
        )

        return self.client.cursor.fetchone()[0]

    @backoff(ConnectionFailure)
    def extract(self) -> Generator[tuple[list, str], None, None]:
        """Extract movies from Postgres."""

        with threading.Lock():
            previously_modified = self.state.get_state(self.mapper.index)

        if last_modified := self._monitor(previously_modified):
            logger.info('Extracting new %s data', self.mapper.index)

            self.client.execute(
                self.mapper.query,
                [
                    previously_modified,
                ],
            )

            while data := self.client.cursor.fetchmany(size=self.batch_size):
                yield data, str(last_modified)
