from collections.abc import Iterator, Mapping
from typing import TypeVar

__all__ = ("FrozenDict",)

K = TypeVar("K")
V = TypeVar("V")


class FrozenDict(Mapping[K, V]):
    _map: dict[K, V]

    def __init__(self, *args, **kwargs) -> None:
        self._map = dict(*args, **kwargs)

    def __getitem__(self, key: K) -> V:
        return self._map[key]

    def __contains__(self, key: object) -> bool:
        return key in self._map

    def __iter__(self) -> Iterator[K]:
        return iter(self._map)

    def __len__(self) -> int:
        return len(self._map)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._map}>"
