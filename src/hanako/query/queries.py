from kyrie.frameworks import QueryHandler
from kyrie.models import IDType, Query

from hanako.query.context import HanakoQueryContext
from hanako.query.views import MangaView

__all__ = ("GetManga",)


class GetManga(Query):
    manga_id: IDType


async def get_manga(query: GetManga, context: HanakoQueryContext) -> MangaView | None:
    return await context.manga_repository().find_one(id=query.manga_id)


query_handler = QueryHandler.new(
    get_manga,
)
