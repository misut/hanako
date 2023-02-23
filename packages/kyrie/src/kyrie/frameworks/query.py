from typing import Any, NamedTuple, Self

from kyrie.context import Context
from kyrie.handler import BaseHandler
from kyrie.models import Query, View


class QueryContext(Context):
    ...


class QueryHandler(BaseHandler[Query, QueryContext, View | None]):
    __target_type__ = Query
    __context_type__ = QueryContext
    __result_type__ = View | None


class QueryBus(NamedTuple):
    context: QueryContext
    handler: QueryHandler

    @classmethod
    def new(cls, context: QueryContext, *handlers: QueryHandler) -> Self:
        handler = QueryHandler.merge(*handlers)
        return cls(context=context, handler=handler)

    async def query(self, query: Query, *args: Any, **kwargs: Any) -> View | None:
        return await self.handler.handle(query, self.context, *args, **kwargs)
