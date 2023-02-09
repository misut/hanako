import abc
from collections.abc import Callable
from typing import Generic, TypeVar

from kyrie.interfaces import Repository
from kyrie.models import View
from kyrie.monads import Option
from sqlalchemy import select
from sqlalchemy.ext import asyncio as aiosqlalchemy

from hanako.infrastructure.orm import BaseOrm, MangaOrm, PoolOrm
from hanako.query import MangaView, PoolView

Obj = TypeVar("Obj", bound=View)
Orm = TypeVar("Orm", bound=BaseOrm)


class SqliteRepository(Repository[Obj], Generic[Obj, Orm]):
    _session_factory: Callable[..., aiosqlalchemy.AsyncSession]

    def __init__(
        self, session_factory: Callable[..., aiosqlalchemy.AsyncSession]
    ) -> None:
        self._session_factory = session_factory

    @property
    @abc.abstractmethod
    def obj(self) -> type[Obj]:
        ...

    @property
    @abc.abstractmethod
    def orm(self) -> type[Orm]:
        ...

    @abc.abstractmethod
    def orm_to_obj(self, orm: Orm) -> Obj:
        ...

    async def find(self, offset: int, limit: int, **filters: object) -> tuple[Obj, ...]:
        stmt = select(self.orm)
        stmt = stmt.filter_by(**filters)
        stmt = stmt.limit(limit).offset(offset)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
        return tuple(self.obj.from_orm(orm) for orm in result.scalars().all())

    async def find_one(self, **filters: object) -> Option[Obj]:
        stmt = select(self.orm)
        stmt = stmt.filter_by(**filters)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            orm = result.scalar()

        if orm is None:
            return Option[Obj](None)
        return Option[Obj](self.orm_to_obj(orm))


class SqliteMangaRepository(SqliteRepository[MangaView, MangaOrm]):
    @property
    def obj(self) -> type[MangaView]:
        return MangaView

    @property
    def orm(self) -> type[MangaOrm]:
        return MangaOrm

    def orm_to_obj(self, orm: MangaOrm) -> MangaView:
        return MangaView(
            id=orm.id,
            title=orm.title,
        )


class SqlitePoolRepository(SqliteRepository[PoolView, PoolOrm]):
    @property
    def obj(self) -> type[PoolView]:
        return PoolView

    @property
    def orm(self) -> type[PoolOrm]:
        return PoolOrm

    def orm_to_obj(self, orm: PoolOrm) -> PoolView:
        return PoolView(
            id=orm.id,
            manga_ids=orm.manga_ids,
        )
