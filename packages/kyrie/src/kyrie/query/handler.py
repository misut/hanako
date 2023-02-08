import inspect
from collections.abc import Callable, Coroutine
from typing import Any, Generic, TypeVar

from kyrie.collections import FrozenDict
from kyrie.exceptions import OperatorNotFoundError
from kyrie.models import Query
from kyrie.query.context import QueryContext

SubQuery = TypeVar("SubQuery", bound=Query)
SubQueryContext = TypeVar("SubQueryContext", bound=QueryContext)
QueryResult = TypeVar("QueryResult")
QueryType = type[Query]
QueryOperator = Callable[[SubQuery, SubQueryContext], Coroutine[Any, Any, QueryResult]]


class QueryHandler(
    FrozenDict[QueryType, QueryOperator],
    Generic[SubQuery, SubQueryContext, QueryResult],
):
    @staticmethod
    def _create_tpl(
        operator: QueryOperator,
    ) -> tuple[QueryType, QueryOperator]:
        sig = inspect.signature(operator)
        params = iter(sig.parameters.values())

        first = next(params, None)
        second = next(params, None)
        assert (
            first and second
        ), f"'{operator.__name__}' should have at least two parameters."

        assert first.annotation, f"'{first.name}' should be annotated."
        assert issubclass(
            first.annotation, Query
        ), f"'{first.annotation.__name__}' should be a subclass of 'Query'"

        assert second.annotation, f"'{second.name}' should be annotated."
        assert issubclass(
            second.annotation, QueryContext
        ), f"'{second.annotation.__name__}' should be a subclass of 'QueryContext'"

        return first.annotation, operator

    @classmethod
    def new(cls, *operators: QueryOperator) -> "QueryHandler":
        mapping = {}
        for operator in operators:
            tp, op = cls._create_tpl(operator)
            assert tp not in mapping, f"'{tp.__name__}' should not be duplicated."
            mapping[tp] = op

        return cls(mapping)

    @classmethod
    def merge(cls, *handlers: "QueryHandler") -> "QueryHandler":
        return cls.new(
            *(operator for handler in handlers for operator in handler.values())
        )

    async def handle(self, query: Query, context: QueryContext) -> QueryResult:
        try:
            operator: QueryOperator = self[type(query)]
        except KeyError as err:
            raise OperatorNotFoundError() from err
        return await operator(query, context)
