import logging
from functools import wraps

from pydantic import BaseSettings


logger = logging.getLogger(__name__)

LOGGER_CONFIG = {
    "format": "%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s",  # noqa 501
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO,
    "handlers": [logging.StreamHandler()],
}

logging.basicConfig(**LOGGER_CONFIG)


class Settings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PostgresDsn(Settings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_options: str


class ElasticConfig(Settings):
    elasticsearch_host: str
    elasticsearch_port: int


class RedisConfig(Settings):
    redis_host: str
    redis_port: int


class ETLConfig(Settings):
    batch_size: int
    frequency: int
    backoff_max_retries: int
    elasticsearch_indexes: list[str]


class ETLError(Exception):
    pass


def backoff(start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: int = 10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except ETLError:
                    logger.exception('Error while transferring data')
                    sleep_time = min(sleep_time * 2**factor, border_sleep_time)
        return inner

    return func_wrapper
