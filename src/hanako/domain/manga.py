import pathlib
from datetime import datetime

from kyrie.models import (
    AggregateRoot,
    DefaultDatetimeField,
    DomainEvent,
    Entity,
    IDType,
)

from hanako.domain.enums import MangaLanguage
from hanako.domain.exceptions import PageCachedPathError, PageNumberError


def _check_cached(page: "MangaPage") -> bool:
    return page.cached_in is not None


class MangaArtist(Entity):
    name: str


class MangaPage(Entity):
    filename: str
    hash: str
    hasavif: bool
    haswebp: bool

    cached_in: str | None = None


class MangaTag(Entity):
    tag: str


class _MangaEvent(DomainEvent):
    __entity_type__ = "Manga"


class MangaFetched(_MangaEvent):
    entity: "Manga"


class MangaPageCached(_MangaEvent):
    page_number: int
    cached_in: str


class Manga(AggregateRoot):
    id: IDType
    language: MangaLanguage
    title: str
    thumbnail: str
    artists: list[MangaArtist]
    pages: list[MangaPage]
    tags: list[MangaTag]

    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def fetch(cls, **kwargs: object) -> MangaFetched:
        obj = cls(**kwargs)
        MangaFetched.update_forward_refs()
        return MangaFetched(entity_id=obj.id, entity=obj)

    def cache_page(self, page_number: int, file_path: str) -> MangaPageCached:
        if not self.is_page_number_valid(page_number):
            raise PageNumberError(f"Invalid Page Number '{page_number}'")

        cached_path = pathlib.Path(file_path)
        if cached_path.is_dir():
            raise PageCachedPathError(f"'{cached_path.name}' Not File But Directory")

        self.pages[page_number].cached_in = str(cached_path)
        return MangaPageCached(
            entity_id=self.id,
            page_number=page_number,
            cached_in=self.pages[page_number].cached_in,
        )

    def is_cached(self) -> bool:
        return all(_check_cached(page) for page in self.pages)

    def is_page_cached(self, page_number: int) -> bool:
        if not self.is_page_number_valid(page_number):
            raise PageNumberError(f"Invalid Page Number '{page_number}'")
        return _check_cached(self.pages[page_number])

    def is_page_number_valid(self, page_number: int) -> bool:
        return 0 <= page_number < len(self.pages)
