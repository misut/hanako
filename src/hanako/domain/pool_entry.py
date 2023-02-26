from datetime import datetime

from kyrie.models import AggregateRoot, DefaultDatetimeField, DomainEvent, IDType

from hanako.domain.enums import MangaLanguage


class _PoolEntryEvent(DomainEvent):
    __entity_type__ = "PoolEntry"


class PoolEntryFetched(_PoolEntryEvent):
    entity: "PoolEntry"


class PoolEntry(AggregateRoot):
    manga_id: IDType
    language: MangaLanguage

    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def fetch(cls, **kwargs: object) -> PoolEntryFetched:
        obj = cls(**kwargs)
        PoolEntryFetched.update_forward_refs()
        return PoolEntryFetched(entity_id=obj.manga_id, entity=obj)
