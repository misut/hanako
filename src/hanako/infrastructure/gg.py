import urllib.request
from typing import Protocol

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

    def __init__(self, url: str = DEFAULT_GGJS_URL) -> None:
        with urllib.request.urlopen(url) as response:
            self._ggjs = js2py.eval_js(response.read().decode("utf-8"))

    @property
    def b(self) -> str:
        return self._ggjs.b

    def m(self, g: int) -> int:
        return self._ggjs.m(g)

    def s(self, h: str) -> str:
        return self._ggjs.s(h)
