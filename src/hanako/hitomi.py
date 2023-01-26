import asyncio
from struct import unpack
from typing import Literal

import js2py
from kivy.network.urlrequest import UrlRequest
from loguru import logger

from hanako.models import HitomiGallery, HitomiFile


def log_on_success(*_) -> None:
    logger.info("Succeeded.")


async def load_gallery(gallery_id: str) -> HitomiGallery:
    url = f"https://ltn.hitomi.la/galleries/{gallery_id}.js"
    req = UrlRequest(url=url, on_success=log_on_success)
    await asyncio.to_thread(req.wait)
    return HitomiGallery(**js2py.eval_js(req.result).to_dict())


async def generate_download_url(file: HitomiFile) -> str:
    req = UrlRequest(url="https://ltn.hitomi.la/gg.js")
    await asyncio.to_thread(req.wait)
    gg = js2py.eval_js(req.result)

    def determine_extension(file: HitomiFile) -> Literal["avif", "webp"]:
        if file.hasavif:
            return "avif"
        if file.haswebp:
            return "webp"

        raise ValueError(f"Not supported file: {file}")

    def determine_filename(file: HitomiFile) -> str:
        if file.hash == "":
            return file.name

        return file.hash

    def determine_route(file: HitomiFile, gg: js2py.base.JsObjectWrapper) -> str:
        g = file.hash[-3:]

        return f"{gg.b}{gg.s(g)}"

    def determine_subdomain(file: HitomiFile, gg: js2py.base.JsObjectWrapper) -> str:
        g = file.hash[-3:]

        return chr(97 + gg.m(int(gg.s(g))))

    extension = determine_extension(file)
    filename = determine_filename(file)
    route = determine_route(file, gg)
    subdomain = determine_subdomain(file, gg)

    return f"https://{subdomain}a.hitomi.la/{extension}/{route}/{filename}.{extension}"


async def download_file(file: HitomiFile, headers: dict[str, str]) -> None:
    url = await generate_download_url(file)
    logger.info(f"download({file.name}): {url}")
    req = UrlRequest(
        url=url,
        on_success=log_on_success,
        req_headers=headers,
        timeout=3,
        file_path=f"wow/{file.name}",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    )
    await asyncio.to_thread(req.wait)


async def download_gallery(gallery: HitomiGallery) -> None:
    headers = {
        "referer": f"https://hitomi.la/reader/{gallery.id}.html",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }
    for file in gallery.files:
        await download_file(file, headers)


async def load_gallery_ids(
    page: int = 0, item: int = 25, language: str = "all"
) -> list[str]:
    byte_beg = page * item * 4
    byte_end = byte_beg + item * 4 - 1
    headers = {
        "origin": "https://hitomi.la",
        "Range": f"bytes={byte_beg}-{byte_end}",
    }
    url = f"https://ltn.hitomi.la/index-{language}.nozomi"

    req = UrlRequest(
        url=url,
        timeout=3,
        method="GET",
        on_success=log_on_success,
        req_headers=headers,
    )
    await asyncio.to_thread(req.wait)

    ttl_bytes = len(req.result) // 4
    return [str(id) for id in unpack(f">{ttl_bytes}i", req.result)]
