from hanako.models import IDType, Query
from hanako.query.context import QueryContext
from hanako.query.handler import QueryHandler
from hanako.query.views import MangaView


class GetManga(Query):
    manga_id: IDType


def get_manga(query: GetManga, context: QueryContext) -> MangaView:
    return context.manga_repository().find_one(id=query.manga_id).unwrap()


query_handler = QueryHandler.new(
    get_manga,
)
