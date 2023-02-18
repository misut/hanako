from datetime import datetime

from kyrie.models import IDType, View

from hanako.domain.enums import MangaLanguage


class MangaView(View):
    __entity_type__ = "Manga"

    id: IDType
    title: str
    thumbnail: str
    fetched_at: datetime
    updated_at: datetime


class PoolView(View):
    __entity_type__ = "Pool"

    id: IDType
    manga_ids: list[IDType]
    language: MangaLanguage
    offset: int
    limit: int
    fetched_at: datetime
    updated_at: datetime
