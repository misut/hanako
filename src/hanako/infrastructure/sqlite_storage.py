from collections.abc import Callable
from typing import ClassVar, Generic, TypeVar

from kyrie.interfaces import Storage
from kyrie.models import Entity
from kyrie.monads import Null, Option, Some
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext import asyncio as aiosqlalchemyorm

from hanako import domain
from hanako.infrastructure.orm import BaseOrm, MangaOrm, PoolEntryOrm

Obj = TypeVar("Obj", bound=Entity)
Orm = TypeVar("Orm", bound=BaseOrm)


class SqliteStorage(Storage[Obj], Generic[Obj, Orm]):
    __obj_type__: ClassVar[type[Obj]]  # type: ignore
    __orm_type__: ClassVar[type[Orm]]  # type: ignore
    __primary_key__: ClassVar[str]

    _session_factory: Callable[..., aiosqlalchemyorm.AsyncSession]

    def __init__(
        self, session_factory: Callable[..., aiosqlalchemyorm.AsyncSession]
    ) -> None:
        self._session_factory = session_factory

    async def find_one(self, **filters: object) -> Option[Obj]:
        stmt = select(self.__orm_type__)
        stmt = stmt.filter_by(**filters)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            orm = result.scalar()

        if orm is None:
            return Null
        return Some(self.__obj_type__.from_orm(orm))

    async def save(self, *entities: Obj) -> None:
        if len(entities) == 0:
            return

        stmt = insert(self.__orm_type__)
        stmt = stmt.values([entity.dict() for entity in entities])
        stmt = stmt.on_conflict_do_update(
            index_elements=[getattr(self.__orm_type__, self.__primary_key__)],
            set_={k: v for k, v in stmt.excluded.items() if k != self.__primary_key__},
        )

        async with self._session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    async def save_one(self, entity: Obj) -> None:
        stmt = select(self.__orm_type__)
        stmt = stmt.filter_by(id=getattr(entity, self.__primary_key__))

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            orm = result.scalar()
            if orm is None:
                orm = self.__orm_type__()
                setattr(orm, "id", getattr(entity, self.__primary_key__))
                session.add(orm)

            for k, v in entity.dict(exclude={self.__primary_key__}).items():
                setattr(orm, k, v)
            await session.commit()


class SqliteMangaStorage(SqliteStorage[domain.Manga, MangaOrm]):
    __obj_type__ = domain.Manga
    __orm_type__ = MangaOrm
    __primary_key__ = "id"


class SqlitePoolEntryStorage(SqliteStorage[domain.PoolEntry, PoolEntryOrm]):
    __obj_type__ = domain.PoolEntry
    __orm_type__ = PoolEntryOrm
    __primary_key__ = "manga_id"
