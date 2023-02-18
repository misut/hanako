from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.frameworks import QueryContext
from kyrie.interfaces import Repository

from hanako.query.views import MangaView, PoolView

MangaRepository = Repository[MangaView]
PoolRepository = Repository[PoolView]


@dataclass(frozen=True)
class HanakoQueryContext(QueryContext):
    manga_repository: Provider[MangaRepository]
    pool_repository: Provider[PoolRepository]
