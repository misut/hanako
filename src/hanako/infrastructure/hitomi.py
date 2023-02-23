import asyncio
import urllib.request
from typing import Protocol, Self

import js2py
import pydantic
from kyrie.models import IDType, ValueObject

DEFAULT_GGJS_URL = "https://ltn.hitomi.la/gg.js"
DEFAULT_HITOMI_BATCH_SIZE = 10


def create_image_headers(gallery_id: IDType) -> dict[str, str]:
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": f"https://hitomi.la/reader/{gallery_id}.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    }


def create_thumbnail_url(hash: str) -> str:
    return f"https://btn.hitomi.la/avifsmallbigtn/{hash[-1]}/{hash[-3:-1]}/{hash}.avif"


class GG(Protocol):
    @property
    def b(self) -> str:
        ...

    def m(self, g: int) -> int:
        ...

    def s(self, h: str) -> str:
        ...


class GGjs(GG):
    _ggjs: js2py.base.JsObjectWrapper

    def __init__(self, ggjs: js2py.base.JsObjectWrapper) -> None:
        self._ggjs = ggjs

    @classmethod
    async def create(cls, url: str = DEFAULT_GGJS_URL) -> Self:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, urllib.request.urlopen, url)
        return cls(ggjs=js2py.eval_js(response.read().decode("utf-8")))

    @property
    def b(self) -> str:
        return self._ggjs.b

    def m(self, g: int) -> int:
        return self._ggjs.m(g)

    def s(self, h: str) -> str:
        return self._ggjs.s(h)


class HitomiArtist(ValueObject):
    name: str = pydantic.Field(alias="artist")
    url: str


class HitomiPage(ValueObject):
    filename: str = pydantic.Field(alias="name")
    width: int
    height: int
    hash: str

    hasavif: bool
    haswebp: bool

    @pydantic.validator("hasavif", "haswebp", pre=True)
    def parse_none(cls, value: None | object) -> bool | object:
        return value or False


class HitomiTag(ValueObject):
    tag: str
    url: str

    female: bool | None
    male: bool | None

    @pydantic.validator("female", "male", pre=True)
    def parse_bool(cls, value: str | int) -> bool | str | int:
        if value == "":
            return False
        return value


class HitomiGallery(ValueObject):
    id: IDType
    title: str
    type: str
    language: str
    galleryurl: str
    pages: list[HitomiPage] = pydantic.Field(alias="files")

    artists: list[HitomiArtist] = []
    related: list[IDType] = []
    tags: list[HitomiTag] = []

    @pydantic.validator("artists", "related", "tags", pre=True)
    def parse_none(cls, value: None | object) -> list | object:
        return value or []
