from kyrie.models import Command, IDType, MultiCommand

__all__ = (
    "CacheManga",
    "CacheMangaPage",
    "FetchManga",
    "FetchMangaList",
    "FetchPool",
)


class FetchManga(Command):
    manga_id: IDType


class FetchMangaList(MultiCommand):
    manga_id_list: list[IDType]


class CacheManga(MultiCommand):
    manga_id: IDType


class CacheMangaPage(Command):
    manga_id: IDType
    page_number: int


class FetchPool(MultiCommand):
    language: str
    offset: int = 0
    limit: int = 0
