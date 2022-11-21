import logging
import time
from datetime import datetime

from settings import (
    ETLConfig,
    ElasticConfig,
    LOGGER_CONFIG,
    PostgresDsn,
    RedisConfig,
)
from elastic_saver import ElasticSaver
from postgres_extractor import PostgresExtractor
from query import get_query_by_index
from state import RedisState


state = RedisState(RedisConfig())
postgres_extractor = PostgresExtractor(PostgresDsn())
elastic_loader = ElasticSaver(ElasticConfig(), state)


itersize = ETLConfig().batch_size
freq = ETLConfig().frequency
indexes = ETLConfig().elasticsearch_indexes

logger = logging.getLogger(__name__)
logging.basicConfig(**LOGGER_CONFIG)


def transfer_data() -> None:
    """Запись данных в Elasticsearch по запросу."""
    while True:
        logger.info("Starting sync...")

        for index in indexes:
            load_from = state.get_state(f"load_from_{index}", default=str(datetime.min))

            try:
                query = get_query_by_index(index, load_from)
                data_generator = postgres_extractor.extract_data(index, query, itersize)
                elastic_loader.upload_data(data_generator, itersize, index)

            except ValueError as e:
                logger.error("Skipping index %s: %s", index, e)
                continue

        logger.info("Sleep for %s seconds", freq)
        time.sleep(freq)


if __name__ == "__main__":
    transfer_data()
