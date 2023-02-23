import asyncio
from collections.abc import Callable
from typing import Literal

import httpx
from kyrie.monads import Err, Ok, Result
from tenacity import *

from hanako import domain
from hanako.command import DownloadError, MangaDownloader
from hanako.infrastructure.hitomi import (
    DEFAULT_HITOMI_BATCH_SIZE,
    GG,
    create_image_headers,
)


def is_false(response: httpx.Response) -> bool:
    return response.status_code == 503


def return_last_response(retry_state: RetryCallState) -> httpx.Response:
    return retry_state.outcome.result() if retry_state.outcome else httpx.Response(503)


class HitomiMangaDownloader(MangaDownloader):
    _client_factory: Callable[..., httpx.AsyncClient]
    _gg: GG
    _semaphore: asyncio.Semaphore

    def __init__(
        self,
        client_factory: Callable[..., httpx.AsyncClient],
        gg: GG,
        batch_size: int = DEFAULT_HITOMI_BATCH_SIZE,
    ) -> None:
        self._client_factory = client_factory
        self._gg = gg
        self._semaphore = asyncio.Semaphore(batch_size)

    def __generate_page_url(self, page: domain.MangaPage) -> str:
        def determine_extension(page: domain.MangaPage) -> Literal["avif", "webp"]:
            if page.hasavif:
                return "avif"
            if page.haswebp:
                return "webp"
            raise ValueError(f"No supported extensions: {page.filename}")

        def determine_filename(page: domain.MangaPage) -> str:
            if page.hash == "":
                return page.filename
            return page.hash

        def determine_route(page: domain.MangaPage, gg: GG) -> str:
            g = page.hash[-3:]
            return f"{gg.b}{gg.s(g)}"

        def determine_subdomain(page: domain.MangaPage, gg: GG) -> str:
            g = page.hash[-3:]
            return chr(97 + gg.m(int(gg.s(g))))

        extension = determine_extension(page)
        filename = determine_filename(page)
        route = determine_route(page, self._gg)
        subdomain = determine_subdomain(page, self._gg)
        return (
            f"https://{subdomain}a.hitomi.la/{extension}/{route}/{filename}.{extension}"
        )

    @retry(
        stop=stop_after_delay(60),
        wait=wait_fixed(1),
        retry=retry_if_result(is_false),
        retry_error_callback=return_last_response,
        sleep=asyncio.sleep,  # type: ignore
    )
    async def __get_response(
        self, client: httpx.AsyncClient, url: str, headers: dict[str, str]
    ) -> httpx.Response:
        async with self._semaphore:
            response = await client.get(url=url, headers=headers)
        return response

    async def download_page(
        self, manga: domain.Manga, page_number: int
    ) -> Result[bytes, DownloadError]:
        url = self.__generate_page_url(manga.pages[page_number])
        headers = create_image_headers(manga.id)
        async with self._client_factory() as client:
            response = await self.__get_response(client, url, headers)

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
                asyncio.create_task(
                    self.__get_response(client, self.__generate_page_url(page), headers)
                )
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
