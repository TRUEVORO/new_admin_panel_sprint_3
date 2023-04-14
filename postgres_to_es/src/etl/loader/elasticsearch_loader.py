import logging
import threading
from logging import config as logging_config

from elasticsearch.exceptions import ConnectionError
from elasticsearch.helpers import bulk

from clients import ElasticsearchClient
from state import State
from utils import LOGGING_CONFIG, backoff

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class ElasticsearchLoader:
    """Clas for loading data to Elasticsearch."""

    def __init__(self, elasticsearch_client: ElasticsearchClient, state: State, index: str, batch_size: int):
        """Initialization of ElasticsearchLoader."""

        self.client = elasticsearch_client
        self.state = state
        self.index = index
        self.batch_size = batch_size

    @backoff(ConnectionError)
    def load(self, batch: list[dict], last_modified: str) -> None:
        """Load data to Elasticsearch."""

        logger.info('Loading new %s data', self.index)

        bulk(
            client=self.client.connection,
            actions=batch,
            index=self.index,
            chunk_size=self.batch_size,
        )

        logger.info('%s data is successfully loaded', self.index.title())

        with threading.Lock():
            self.state.set_state(self.index, last_modified)

        logger.info('Current %s state is updated', self.index)
