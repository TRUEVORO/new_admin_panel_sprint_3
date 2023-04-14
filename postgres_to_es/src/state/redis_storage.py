from clients import RedisClient

from .base_storage import BaseStorage


class RedisStorage(BaseStorage):
    """Redis state storage."""

    def __init__(self, redis_client: RedisClient) -> None:
        """Initialize Redis storage."""

        self.redis = redis_client

    def save_state(self, key: str, value: str) -> None:
        """Save state in storage."""

        self.redis.set(key, value.encode())

    def retrieve_state(self, key: str) -> str | None:
        """Retrieve state from storage."""

        return self.redis.get(key).decode() if self.redis.get(key) else None
