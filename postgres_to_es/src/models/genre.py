from pydantic import Field

from .mixin import ElasticsearchIDMixin, UUIDMixin


class _Genre(UUIDMixin):
    """Genre base model."""

    name: str = Field(default_factory=str)


class Genre(_Genre, ElasticsearchIDMixin):
    """Genre model."""

    pass
