import logging
from logging import config as logging_config

from utils import LOGGING_CONFIG

from .base_storage import BaseStorage

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class State:
    """Class for working with states."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: str) -> None:
        """Set status for a specific key."""

        logging.info('Saving %s state', key)

        self.storage.save_state(key, value)

    def get_state(self, key: str) -> str | None:
        """Get status on a specific key."""

        logging.info('Get current %s state', key)

        return self.storage.retrieve_state(key)
