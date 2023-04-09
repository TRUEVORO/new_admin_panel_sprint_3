from pydantic import Field

from .mixin import ElasticsearchIDMixin, UUIDMixin


class _Person(UUIDMixin):
    """Person model without films."""

    full_name: str = Field(default_factory=str)


class _Movie(UUIDMixin):
    """Movie model with person's roles."""

    roles: list[str] = Field(default_factory=list)


class Person(_Person, ElasticsearchIDMixin):
    """Person model with films."""

    films: list[_Movie] = Field(default_factory=list)
