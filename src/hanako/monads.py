from collections.abc import Callable
from typing import Any, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Option(Generic[T]):
    _value: T | None

    def __init__(self, value: T | None) -> None:
        self._value = value

    def __bool__(self) -> bool:
        return self._value is not None

    def expect(self, error_message: str) -> T:
        if self._value is None:
            raise ValueError(error_message)
        return self._value

    def unwrap(self) -> T:
        if self._value is None:
            raise ValueError()
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value or default

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self._value or func()

    def map(self, func: Callable[[T], U]) -> "Option[U]":
        return Option[U](None) if self._value is None else Option[U](func(self._value))

    def map_or(self, func: Callable[[T], U], default: U) -> U:
        return default if self._value is None else func(self._value)

    def map_or_else(self, func: Callable[[T], U], default: Callable[[], U]) -> U:
        return default() if self._value is None else func(self._value)

    def filter(self, predicate: Callable[[T], bool]) -> "Option[T]":
        if self._value is not None and predicate(self._value):
            return self

        return Option[T](None)

    def flatten(self) -> "Option[T]":
        value = getattr(self._value, "_value", None)
        return Option[T](None) if value is None else Option[T](value)

    def __eq__(self, other: object) -> bool:
        return self._value == other

    def __ne__(self, other: object) -> bool:
        return self._value != other

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return "None" if self._value is None else f"Some({self._value})"


SOME = Option
NONE = Option[Any](None)
