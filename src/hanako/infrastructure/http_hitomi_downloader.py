import asyncio
from collections.abc import Callable

import httpx
from kyrie.models import IDType

from hanako import domain
from hanako.command import HitomiDownloader


def _create_headers(manga_id: IDType) -> dict[str, str]:
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": f"https://hitomi.la/reader/{manga_id}.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }


class HttpHitomiDownloader(HitomiDownloader):
    _client_factory: Callable[..., httpx.AsyncClient]

    def __init__(self, client_factory: Callable[..., httpx.AsyncClient]) -> None:
        self._client_factory = client_factory

    async def download_page(
        self, manga: domain.Manga, page_number: int
    ) -> bytes:  # pragma: no cover
        async with self._client_factory() as client:
            response = await client.get(
                url=manga.pages[page_number].url,
                headers=_create_headers(manga.id),
            )
            response.raise_for_status()

        return response.content

    async def download_pages(
        self, manga: domain.Manga
    ) -> list[bytes]:  # pragma: no cover
        tasks = [
            asyncio.create_task(self.download_page(manga, page_number))
            for page_number in range(len(manga.pages))
        ]
        return [await task for task in tasks]
