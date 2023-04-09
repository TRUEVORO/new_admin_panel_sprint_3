import logging
import threading
import time
from datetime import datetime
from logging import config as logging_config

from state import RedisStorage, State
from utils import LOGGING_CONFIG, Mapper, Settings

from .extractor import PostgresExtractor
from .loader import ElasticsearchLoader
from .transformer import Transformer

logger = logging.getLogger(__name__)
logging_config.dictConfig(LOGGING_CONFIG)


def etl(mapper: Mapper, settings: Settings) -> None:
    """ETL process for specific mapper."""

    logger.info('{} ETL is started'.format(mapper.index))

    state = State(storage=RedisStorage(redis_dsn=settings.redis_dsn))

    with threading.Lock():
        if not state.get_state(key=mapper.index):
            state.set_state(key=mapper.index, value=str(datetime.min))

    extractor = PostgresExtractor(
        postgres_dsn=settings.postgres_dsn, state=state, mapper=mapper, batch_size=settings.batch_size
    )
    transformer = Transformer(model=mapper.model)
    loader = ElasticsearchLoader(
        elasticsearch_dsn=settings.elasticsearch_dsn, state=state, index=mapper.index, batch_size=settings.batch_size
    )

    while True:
        for data, last_modified in extractor.extract():
            if data:
                transformed_data = transformer.transform(data)
                loader.load(transformed_data, last_modified)

        logger.info('{} ETL is finished, going to sleep for {} s'.format(mapper.index.title(), settings.timeout))
        time.sleep(settings.timeout)
