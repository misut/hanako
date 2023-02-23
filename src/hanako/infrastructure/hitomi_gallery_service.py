import asyncio
import base64
from collections.abc import Callable
from struct import unpack
from typing import cast

import httpx
import js2py
from kyrie.models import IDType
from kyrie.monads import Err, Ok, Result
from tenacity import *

from hanako import domain
from hanako.command import FetchError, GalleryService
from hanako.infrastructure.hitomi import (
    DEFAULT_HITOMI_BATCH_SIZE,
    HitomiGallery,
    create_image_headers,
    create_thumbnail_url,
)


def is_false(response: httpx.Response) -> bool:
    return response.status_code == 503


def return_last_response(_: RetryCallState) -> httpx.Response:
    return httpx.Response(503)


class HitomiGalleryService(GalleryService):
    _client_factory: Callable[..., httpx.AsyncClient]
    _semaphore: asyncio.Semaphore

    def __init__(
        self,
        client_factory: Callable[..., httpx.AsyncClient],
        batch_size: int = DEFAULT_HITOMI_BATCH_SIZE,
    ) -> None:
        self._client_factory = client_factory
        self._semaphore = asyncio.Semaphore(batch_size)

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

    async def fetch_galleries(
        self, *gallery_ids: IDType
    ) -> Result[list[domain.Gallery], FetchError]:
        url = "https://ltn.hitomi.la/galleries/{}.js"
        async with self._client_factory() as client:
            tasks = [
                asyncio.create_task(
                    self.__get_response(client, url.format(gallery_id), {})
                )
                for gallery_id in gallery_ids
            ]
            responses = [await task for task in tasks]

        galleries: list[HitomiGallery] = []
        for response in responses:
            try:
                response.raise_for_status()
                galleries.append(
                    HitomiGallery(**js2py.eval_js(response.text).to_dict())
                )
            except httpx.HTTPError as err:
                return Err(FetchError(err))

        async with self._client_factory() as client:
            tasks = [
                asyncio.create_task(
                    self.__get_response(
                        client,
                        create_thumbnail_url(gallery.pages[0].hash),
                        create_image_headers(gallery.id),
                    )
                )
                for gallery in galleries
            ]
            responses = [await task for task in tasks]

        thumbnails: list[str] = []
        for response in responses:
            try:
                response.raise_for_status()
                thumbnails.append(base64.b64encode(response.content).decode("ascii"))
            except httpx.HTTPError as err:
                return Err(FetchError(err))

        return Ok(
            [
                domain.Gallery(
                    id=gallery.id,
                    title=gallery.title,
                    thumbnail=thumbnail,
                    artists=[domain.GalleryArtist(**a.dict()) for a in gallery.artists],
                    pages=[domain.GalleryPage(**p.dict()) for p in gallery.pages],
                    tags=[domain.GalleryTag(**t.dict()) for t in gallery.tags],
                )
                for gallery, thumbnail in zip(galleries, thumbnails)
            ]
        )

    async def fetch_pool(
        self, language: str, offset: int, limit: int
    ) -> Result[domain.GalleryPool, FetchError]:
        url = f"https://ltn.hitomi.la/index-{language}.nozomi"
        headers = {"origin": "https://hitomi.la"}
        if limit > 0:
            byte_beg = offset * 4
            byte_end = byte_beg + limit * 4 - 1
            headers["Range"] = f"bytes={byte_beg}-{byte_end}"

        async with self._client_factory() as client:
            response = await client.get(url=url, headers=headers)

        result: Result[domain.GalleryPool, FetchError]
        try:
            response.raise_for_status()
            gallery_ids = response.content
            total_bytes = len(gallery_ids) // 4
            result = Ok(
                domain.GalleryPool(
                    id_list=[
                        cast(IDType, id)
                        for id in unpack(f">{total_bytes}i", gallery_ids)
                    ],
                    language=language,
                    offset=offset,
                    limit=limit,
                )
            )
        except httpx.HTTPError as err:
            result = Err(FetchError(err))

        return result
