from collections import UserDict
from collections.abc import Callable, Coroutine
from typing import Any, Self

import flet

Handler = Callable[[flet.Page], Coroutine[Any, Any, None]]


class Router(UserDict[str, Handler]):
    _path: str

    def __init__(self, prefix: str = "") -> None:
        if prefix:
            assert prefix.startswith("/"), "Path Should Start With '/'"
            assert not prefix.endswith("/"), "Path Should Not End With '/'"
        self._path = prefix
        super().__init__()

    @property
    def path(self) -> str:
        return self._path

    def add_route(self, path: str, handler: Handler) -> None:
        assert path not in self, f"Path '{path}' Already Added"
        self[path] = handler

    def include_router(self, router: Self) -> None:
        for path, handler in router.items():
            self.add_route(router.path + path, handler)

    def route(self, path: str) -> Callable[[Handler], Handler]:
        def decorator(handler: Handler) -> Handler:
            self.add_route(path, handler)
            return handler

        return decorator
