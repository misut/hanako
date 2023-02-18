from collections.abc import Awaitable, Callable
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def async_partial(
    coro: Callable[Concatenate[T, P], Awaitable[R]], /, arg: T
) -> Callable[P, Awaitable[R]]:
    async def new_coroutine(*coro_args: P.args, **coro_kwargs: P.kwargs) -> R:
        return await coro(arg, *coro_args, **coro_kwargs)

    return new_coroutine
