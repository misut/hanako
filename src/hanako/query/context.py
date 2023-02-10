from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.frameworks import QueryContext
from kyrie.interfaces import Repository

from hanako.query.views import MangaView

MangaRepository = Repository[MangaView]


@dataclass(frozen=True)
class HanakoQueryContext(QueryContext):
    manga_repository: Provider[MangaRepository]
