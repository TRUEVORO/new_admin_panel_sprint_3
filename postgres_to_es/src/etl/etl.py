import logging
import threading
import time
from contextlib import closing
from datetime import datetime
from logging import config as logging_config

from clients import ElasticsearchClient, PostgresClient, RedisClient
from state import RedisStorage, State
from utils import LOGGING_CONFIG, Mapper, Settings

from .extractor import PostgresExtractor
from .loader import ElasticsearchLoader
from .transformer import Transformer

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


def etl(mapper: Mapper, settings: Settings) -> None:
    """ETL process for specific mapper."""

    logger.info('%s ETL is started', mapper.index.title())

    with closing(ElasticsearchClient(settings.elasticsearch_dsn)) as elasticsearch_client, closing(
        PostgresClient(settings.postgres_dsn)
    ) as postgres_client, closing(RedisClient(settings.redis_dsn)) as redis_client:
        state = State(storage=RedisStorage(redis_client=redis_client))

        with threading.Lock():
            if not state.get_state(key=mapper.index):
                state.set_state(key=mapper.index, value=str(datetime.min))

        extractor = PostgresExtractor(
            postgres_client=postgres_client, state=state, mapper=mapper, batch_size=settings.batch_size
        )
        transformer = Transformer(model=mapper.model)
        loader = ElasticsearchLoader(
            elasticsearch_client=elasticsearch_client, state=state, index=mapper.index, batch_size=settings.batch_size
        )

        while True:
            for data, last_modified in extractor.extract():
                if data:
                    transformed_data = transformer.transform(data)
                    loader.load(transformed_data, last_modified)

            logger.info('%s ETL is finished, going to sleep for %s s', mapper.index.title(), settings.timeout)
            time.sleep(settings.timeout)
