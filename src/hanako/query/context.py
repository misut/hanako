from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.frameworks import QueryContext
from kyrie.interfaces import Repository

from hanako.query.views import MangaView, PoolEntryView

MangaRepository = Repository[MangaView]
PoolEntryRepository = Repository[PoolEntryView]


@dataclass(frozen=True)
class HanakoQueryContext(QueryContext):
    manga_repository: Provider[MangaRepository]
    pool_entry_repository: Provider[PoolEntryRepository]
