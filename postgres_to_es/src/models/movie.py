from pydantic import Field, validator

from .genre import _Genre
from .mixin import ElasticsearchIDMixin
from .person import _Person


class Movie(ElasticsearchIDMixin):
    """Movie model."""

    title: str
    imdb_rating: float | None = Field(default=None)
    description: str | None = Field(default=None)
    genres: list[_Genre] = Field(default_factory=list)
    actors: list[_Person] = Field(default_factory=list)
    directors: list[_Person] = Field(default_factory=list)
    writers: list[_Person] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)

    @validator('actors_names', pre=True, always=True)
    def set_actors_full_names(cls, v: list, values: dict) -> list[str]:  # noqa
        """Set actors full names in Movie model."""

        actors = values.get('actors', v)
        return [actor.full_name for actor in actors]

    @validator('writers_names', pre=True, always=True)
    def set_writers_full_names(cls, v: list, values: dict) -> list[str]:  # noqa
        """Set writers full names in Movie model."""

        writers = values.get('writers', v)
        return [writer.full_name for writer in writers]
