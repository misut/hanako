import asyncio

import js2py
from kivy.network.urlrequest import UrlRequest
from loguru import logger

from hanako.models import HitomiGallery

header = {
    "referer": "https://hitomi.la/reader/1234567.html",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.3",
}


def log_on_success(*_) -> None:
    logger.info("Succeeded.")


async def load_gallery(gallery_id: str) -> HitomiGallery:
    url = f"https://ltn.hitomi.la/galleries/{gallery_id}.js"
    req = UrlRequest(url, on_success=log_on_success)
    await asyncio.to_thread(req.wait)
    return HitomiGallery(**js2py.eval_js(req.result).to_dict())


async def download_gallery(*_) -> None:
    url = ""
    req = UrlRequest(url)
    await asyncio.to_thread(req.wait)
