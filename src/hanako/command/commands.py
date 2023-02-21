from kyrie.models import Command, IDType

__all__ = (
    "CacheManga",
    "FetchManga",
    "FetchPool",
    "UpdatePool",
)


class FetchManga(Command):
    manga_id: IDType


class FetchMangaUsingPool(Command):
    pool_id: IDType


class CacheManga(Command):
    manga_id: IDType


class FetchPool(Command):
    language: str
    offset: int = 0
    limit: int = 0


class UpdatePool(Command):
    pool_id: IDType
