import abc
from collections.abc import Sequence

from kyrie.monads import Result

from hanako import domain
from hanako.command.exceptions import ReadError, WriteError


class MangaCache(abc.ABC):
    @abc.abstractmethod
    async def read(self, manga: domain.Manga) -> Result[list[bytes], ReadError]:
        ...

    @abc.abstractmethod
    async def write_one(
        self, manga: domain.Manga, page_file: bytes, page_number: int
    ) -> Result[str, WriteError]:
        ...

    @abc.abstractmethod
    async def write(
        self, manga: domain.Manga, page_files: Sequence[bytes]
    ) -> Result[list[str], WriteError]:
        ...
