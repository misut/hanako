import abc

from kyrie.monads import Result

from hanako import domain
from hanako.command.exceptions import DownloadError


class MangaDownloader(abc.ABC):
    @abc.abstractmethod
    async def download_page(
        self, manga: domain.Manga, page_number: int
    ) -> Result[bytes, DownloadError]:
        ...

    @abc.abstractmethod
    async def download_manga(
        self, manga: domain.Manga
    ) -> Result[list[bytes], DownloadError]:
        ...
