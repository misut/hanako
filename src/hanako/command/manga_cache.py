import abc
from collections.abc import Sequence

from hanako import domain


class MangaCache(abc.ABC):
    @abc.abstractmethod
    async def read(self, manga: domain.Manga) -> list[bytes]:
        ...

    @abc.abstractmethod
    async def write(self, manga: domain.Manga, page_files: Sequence[bytes]) -> str:
        ...
