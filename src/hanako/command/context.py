from contextvars import ContextVar
from dataclasses import dataclass

from hanako.context import Context, Provider
from hanako.domain import Manga
from hanako.interfaces import MangaService, Storage

MangaStorage = Storage[Manga]


@dataclass(frozen=True)
class CommandContext(Context):
    hitomi: Provider[MangaService]
    manga_storage: Provider[MangaStorage]


_command_context: ContextVar[CommandContext] = ContextVar("command_context")


def initialize_command_context(
    hitomi_provider: Provider[MangaService],
    manga_storage_provider: Provider[MangaStorage],
) -> None:
    _command_context.set(
        CommandContext(hitomi=hitomi_provider, manga_storage=manga_storage_provider)
    )


def command_context() -> CommandContext:
    return _command_context.get()
