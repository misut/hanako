import uuid
from datetime import datetime
from typing import ClassVar, cast

import pydantic

__all__ = (
    "AggregateRoot",
    "BaseModel",
    "Command",
    "DomainEvent",
    "Entity",
    "IDType",
    "ImmutableModel",
    "Query",
    "ValueObject",
    "View",
    "generate_id",
    "now",
)

IDType = str


def generate_id() -> IDType:
    return cast(IDType, str(uuid.uuid4()))


now = datetime.now

DefaultDatetimeField = pydantic.Field(default_factory=now)
DefaultIDField = pydantic.Field(default_factory=generate_id)


def milliseconds_encoding(dt: datetime) -> str:
    return dt.isoformat(timespec="milliseconds")


class BaseModel(pydantic.BaseModel):
    class Config:
        json_encoders = {datetime: milliseconds_encoding}


class Entity(BaseModel):
    class Config:
        underscore_attrs_are_private = True


class AggregateRoot(Entity):
    ...


class ImmutableModel(BaseModel):
    class Config:
        allow_mutation = False


class ValueObject(ImmutableModel):
    ...


class Command(ImmutableModel):
    triggered_by: str = ""


class Query(ImmutableModel):
    ...


class DomainEvent(ImmutableModel):
    __entity_type__: ClassVar[str]

    entity_id: IDType
    occurred_at: datetime = DefaultDatetimeField


class View(ImmutableModel):
    class Config:
        orm_mode = True
