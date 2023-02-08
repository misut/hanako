import pathlib
from datetime import datetime
from typing import Any

from kyrie.models import AggregateRoot, DefaultDatetimeField, DomainEvent, IDType, now


class _MangaEvent(DomainEvent):
    __entity_type__ = "Manga"


class MangaCached(_MangaEvent):
    cached_in: pathlib.Path
    updated_at: datetime


class MangaFlushed(_MangaEvent):
    updated_at: datetime


class MangaFetched(_MangaEvent):
    title: str
    fetched_at: datetime
    updated_at: datetime


class MangaUpdated(_MangaEvent):
    title: str
    updated_at: datetime


class Manga(AggregateRoot):
    id: IDType
    title: str

    cached_in: pathlib.Path | None = None
    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def create(cls, **data: Any) -> MangaFetched:
        obj = cls(**data)
        return MangaFetched(
            entity_id=obj.id,
            title=obj.title,
            fetched_at=obj.fetched_at,
            updated_at=obj.updated_at,
        )

    def is_cached(self) -> bool:
        if self.cached_in is not None:
            return True
        return False

    def flush_cache(self) -> MangaFlushed:
        self.cached_in = None
        self.updated_at = now()
        return MangaFlushed(
            entity_id=self.id,
            updated_at=self.updated_at,
        )

    def sync_cache(self, cached_in: pathlib.Path) -> MangaCached:
        self.cached_in = cached_in
        self.updated_at = now()
        return MangaCached(
            entity_id=self.id,
            cached_in=self.cached_in,
            updated_at=self.updated_at,
        )

    def update(self, title: str) -> MangaUpdated:
        self.title = title
        self.updated_at = now()
        return MangaUpdated(
            entity_id=self.id,
            title=self.title,
            updated_at=self.updated_at,
        )
