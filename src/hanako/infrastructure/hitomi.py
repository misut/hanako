from struct import unpack
from typing import Literal, cast

import httpx
import js2py
from kyrie.models import IDType

from hanako.command import MangaService
from hanako.domain import HitomiGallery, HitomiPage


async def generate_download_url(page: HitomiPage) -> str:
    response = httpx.get(url="https://ltn.hitomi.la/gg.js")
    gg = js2py.eval_js(response.text)

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

    def determine_route(page: HitomiPage, gg: js2py.base.JsObjectWrapper) -> str:
        g = page.hash[-3:]

        return f"{gg.b}{gg.s(g)}"

    def determine_subdomain(page: HitomiPage, gg: js2py.base.JsObjectWrapper) -> str:
        g = page.hash[-3:]

        return chr(97 + gg.m(int(gg.s(g))))

    extension = determine_extension(page)
    filename = determine_filename(page)
    route = determine_route(page, gg)
    subdomain = determine_subdomain(page, gg)

    return f"https://{subdomain}a.hitomi.la/{extension}/{route}/{filename}.{extension}"


class Hitomi(MangaService):
    async def fetch_ids(self, offset: int = 0, limit: int = 0) -> list[IDType]:
        headers = {"origin": "https://hitomi.la"}
        if limit > 0:
            byte_beg = offset * 4
            byte_end = byte_beg + limit * 4 - 1
            headers["Range"] = f"bytes={byte_beg}-{byte_end}"

        url = "https://ltn.hitomi.la/index-all.nozomi"
        response = httpx.get(
            url=url,
            timeout=3,
            headers=headers,
        )

        res = response.content
        ttl_bytes = len(res) // 4
        return [cast(IDType, id) for id in unpack(f">{ttl_bytes}i", res)]

    async def fetch_gallery(self, gallery_id: IDType) -> HitomiGallery:
        url = f"https://ltn.hitomi.la/galleries/{gallery_id}.js"
        response = httpx.get(url=url)
        return HitomiGallery(**js2py.eval_js(response.text).to_dict())

    async def download_page(self, gallery_id: IDType, page: HitomiPage) -> None:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": f"https://hitomi.la/reader/{gallery_id}.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        }
        url = await generate_download_url(page)
        httpx.get(
            url=url,
            headers=headers,
            timeout=3,
        )

    async def download_gallery(self, gallery: HitomiGallery) -> None:
        for page in gallery.pages:
            await self.download_page(gallery.id, page)
