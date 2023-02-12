from typing import Any
import pydantic
from kyrie.models import IDType, ImmutableModel, ValueObject


class HitomiArtist(ValueObject):
    name: str = pydantic.Field(alias="artist")
    url: str


class HitomiPage(ValueObject):
    filename: str = pydantic.Field(alias="name")
    width: int
    height: int
    hash: str

    hasavif: bool | None
    haswebp: bool | None


class HitomiTag(ValueObject):
    tag: str
    url: str

    female: bool | None
    male: bool | None

    @pydantic.validator("female", "male", pre=True)
    def parse_bool(cls, value: str | int) -> bool | str | int:
        if value == "":
            return False
        return value


class HitomiGallery(ImmutableModel):
    id: IDType
    title: str
    type: str
    language: str
    galleryurl: str
    pages: list[HitomiPage] = pydantic.Field(alias="files")

    artists: list[HitomiArtist] = []
    related: list[IDType] = []
    tags: list[HitomiTag] = []

    @pydantic.validator("artists", "related", "tags", pre=True)
    def parse_none(cls, value: None | Any) -> list | Any:
        return value or []
