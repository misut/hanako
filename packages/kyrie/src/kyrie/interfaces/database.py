import abc
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(abc.ABC, Generic[T]):
    @abc.abstractmethod
    async def find(self, offset: int, limit: int, **filters: object) -> tuple[T, ...]:
        ...

    @abc.abstractmethod
    async def find_one(self, **filters: object) -> T | None:
        ...


class Storage(abc.ABC, Generic[T]):
    @abc.abstractmethod
    async def save(self, *entities: T) -> None:
        ...

    @abc.abstractmethod
    async def save_one(self, entity: T) -> None:
        ...
