from collections.abc import Mapping, Sequence
from datetime import datetime

from kyrie.models import (
    AggregateRoot,
    DefaultDatetimeField,
    DomainEvent,
    Entity,
    IDType,
)


class MangaPage(Entity):
    filename: str
    hash: str
    url: str

    cached_in: str | None = None


class _MangaEvent(DomainEvent):
    __entity_type__ = "Manga"


class MangaFetched(_MangaEvent):
    entity: "Manga"


class Manga(AggregateRoot):
    id: IDType
    title: str
    thumbnail: str
    pages: list[MangaPage]

    fetched_at: datetime = DefaultDatetimeField
    updated_at: datetime = DefaultDatetimeField

    @classmethod
    def create(
        cls,
        id: IDType,
        title: str,
        thumbnail: str,  # base64 encoded
        pages: Sequence[Mapping[str, int | str]],
    ) -> MangaFetched:
        obj = cls(
            id=id,
            title=title,
            thumbnail=thumbnail,
            pages=pages,
        )
        MangaFetched.update_forward_refs()
        return MangaFetched(entity_id=obj.id, entity=obj)
