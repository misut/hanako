from contextvars import ContextVar
from dataclasses import dataclass

from hanako.context import Context, Provider
from hanako.interfaces import Repository
from hanako.query.views import MangaView

MangaRepository = Repository[MangaView]


@dataclass(frozen=True)
class QueryContext(Context):
    manga_repository: Provider[MangaRepository]


_query_context: ContextVar[QueryContext] = ContextVar("query_context")


def initialize_query_context(
    manga_repository_provider: Provider[MangaRepository],
) -> None:
    _query_context.set(QueryContext(manga_repository=manga_repository_provider))


def query_context() -> QueryContext:
    return _query_context.get()
