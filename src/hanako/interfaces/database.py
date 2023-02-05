import abc
from typing import Generic, TypeVar

from hanako.monads import Option

T = TypeVar("T")


class Repository(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def find(self, offset: int, limit: int, **filters: object) -> tuple[T, ...]:
        ...

    @abc.abstractmethod
    def find_one(self, **filters: object) -> Option[T]:
        ...


class Storage(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def save(self, *entities: T) -> None:
        ...

    @abc.abstractmethod
    def save_one(self, entity: T) -> None:
        ...
