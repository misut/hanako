from kyrie.frameworks import QueryHandler
from kyrie.models import IDType, Query

from hanako.query.context import HanakoQueryContext
from hanako.query.views import MangaView, PoolView

__all__ = ("GetManga",)


class GetManga(Query):
    manga_id: IDType


async def get_manga(query: GetManga, context: HanakoQueryContext) -> MangaView | None:
    return await context.manga_repository().find_one(id=query.manga_id)


class GetLatestPool(Query):
    language: str
    offset: int = 0
    limit: int = 0


async def get_latest_pool(
    query: GetLatestPool, context: HanakoQueryContext
) -> PoolView | None:
    return await context.pool_repository().find_one(
        language=query.language, offset=query.offset, limit=query.limit
    )


query_handler = QueryHandler.new(
    get_manga,
    get_latest_pool,
)
