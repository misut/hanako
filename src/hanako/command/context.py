from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.frameworks import CommandContext
from kyrie.interfaces import Storage

from hanako.command.hitomi_service import HitomiService
from hanako.domain import Manga, Pool

MangaStorage = Storage[Manga]
PoolStorage = Storage[Pool]


@dataclass(frozen=True)
class HanakoCommandContext(CommandContext):
    hitomi_service: Provider[HitomiService]
    manga_storage: Provider[MangaStorage]
    pool_storage: Provider[PoolStorage]
