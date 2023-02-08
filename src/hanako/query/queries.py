from kyrie.models import IDType, Query
from kyrie.monads import Option
from kyrie.query import QueryHandler

from hanako.query.context import HanakoQueryContext
from hanako.query.views import MangaView


class GetManga(Query):
    manga_id: IDType


async def get_manga(query: GetManga, context: HanakoQueryContext) -> Option[MangaView]:
    return context.manga_repository().find_one(id=query.manga_id)


query_handler = QueryHandler.new(
    get_manga,
)
