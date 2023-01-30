import asyncio
from typing import cast, Literal
from struct import unpack

import js2py
from kivy.network.urlrequest import UrlRequest
from loguru import logger

from hanako.interfaces import Manga, MangaPage, MangaService
from hanako.models import IDType


def log_on_success(*_) -> None:
    logger.info("Succeeded.")


async def generate_download_url(page: MangaPage) -> str:
    req = UrlRequest(url="https://ltn.hitomi.la/gg.js")
    await asyncio.to_thread(req.wait)
    gg = js2py.eval_js(req.result)

    def determine_extension(page: MangaPage) -> Literal["avif", "webp"]:
        if page.hasavif:
            return "avif"
        if page.haswebp:
            return "webp"

        raise ValueError(f"No supported extensions: {page.filename}")

    def determine_filename(page: MangaPage) -> str:
        if page.hash == "":
            return page.filename

        return page.hash

    def determine_route(page: MangaPage, gg: js2py.base.JsObjectWrapper) -> str:
        g = page.hash[-3:]

        return f"{gg.b}{gg.s(g)}"

    def determine_subdomain(page: MangaPage, gg: js2py.base.JsObjectWrapper) -> str:
        g = page.hash[-3:]

        return chr(97 + gg.m(int(gg.s(g))))

    extension = determine_extension(page)
    filename = determine_filename(page)
    route = determine_route(page, gg)
    subdomain = determine_subdomain(page, gg)

    return f"https://{subdomain}a.hitomi.la/{extension}/{route}/{filename}.{extension}"


class Hitomi(MangaService):
    async def fetch_ids(self, offset: int, limit: int) -> list[IDType]:
        byte_beg = offset * 4
        byte_end = byte_beg + limit * 4 - 1
        headers = {
            "origin": "https://hitomi.la",
            "Range": f"bytes={byte_beg}-{byte_end}",
        }
        url = "https://ltn.hitomi.la/index-all.nozomi"

        req = UrlRequest(
            url=url,
            decode=False,
            timeout=3,
            method="GET",
            on_success=log_on_success,
            req_headers=headers,
        )
        await asyncio.to_thread(req.wait)

        res = bytes(req.result, "utf-8")
        ttl_bytes = len(res) // 4
        return [cast(IDType, id) for id in unpack(f">{ttl_bytes}i", res)]

    async def fetch_manga(self, manga_id: IDType) -> Manga:
        url = f"https://ltn.hitomi.la/galleries/{manga_id}.js"
        req = UrlRequest(url=url, on_success=log_on_success)
        await asyncio.to_thread(req.wait)
        return Manga(**js2py.eval_js(req.result).to_dict())

    async def download_page(self, manga_id: IDType, page: MangaPage) -> None:
        headers = {
            "referer": f"https://hitomi.la/reader/{manga_id}.html",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
        url = await generate_download_url(page)
        req = UrlRequest(
            url=url,
            on_success=log_on_success,
            req_headers=headers,
            timeout=3,
            file_path=f"wow/{page.filename}",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        )
        await asyncio.to_thread(req.wait)

    async def download_manga(self, manga: Manga) -> None:
        for page in manga.pages:
            await self.download_page(manga.id, page)
