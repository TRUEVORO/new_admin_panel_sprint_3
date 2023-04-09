import logging
from logging import config as logging_config

from models import Genre, Movie, Person
from utils import LOGGING_CONFIG

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


class Transformer:
    """Transformer class for Postgres to Elasticsearch data."""

    def __init__(self, model: type[Genre | Movie | Person]):
        """Initialization of transformer class."""

        self.model = model

    def transform(self, batch: list[dict]) -> list[dict]:
        """Transform Postgres data to Elasticsearch format."""

        logger.info('Transforming new data')

        return [self.model(**data).dict(by_alias=True) for data in batch]
