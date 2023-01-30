import abc

import pydantic

from hanako.models import IDType, ImmutableModel, ValueObject


class MangaPage(ValueObject):
    filename: str = pydantic.Field(None, alias="name")
    width: int
    height: int
    hash: str

    hasavif: bool | None
    haswebp: bool | None


class MangaTag(ValueObject):
    key: str
    val: str


class Manga(ImmutableModel):
    id: IDType
    title: str
    language: str
    pages: list[MangaPage] = pydantic.Field(None, alias="files")

    tags: list[MangaTag] = pydantic.Field([])


class MangaService(abc.ABC):
    @abc.abstractmethod
    async def fetch_ids(self, offset: int, limit: int) -> list[IDType]:
        ...

    @abc.abstractmethod
    async def fetch_manga(self, manga_id: IDType) -> Manga:
        ...

    @abc.abstractmethod
    async def download_page(self, manga_id: IDType, page: MangaPage) -> None:
        ...

    @abc.abstractmethod
    async def download_manga(self, manga: Manga) -> None:
        ...
