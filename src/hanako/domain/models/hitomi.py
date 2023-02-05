import pydantic

from hanako.models import IDType, ImmutableModel, ValueObject


class HitomiPage(ValueObject):
    filename: str = pydantic.Field(alias="name")
    width: int
    height: int
    hash: str

    hasavif: bool | None
    haswebp: bool | None


class HitomiTag(ValueObject):
    key: str
    val: str


class HitomiGallery(ImmutableModel):
    id: IDType
    title: str
    language: str
    pages: list[HitomiPage] = pydantic.Field(alias="files")
    tags: list[HitomiTag] = []
