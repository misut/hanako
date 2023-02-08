from contextvars import ContextVar
from dataclasses import dataclass

from kyrie.command import CommandContext
from kyrie.context import Provider
from kyrie.interfaces import Storage

from hanako.command.manga_service import MangaService
from hanako.domain import Manga

MangaStorage = Storage[Manga]


@dataclass(frozen=True)
class HanakoCommandContext(CommandContext):
    hitomi: Provider[MangaService]
    manga_storage: Provider[MangaStorage]


_command_context: ContextVar[HanakoCommandContext] = ContextVar("command_context")


def initialize_command_context(
    hitomi_provider: Provider[MangaService],
    manga_storage_provider: Provider[MangaStorage],
) -> None:
    _command_context.set(
        HanakoCommandContext(
            hitomi=hitomi_provider, manga_storage=manga_storage_provider
        )
    )


def command_context() -> HanakoCommandContext:
    return _command_context.get()
