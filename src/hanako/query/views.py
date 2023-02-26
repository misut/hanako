from datetime import datetime

from kyrie.models import IDType, View

from hanako.domain.enums import MangaLanguage


class MangaPageView(View):
    __entity_type__ = "MangaPage"

    filename: str
    cached_in: str | None


class MangaView(View):
    __entity_type__ = "Manga"

    id: IDType
    language: str
    title: str
    thumbnail: str
    pages: list[MangaPageView]
    fetched_at: datetime
    updated_at: datetime

    @property
    def num_pages(self) -> int:
        return len(self.pages)


class PoolEntryView(View):
    __entity_type__ = "PoolEntry"

    manga_id: IDType
    language: MangaLanguage
    fetched_at: datetime
    updated_at: datetime
