from collections.abc import Callable

from kyrie.monads import Option
from sqlalchemy import orm as sqlalchemyorm

from hanako.infrastructure.orm import MangaOrm
from hanako.query import MangaRepository, MangaView


class SqlMangaRepository(MangaRepository):
    _session_factory: Callable[..., sqlalchemyorm.Session]

    def __init__(self, session_factory: Callable[..., sqlalchemyorm.Session]) -> None:
        self._session_factory = session_factory

    def find(self, offset: int, limit: int, **filters: object) -> tuple[MangaView, ...]:
        with self._session_factory() as session:
            query = session.query(MangaOrm)
            query = query.filter_by(**filters)
            query = query.limit(limit).offset(offset)
        return tuple(MangaView.from_orm(orm) for orm in query)

    def find_one(self, **filters: object) -> Option[MangaView]:
        with self._session_factory() as session:
            query = session.query(MangaOrm)
            query = query.filter_by(**filters)
            orm = query.first()
            if orm is None:
                return Option[MangaView](None)
            return Option[MangaView](
                MangaView(
                    id=orm.id,
                    title=orm.title,
                )
            )
