import pathlib
from collections.abc import Mapping, Sequence
from datetime import datetime

from kyrie.models import (
    AggregateRoot,
    DefaultDatetimeField,
    DomainEvent,
    Entity,
    IDType,
)


class MangaArtist(Entity):
    name: str


class MangaPage(Entity):
    filename: str
    url: str

    cached_in: str | None = None


class MangaTag(Entity):
    tag: str


class _MangaEvent(DomainEvent):
    __entity_type__ = "Manga"


class MangaFetched(_MangaEvent):
    entity: "Manga"


class MangaCached(_MangaEvent):
    cached_in: str


class Manga(AggregateRoot):
    id: IDType
    title: str
    thumbnail: str
    pages: list[MangaPage]

    cached_in: str | None = None
    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def create(cls, **kwargs: object) -> MangaFetched:
        obj = cls(**kwargs)
        MangaFetched.update_forward_refs()
        return MangaFetched(entity_id=obj.id, entity=obj)

    def cache(self, dir_path: str) -> MangaCached:
        path = pathlib.Path(dir_path)
        if path.is_file():
            raise ValueError(f"'{path.name}' Not Directory")

        self.cached_in = dir_path
        for page in self.pages:
            page.cached_in = str(path.joinpath(page.filename))
        return MangaCached(entity_id=self.id, cached_in=dir_path)

    def is_cached(self) -> bool:
        return self.cached_in is not None
