import inspect
from collections.abc import Callable, Coroutine
from typing import Any, ClassVar, Concatenate, Generic, Self, TypeVar

from kyrie.collections import FrozenDict
from kyrie.context import Context
from kyrie.exceptions import ProcessorNotFoundError
from kyrie.models import ImmutableModel

Target = TypeVar("Target", bound=ImmutableModel)
TargetContext = TypeVar("TargetContext", bound=Context)
Result = TypeVar("Result")
Processor = Callable[Concatenate[Target, TargetContext, ...], Coroutine[Any, Any, Result]]  # type: ignore


class BaseHandler(
    FrozenDict[type[Target], Processor], Generic[Target, TargetContext, Result]
):
    __target_type__: ClassVar[type[Target]]  # type: ignore
    __context_type__: ClassVar[type[TargetContext]]  # type: ignore
    __result_type__: ClassVar[type[Result] | None]  # type: ignore

    @classmethod
    def _create_tpl(cls, processor: Processor) -> tuple[type[Target], Processor]:
        sig = inspect.signature(processor)
        params = iter(sig.parameters.values())

        first = next(params, None)
        second = next(params, None)
        assert (
            first and second
        ), f"'{processor.__name__}' should have at least two parameters."

        assert first.annotation, f"'{first.name}' Not Annotated"
        assert issubclass(
            first.annotation, cls.__target_type__
        ), f"'{first.annotation.__name__}' should be a subclass of '{cls.__target_type__.__name__}'"

        assert second.annotation, f"'{second.name}' Not Annotated"
        assert issubclass(
            second.annotation, cls.__context_type__
        ), f"'{second.annotation.__name__}' should be a subclass of '{cls.__context_type__.__name__}'"

        assert (
            sig.return_annotation != inspect.Signature.empty
        ), f"Return Type Not Annotated"

        return first.annotation, processor

    @classmethod
    def new(cls, *processors: Processor) -> Self:
        mapping = {}
        for processor in processors:
            tp, op = cls._create_tpl(processor)
            assert tp not in mapping, f"'{tp.__name__}' Already Assigned"
            mapping[tp] = op

        return cls(mapping)

    @classmethod
    def merge(cls, *handlers: Self) -> Self:
        return cls.new(
            *(operator for handler in handlers for operator in handler.values())
        )

    async def handle(
        self,
        target: Target,
        context: TargetContext,
        *args: Any,
        **kwargs: Any,
    ) -> Result:
        try:
            processor = self[type(target)]
        except KeyError as err:
            raise ProcessorNotFoundError() from err
        return await processor(target, context, *args, **kwargs)
