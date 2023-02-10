import abc
from collections.abc import Callable
from typing import ClassVar, Generic, TypeVar

from kyrie.interfaces import Repository
from kyrie.models import View
from sqlalchemy import select
from sqlalchemy.ext import asyncio as aiosqlalchemy

from hanako.infrastructure.orm import BaseOrm, MangaOrm, PoolOrm
from hanako.query import MangaView, PoolView

Obj = TypeVar("Obj", bound=View)
ObjType = type[Obj]
Orm = TypeVar("Orm", bound=BaseOrm)
OrmType = type[Orm]


class SqliteRepository(Repository[Obj], Generic[Obj, Orm]):
    __obj_type__: ClassVar[type[Obj]]  # type: ignore
    __orm_type__: ClassVar[type[Orm]]  # type: ignore

    _session_factory: Callable[..., aiosqlalchemy.AsyncSession]

    def __init__(
        self, session_factory: Callable[..., aiosqlalchemy.AsyncSession]
    ) -> None:
        self._session_factory = session_factory

    @abc.abstractmethod
    def orm_to_obj(self, orm: Orm) -> Obj:
        ...

    async def find(self, offset: int, limit: int, **filters: object) -> tuple[Obj, ...]:
        stmt = select(self.__orm_type__)
        stmt = stmt.filter_by(**filters)
        stmt = stmt.limit(limit).offset(offset)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
        return tuple(self.__obj_type__.from_orm(orm) for orm in result.scalars().all())

    async def find_one(self, **filters: object) -> Obj | None:
        stmt = select(self.__orm_type__)
        stmt = stmt.filter_by(**filters)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            orm = result.scalar()

        if orm is None:
            return None
        return self.orm_to_obj(orm)


class SqliteMangaRepository(SqliteRepository[MangaView, MangaOrm]):
    __obj_type__ = MangaView
    __orm_type__ = MangaOrm

    def orm_to_obj(self, orm: MangaOrm) -> MangaView:
        return MangaView(
            id=orm.id,
            title=orm.title,
        )


class SqlitePoolRepository(SqliteRepository[PoolView, PoolOrm]):
    __obj_type__ = PoolView
    __orm_type__ = PoolOrm

    def orm_to_obj(self, orm: PoolOrm) -> PoolView:
        return PoolView(
            id=orm.id,
            manga_ids=orm.manga_ids,
        )
