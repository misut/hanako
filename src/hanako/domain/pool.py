from datetime import datetime

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


class PoolUpdated(_PoolEvent):
    manga_ids: list[IDType]


class Pool(AggregateRoot):
    id: IDType = DefaultIDField
    manga_ids: list[IDType]
    language: MangaLanguage
    offset: int
    limit: int

    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def create(
        cls,
        manga_ids: list[str],
        language: str,
        offset: int,
        limit: int,
    ) -> PoolFetched:
        if not any(language == member.value for member in MangaLanguage):
            raise ValueError(f"Language '{language}' Not Supported")
        obj = cls(
            manga_ids=manga_ids,
            language=MangaLanguage(language),
            offset=offset,
            limit=limit,
        )
        PoolFetched.update_forward_refs()
        return PoolFetched(entity_id=obj.id, entity=obj)

    def update(self, manga_ids: list[IDType]) -> PoolUpdated:
        if set(self.manga_ids) > set(manga_ids):
            raise ValueError(f"Not Completely Including Current Pool")
        self.manga_ids = manga_ids
        return PoolUpdated(entity_id=self.id, manga_ids=manga_ids)
