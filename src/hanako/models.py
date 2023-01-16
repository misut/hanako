import pydantic

BaseModel = pydantic.BaseModel


class ImmutableModel(BaseModel):
    class Config:
        allow_mutation = False


class ValueObject(ImmutableModel):
    ...


class HitomiFile(ValueObject):
    name: str
    width: int
    height: int
    hash: str


class HitomiGallery(ValueObject):
    id: str
    title: str
    language: str
    files: list[HitomiFile]
