import pydantic

from hanako.models import IDType, ImmutableModel, ValueObject


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
    artists: list[HitomiArtist]
    pages: list[HitomiPage] = pydantic.Field(alias="files")

    related: list[IDType] = []
    tags: list[HitomiTag] = []
