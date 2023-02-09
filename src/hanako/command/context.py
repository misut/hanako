from contextvars import ContextVar
from dataclasses import dataclass

from kyrie.command import CommandContext
from kyrie.context import Provider
from kyrie.interfaces import Storage

from hanako.command.hitomi_service import HitomiService
from hanako.domain import Manga, Pool

MangaStorage = Storage[Manga]
PoolStorage = Storage[Pool]


@dataclass(frozen=True)
class HanakoCommandContext(CommandContext):
    hitomi: Provider[HitomiService]
    manga_storage: Provider[MangaStorage]
    pool_storage: Provider[PoolStorage]


_command_context: ContextVar[HanakoCommandContext] = ContextVar("command_context")


def initialize_command_context(
    hitomi_provider: Provider[HitomiService],
    manga_storage_provider: Provider[MangaStorage],
    pool_storage_provider: Provider[PoolStorage],
) -> None:
    _command_context.set(
        HanakoCommandContext(
            hitomi=hitomi_provider,
            manga_storage=manga_storage_provider,
            pool_storage=pool_storage_provider,
        )
    )


def command_context() -> HanakoCommandContext:
    return _command_context.get()
