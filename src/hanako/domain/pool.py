from datetime import datetime
from typing import Any

from kyrie.models import (
    AggregateRoot,
    DefaultDatetimeField,
    DefaultIDField,
    DomainEvent,
    IDType,
)

from hanako.domain.enums import MangaLanguage


class _PoolEvent(DomainEvent):
    __entity_type__ = "Pool"


class PoolFetched(_PoolEvent):
    entity: "Pool"


class Pool(AggregateRoot):
    id: IDType = DefaultIDField
    manga_ids: list[IDType]
    language: MangaLanguage
    offset: int
    limit: int

    fetched_at: datetime = DefaultDatetimeField

    @classmethod
    def create(
        cls,
        manga_ids: list[str],
        language: str,
        offset: int,
        limit: int,
    ) -> PoolFetched:
        if language not in MangaLanguage:
            raise ValueError(f"Language '{language}' Not Supported")
        obj = cls(
            manga_ids=manga_ids,
            language=MangaLanguage(language),
            offset=offset,
            limit=limit,
        )
        return PoolFetched(entity_id=obj.id, entity=obj)
