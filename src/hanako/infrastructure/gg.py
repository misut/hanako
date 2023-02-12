import asyncio

import urllib.request
from typing import Protocol, Self

import js2py

DEFAULT_GGJS_URL = "https://ltn.hitomi.la/gg.js"


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
