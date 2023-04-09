from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class UUIDMixin(BaseModel):
    """Mixin uuid model."""

    uuid: UUID = Field(default_factory=uuid4, alias='id')


class ElasticsearchIDMixin(UUIDMixin):
    """Mixin uuids model with extra '_id' field."""

    es_id: UUID = Field(default_factory=uuid4, alias='_id')

    @validator('es_id', pre=True, always=True)
    def set_id_for_es(cls, v: UUID, values: dict) -> UUID:
        """Set extra '_id' field for Elasticsearch."""

        return values.get('uuid', v)
