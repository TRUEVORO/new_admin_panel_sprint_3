import abc

from redis import Redis
from redis.exceptions import ConnectionError

from settings import backoff, RedisConfig


class State:
    @abc.abstractmethod
    def set_state(self, key: str, value: str) -> None:
        """Установить состояние для определённого ключа"""
        pass

    @abc.abstractmethod
    def get_state(self, key: str) -> dict:
        """Получить состояние по определённому ключу"""
        pass


class RedisState(State):
    def __init__(self, config: RedisConfig, redis_conn: Redis | None):
        self._config = config
        self._redis_connection = redis_conn

    @staticmethod
    def check_connection_status(redis_connection: Redis) -> bool:
        try:
            redis_connection.ping()
        except ConnectionError:
            return False
        return True

    @backoff()
    def _create_connection(self) -> Redis:
        return Redis(**self._config.dict())

    @property
    def redis_connection(self) -> Redis:
        if not any((self._redis_connection, self.check_connection_status(self._redis_connection))):
            self._redis_connection = self._create_connection()
        return self._redis_connection

    @backoff()
    def set_state(self, key: str, value: str) -> None:
        self.redis_connection.set(key, value.encode())

    @backoff()
    def get_state(self, key: str) -> dict | None:
        return self.redis_connection.get(key).decode() if self.redis_connection.get(key) is not None else None
