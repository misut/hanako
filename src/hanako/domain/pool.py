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
    id_list: list[IDType]


class Pool(AggregateRoot):
    id: IDType = DefaultIDField
    id_list: list[IDType]
    language: MangaLanguage
    offset: int
    limit: int

    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def create(cls, **kwargs: object) -> PoolFetched:
        obj = cls(**kwargs)
        PoolFetched.update_forward_refs()
        return PoolFetched(entity_id=obj.id, entity=obj)

    def update(self, id_list: list[IDType]) -> PoolUpdated:
        if set(self.id_list) > set(id_list):
            raise ValueError(f"Not Completely Including Current Pool")
        self.id_list = id_list
        return PoolUpdated(entity_id=self.id, id_list=id_list)
