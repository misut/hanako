import asyncio
from collections.abc import Callable
from struct import unpack
from typing import Literal, cast

import httpx
import js2py
from kyrie.models import IDType

from hanako.command import HitomiService
from hanako.domain import HitomiGallery, HitomiPage
from hanako.infrastructure.gg import GG


def generate_download_url(page: HitomiPage, gg: GG) -> str:
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
    route = determine_route(page, gg)
    subdomain = determine_subdomain(page, gg)
    return f"https://{subdomain}a.hitomi.la/{extension}/{route}/{filename}.{extension}"


class HttpHitomiService(HitomiService):
    _client_factory: Callable[..., httpx.AsyncClient]
    _gg: GG

    def __init__(
        self, client_factory: Callable[..., httpx.AsyncClient], gg: GG
    ) -> None:
        self._client_factory = client_factory
        self._gg = gg

    async def fetch_gallery_ids(
        self, language: str, offset: int, limit: int
    ) -> list[IDType]:  # pragma: no cover
        url = f"https://ltn.hitomi.la/index-{language}.nozomi"
        headers = {"origin": "https://hitomi.la"}
        if limit > 0:
            byte_beg = offset * 4
            byte_end = byte_beg + limit * 4 - 1
            headers["Range"] = f"bytes={byte_beg}-{byte_end}"

        async with self._client_factory() as client:
            response = await client.get(url=url, headers=headers)

        gallery_ids = response.content
        total_bytes = len(gallery_ids) // 4
        return [cast(IDType, id) for id in unpack(f">{total_bytes}i", gallery_ids)]

    async def fetch_gallery(self, gallery_id: IDType) -> HitomiGallery:
        url = f"https://ltn.hitomi.la/galleries/{gallery_id}.js"

        async with self._client_factory() as client:
            response = await client.get(url=url)

        return HitomiGallery(**js2py.eval_js(response.text).to_dict())

    async def download_page(
        self, gallery_id: IDType, page: HitomiPage
    ) -> bytes:  # pragma: no cover
        url = generate_download_url(page, self._gg)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": f"https://hitomi.la/reader/{gallery_id}.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        }

        async with self._client_factory() as client:
            response = await client.get(url=url, headers=headers)

        return response.content

    async def download_gallery(
        self, gallery: HitomiGallery
    ) -> list[bytes]:  # pragma: no cover
        tasks = [
            asyncio.create_task(self.download_page(gallery.id, page))
            for page in gallery.pages
        ]
        return [await task for task in tasks]
