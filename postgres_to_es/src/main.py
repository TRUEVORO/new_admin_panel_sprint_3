import logging
from concurrent.futures import ThreadPoolExecutor
from logging import config as logging_config

from etl import QueryTemplates, etl
from models import Genre, Movie, Person
from utils import LOGGING_CONFIG, Mapper, Settings

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging_config.dictConfig(LOGGING_CONFIG)

    settings = Settings()

    query_templates = QueryTemplates()

    GENRE_MAPPER = Mapper('genres', 'genre', query_templates.GENRES_QUERY, Genre)
    MOVIES_MAPPER = Mapper('movies', 'film_work', query_templates.MOVIES_QUERY, Movie)
    PERSON_MAPPER = Mapper('persons', 'person', query_templates.PERSONS_QUERY, Person)

    with ThreadPoolExecutor(max_workers=3) as pool:
        logger.info('Starting ETL')

        pool.submit(etl, GENRE_MAPPER, settings)
        pool.submit(etl, MOVIES_MAPPER, settings)
        pool.submit(etl, PERSON_MAPPER, settings)
