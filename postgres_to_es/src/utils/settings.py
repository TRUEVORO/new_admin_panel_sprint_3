from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, RedisDsn

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Settings model with DSN."""

    postgres_dsn: PostgresDsn
    elasticsearch_dsn: AnyHttpUrl
    redis_dsn: RedisDsn
    batch_size: int
    timeout: float

    class Config:
        env_file = BASE_DIR / '.env'
        env_file_encoding = 'utf-8'
