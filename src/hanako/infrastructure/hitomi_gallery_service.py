import asyncio
import base64
from collections.abc import Callable
from struct import unpack
from typing import Literal, cast

import httpx
import js2py
from kyrie.models import IDType
from kyrie.monads import Err, Ok, Result

from hanako import domain
from hanako.command import FetchError, GalleryService
from hanako.infrastructure.hitomi import (
    GG,
    HitomiGallery,
    HitomiPage,
    create_image_headers,
    create_thumbnail_url,
)


class HitomiGalleryService(GalleryService):
    _client_factory: Callable[..., httpx.AsyncClient]
    _gg: GG

    def __init__(
        self, client_factory: Callable[..., httpx.AsyncClient], gg: GG
    ) -> None:
        self._client_factory = client_factory
        self._gg = gg

    def __generate_page_url(self, page: HitomiPage) -> str:
        def determine_extension(page: HitomiPage) -> Literal["avif", "webp"]:
            if page.hasavif:
                return "avif"
            if page.haswebp:
                return "webp"
            raise ValueError(f"No supported extensions: {page.filename}")

        def determine_filename(page: HitomiPage) -> str:
            if page.hash == "":
                return page.filename
            return page.hash

        def determine_route(page: HitomiPage, gg: GG) -> str:
            g = page.hash[-3:]
            return f"{gg.b}{gg.s(g)}"

        def determine_subdomain(page: HitomiPage, gg: GG) -> str:
            g = page.hash[-3:]
            return chr(97 + gg.m(int(gg.s(g))))

        extension = determine_extension(page)
        filename = determine_filename(page)
        route = determine_route(page, self._gg)
        subdomain = determine_subdomain(page, self._gg)
        return (
            f"https://{subdomain}a.hitomi.la/{extension}/{route}/{filename}.{extension}"
        )

    async def __get_response(
        self, client: httpx.AsyncClient, url: str, headers: dict[str, str]
    ) -> httpx.Response:
        response = await client.get(url=url, headers=headers)
        return response

    async def fetch_galleries(
        self, *gallery_ids: IDType
    ) -> list[Result[domain.Gallery, FetchError]]:
        url = "https://ltn.hitomi.la/galleries/{}.js"
        async with self._client_factory() as client:
            tasks = [
                asyncio.create_task(
                    self.__get_response(client, url.format(gallery_id), {})
                )
                for gallery_id in gallery_ids
            ]
            responses = [await task for task in tasks]

        galleries: list[Result[HitomiGallery, FetchError]] = []
        for response in responses:
            gallery: Result[HitomiGallery, FetchError]
            try:
                response.raise_for_status()
                gallery = Ok(HitomiGallery(**js2py.eval_js(response.text).to_dict()))
            except httpx.HTTPError as err:
                gallery = Err(FetchError(err))
            finally:
                galleries.append(gallery)

        async with self._client_factory() as client:
            tasks = [
                asyncio.create_task(
                    self.__get_response(
                        client,
                        create_thumbnail_url(gallery.unwrap().pages[0].hash),
                        create_image_headers(gallery.unwrap().id),
                    )
                )
                for gallery in galleries
                if gallery.is_ok()
            ]
            responses = [await task for task in tasks]

        thumbnails: list[Result[str, FetchError]] = []
        for response in responses:
            thumbnail: Result[str, FetchError]
            try:
                response.raise_for_status()
                thumbnail = Ok(base64.b64encode(response.content).decode("ascii"))
            except httpx.HTTPError as err:
                thumbnail = Err(FetchError(err))
            finally:
                thumbnails.append(thumbnail)

        results: list[Result[domain.Gallery, FetchError]] = []
        for gallery, thumbnail in zip(galleries, thumbnails):
            if gallery.is_err():
                results.append(Err(gallery.unwrap_err()))
                continue
            if thumbnail.is_err():
                results.append(Err(thumbnail.unwrap_err()))
                continue

            g, t = gallery.unwrap(), thumbnail.unwrap()
            results.append(
                Ok(
                    domain.Gallery(
                        id=g.id,
                        title=g.title,
                        thumbnail=t,
                        artists=[domain.GalleryArtist(name=a.name) for a in g.artists],
                        pages=[
                            domain.GalleryPage(
                                filename=p.filename,
                                url=self.__generate_page_url(p),
                            )
                            for p in g.pages
                        ],
                        tags=[domain.GalleryTag(tag=t.tag) for t in g.tags],
                    )
                )
            )

        return results

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
