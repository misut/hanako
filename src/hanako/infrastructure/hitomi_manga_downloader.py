import asyncio
from collections.abc import Callable

import httpx
from kyrie.monads import Err, Ok, Result

from hanako import domain
from hanako.command import DownloadError, MangaDownloader
from hanako.infrastructure.hitomi import create_image_headers


class HitomiMangaDownloader(MangaDownloader):
    _client_factory: Callable[..., httpx.AsyncClient]

    def __init__(self, client_factory: Callable[..., httpx.AsyncClient]) -> None:
        self._client_factory = client_factory

    async def __get_response(
        self, client: httpx.AsyncClient, url: str, headers: dict[str, str]
    ) -> httpx.Response:
        response = await client.get(url=url, headers=headers)
        return response

    async def download_page(
        self, manga: domain.Manga, page_number: int
    ) -> Result[bytes, DownloadError]:
        async with self._client_factory() as client:
            response = await self.__get_response(
                client, manga.pages[page_number].url, create_image_headers(manga.id)
            )

        result: Result[bytes, DownloadError]
        try:
            response.raise_for_status()
            result = Ok(response.content)
        except httpx.HTTPError as err:
            result = Err(DownloadError(err))
        finally:
            return result

    async def download_manga(
        self, manga: domain.Manga
    ) -> Result[list[bytes], DownloadError]:
        headers = create_image_headers(manga.id)
        async with self._client_factory() as client:
            tasks = [
                asyncio.create_task(self.__get_response(client, page.url, headers))
                for page in manga.pages
            ]
            responses = [await task for task in tasks]

        page_files: list[bytes] = []
        for response in responses:
            try:
                response.raise_for_status()
                page_files.append(response.content)
            except httpx.HTTPError as err:
                return Err(DownloadError(err))

        return Ok(page_files)
