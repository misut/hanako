from kyrie.models import Command, IDType, MultiCommand

__all__ = (
    "CacheManga",
    "FetchManga",
    "FetchPool",
    "UpdatePool",
)


class FetchManga(Command):
    manga_id: IDType


class FetchMangaUsingPool(MultiCommand):
    pool_id: IDType
    offset: int = 0
    limit: int = 0


class CacheManga(Command):
    manga_id: IDType


class FetchPool(Command):
    language: str
    offset: int = 0
    limit: int = 0


class UpdatePool(Command):
    pool_id: IDType
