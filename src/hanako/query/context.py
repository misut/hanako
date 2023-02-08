from contextvars import ContextVar
from dataclasses import dataclass

from kyrie.context import Provider
from kyrie.interfaces import Repository
from kyrie.query import QueryContext

from hanako.query.views import MangaView

MangaRepository = Repository[MangaView]


@dataclass(frozen=True)
class HanakoQueryContext(QueryContext):
    manga_repository: Provider[MangaRepository]


_query_context: ContextVar[HanakoQueryContext] = ContextVar("query_context")


def initialize_query_context(
    manga_repository_provider: Provider[MangaRepository],
) -> None:
    _query_context.set(HanakoQueryContext(manga_repository=manga_repository_provider))


def query_context() -> HanakoQueryContext:
    return _query_context.get()
