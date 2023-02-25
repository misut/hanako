from datetime import datetime

from kyrie.models import AggregateRoot, DefaultDatetimeField, DomainEvent, IDType

from hanako.domain.enums import MangaLanguage


class _PoolEntryEvent(DomainEvent):
    __entity_type__ = "PoolEntry"


class PoolEntryFetched(_PoolEntryEvent):
    manga_id: IDType
    entity: "PoolEntry"


class PoolEntryUpdated(_PoolEntryEvent):
    manga_id: IDType
    language: MangaLanguage
    updated_at: datetime


class PoolEntry(AggregateRoot):
    manga_id: IDType
    language: MangaLanguage

    created_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def fetch(cls, **kwargs: object) -> PoolEntryFetched:
        obj = cls(**kwargs)
        PoolEntryFetched.update_forward_refs()
        return PoolEntryFetched(manga_id=obj.manga_id, entity=obj)
