from datetime import datetime

import pydantic

now = datetime.now

DefaultDatetimeField = pydantic.Field(default_factory=now)


def milliseconds_encoding(dt: datetime) -> str:
    return dt.isoformat(timespec="milliseconds")


class BaseModel(pydantic.BaseModel):
    class Config:
        json_encoders = {datetime: milliseconds_encoding}


class ImmutableModel(BaseModel):
    class Config:
        allow_mutation = False


class ValueObject(ImmutableModel):
    ...


class Command(ImmutableModel):
    triggered_by: str = ""


class HitomiFile(ValueObject):
    name: str
    width: int
    height: int
    hash: str

    hasavif: bool | None
    haswebp: bool | None


class HitomiGallery(ValueObject):
    id: str
    title: str
    language: str
    files: list[HitomiFile]
