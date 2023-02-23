from datetime import datetime

from kyrie.models import IDType, View

from hanako.domain.enums import MangaLanguage


class MangaPageView(View):
    filename: str
    cached_in: str | None


class MangaView(View):
    __entity_type__ = "Manga"

    id: IDType
    title: str
    thumbnail: str
    pages: list[MangaPageView]
    fetched_at: datetime
    updated_at: datetime

    @property
    def num_pages(self) -> int:
        return len(self.pages)


class PoolView(View):
    __entity_type__ = "Pool"

    id: IDType
    id_list: list[IDType]
    language: MangaLanguage
    offset: int
    limit: int
    fetched_at: datetime
    updated_at: datetime
