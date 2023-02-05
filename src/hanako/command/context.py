from contextvars import ContextVar
from dataclasses import dataclass

from hanako.context import Context, Provider
from hanako.domain import Manga
from hanako.drivers import Hitomi
from hanako.interfaces import Storage

MangaStorage = Storage[Manga]


@dataclass(frozen=True)
class CommandContext(Context):
    hitomi: Provider[Hitomi]
    manga_storage: Provider[MangaStorage]


_command_context: ContextVar[CommandContext] = ContextVar("command_context")


def initialize_command_context(
    hitomi_provider: Provider[Hitomi],
    manga_storage_provider: Provider[MangaStorage],
) -> None:
    _command_context.set(
        CommandContext(hitomi=hitomi_provider, manga_storage=manga_storage_provider)
    )


def command_context() -> CommandContext:
    return _command_context.get()
