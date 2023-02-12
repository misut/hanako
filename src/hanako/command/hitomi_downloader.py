import abc

from hanako import domain


class HitomiDownloader(abc.ABC):
    @abc.abstractmethod
    async def download_page(self, manga: domain.Manga, page_number: int) -> bytes:
        ...

    @abc.abstractmethod
    async def download_pages(self, manga: domain.Manga) -> list[bytes]:
        ...
