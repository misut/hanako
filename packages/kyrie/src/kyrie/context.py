from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

__all__ = (
    "Context",
    "Provider",
)

T = TypeVar("T")


@dataclass(frozen=True)
class Context:
    ...


class Provider(Generic[T]):
    _provider: type[T]
    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]

    def __init__(self, provider: type[T], *args: Any, **kwargs: Any) -> None:
        self._provider = provider
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        return self.provide(*args, **kwargs)

    def provide(self, *args: Any, **kwargs: Any) -> T:
        kwargs.update(self._kwargs)
        return self._provider(*args, *self._args, **kwargs)
