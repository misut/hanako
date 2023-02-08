from collections.abc import Callable

from sqlalchemy import orm as sqlalchemyorm

from hanako.command import MangaStorage
from hanako.domain import Manga


class SqlMangaStorage(MangaStorage):
    _session_factory: Callable[..., sqlalchemyorm.Session]

    def __init__(self, session_factory: Callable[..., sqlalchemyorm.Session]) -> None:
        self._session_factory = session_factory

    def save(self, *entities: Manga) -> None:
        return super().save(*entities)

    def save_one(self, entity: Manga) -> None:
        return super().save_one(entity)
