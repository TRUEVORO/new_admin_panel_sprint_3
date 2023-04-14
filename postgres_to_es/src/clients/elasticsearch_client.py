from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from utils import backoff

from .base_client import BaseClient


class ElasticsearchClient(BaseClient):
    """Elasticsearch client."""

    @backoff(ConnectionError)
    def _reconnect(self) -> Elasticsearch:
        """Reconnect to Elasticsearch client if no connection exists."""

        return Elasticsearch(self.dsn)
