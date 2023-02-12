import base64
from collections.abc import Callable
from struct import unpack
from typing import Literal, cast

import httpx
import js2py
from kyrie.models import IDType

from hanako.command import HitomiFetcher
from hanako.domain import HitomiGallery, HitomiPage
from hanako.infrastructure.gg import GG


def _create_headers(gallery_id: IDType) -> dict[str, str]:
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": f"https://hitomi.la/reader/{gallery_id}.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }


def _create_thumbnail_url(hash: str) -> str:
    return f"https://btn.hitomi.la/avifsmallbigtn/{hash[-1]}/{hash[-3:-1]}/{hash}.avif"


class HttpHitomiFetcher(HitomiFetcher):
    _client_factory: Callable[..., httpx.AsyncClient]
    _gg: GG

    def __init__(
        self, client_factory: Callable[..., httpx.AsyncClient], gg: GG
    ) -> None:
        self._client_factory = client_factory
        self._gg = gg

    async def fetch_gallery_ids(
        self, language: str, offset: int, limit: int
    ) -> list[IDType]:
        url = f"https://ltn.hitomi.la/index-{language}.nozomi"
        headers = {"origin": "https://hitomi.la"}
        if limit > 0:
            byte_beg = offset * 4
            byte_end = byte_beg + limit * 4 - 1
            headers["Range"] = f"bytes={byte_beg}-{byte_end}"

        async with self._client_factory() as client:
            response = await client.get(url=url, headers=headers)
            response.raise_for_status()

        gallery_ids = response.content
        total_bytes = len(gallery_ids) // 4
        return [cast(IDType, id) for id in unpack(f">{total_bytes}i", gallery_ids)]

    async def fetch_gallery(self, gallery_id: IDType) -> HitomiGallery:
        url = f"https://ltn.hitomi.la/galleries/{gallery_id}.js"

        async with self._client_factory() as client:
            response = await client.get(url=url)
            response.raise_for_status()

        return HitomiGallery(**js2py.eval_js(response.text).to_dict())

    async def fetch_thumbnail(self, gallery: HitomiGallery) -> str:
        async with self._client_factory() as client:
            response = await client.get(
                url=_create_thumbnail_url(gallery.pages[0].hash),
                headers=_create_headers(gallery.id),
            )
            response.raise_for_status()

        return base64.b64encode(response.content).decode("ascii")

    def generate_page_url(self, page: HitomiPage) -> str:
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
