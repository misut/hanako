from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.frameworks import CommandContext
from kyrie.interfaces import Storage

from hanako import domain
from hanako.command.gallery_service import GalleryService
from hanako.command.manga_cache import MangaCache
from hanako.command.manga_downloader import MangaDownloader

MangaStorage = Storage[domain.Manga]
PoolEntryStorage = Storage[domain.PoolEntry]


@dataclass(frozen=True)
class HanakoCommandContext(CommandContext):
    gallery_service: Provider[GalleryService]
    manga_cache: Provider[MangaCache]
    manga_downloader: Provider[MangaDownloader]
    manga_storage: Provider[MangaStorage]
    pool_entry_storage: Provider[PoolEntryStorage]
