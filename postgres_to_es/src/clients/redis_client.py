from redis import Redis
from redis.exceptions import ConnectionError
from redis.typing import EncodableT, KeyT

from utils import backoff

from .base_client import BaseClient


class RedisClient(BaseClient):
    """Redis client."""

    @backoff(ConnectionError)
    def _reconnect(self) -> Redis:
        """Reconnect to Redis if no connection exists."""

        return Redis(host=self.dsn.host, port=int(self.dsn.port), db=self.dsn.path[1:])

    @backoff(ConnectionError)
    def set(self, name: KeyT, value: EncodableT, *args, **kwargs) -> None:
        """Redis client execute set."""

        self.connection.set(name, value, *args, **kwargs)

    @backoff(ConnectionError)
    def get(self, name: KeyT) -> bytes | None:
        """Redis client execute get."""

        return self.connection.get(name)
