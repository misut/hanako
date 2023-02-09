import abc
from collections.abc import Callable
from typing import Generic, TypeVar

from kyrie.models import Entity
from kyrie.interfaces import Storage
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext import asyncio as aiosqlalchemyorm

from hanako.domain import Manga, Pool
from hanako.infrastructure.orm import BaseOrm, MangaOrm, PoolOrm

Obj = TypeVar("Obj", bound=Entity)
Orm = TypeVar("Orm", bound=BaseOrm)


class SqliteStorage(Storage[Obj], Generic[Obj, Orm]):
    _session_factory: Callable[..., aiosqlalchemyorm.AsyncSession]

    def __init__(
        self, session_factory: Callable[..., aiosqlalchemyorm.AsyncSession]
    ) -> None:
        self._session_factory = session_factory

    @property
    @abc.abstractmethod
    def orm(self) -> type[Orm]:
        ...

    async def save(self, *entities: Obj) -> None:
        stmt = insert(self.orm)
        stmt = stmt.values([entity.dict() for entity in entities])
        stmt = stmt.on_conflict_do_update(
            index_elements=[getattr(self.orm, "id")],
            set_={k: v for k, v in stmt.excluded.items() if k != "id"},
        )

        async with self._session_factory() as session:
            await session.execute(stmt)

    async def save_one(self, entity: Obj) -> None:
        stmt = select(self.orm)
        stmt = stmt.filter_by(id=entity.id)

        async with self._session_factory() as session:
            result = await session.execute(stmt)
            orm = result.scalar()
            if orm is None:
                orm = self.orm()
                setattr(orm, "id", entity.id)
                session.add(orm)

            for k, v in entity.dict(exclude={"id"}).items():
                setattr(orm, k, v)
            await session.commit()


class SqliteMangaStorage(SqliteStorage[Manga, MangaOrm]):
    @property
    def orm(self) -> type[MangaOrm]:
        return MangaOrm


class SqlitePoolStorage(SqliteStorage[Pool, PoolOrm]):
    @property
    def orm(self) -> type[PoolOrm]:
        return PoolOrm
