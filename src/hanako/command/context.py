from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.frameworks import CommandContext
from kyrie.interfaces import Storage

from hanako import domain
from hanako.command.hitomi_fetcher import HitomiFetcher
from hanako.command.hitomi_downloader import HitomiDownloader

MangaStorage = Storage[domain.Manga]
PoolStorage = Storage[domain.Pool]


@dataclass(frozen=True)
class HanakoCommandContext(CommandContext):
    hitomi_downloader: Provider[HitomiDownloader]
    hitomi_fetcher: Provider[HitomiFetcher]
    manga_storage: Provider[MangaStorage]
    pool_storage: Provider[PoolStorage]
