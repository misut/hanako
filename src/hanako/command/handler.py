import inspect
from collections.abc import Callable, Coroutine
from typing import Any

from hanako.collections import FrozenDict
from hanako.command.context import CommandContext
from hanako.exceptions import OperatorNotFoundError
from hanako.models import Command

CommandType = type[Command]
SubCommand = Any
CommandResult = Any
CommandOperator = Callable[
    [SubCommand, CommandContext], Coroutine[Any, Any, CommandResult]
]


class CommandHandler(FrozenDict[CommandType, CommandOperator]):
    @staticmethod
    def _create_tpl(
        operator: CommandOperator,
    ) -> tuple[CommandType, CommandOperator]:
        sig = inspect.signature(operator)
        params = iter(sig.parameters.values())

        first = next(params, None)
        second = next(params, None)
        assert (
            first and second
        ), f"'{operator.__name__}' should have at least two parameters."

        assert first.annotation, f"'{first.name}' should be annotated."
        assert issubclass(
            first.annotation, Command
        ), f"'{first.annotation.__name__}' should be a subclass of 'Command'"

        assert second.annotation, f"'{second.name}' should be annotated."
        assert issubclass(
            second.annotation, CommandContext
        ), f"'{second.annotation.__name__}' should be a subclass of 'CommandContext'"

        return first.annotation, operator

    @classmethod
    def new(cls, *operators: CommandOperator) -> "CommandHandler":
        mapping = {}
        for operator in operators:
            tp, op = cls._create_tpl(operator)
            assert tp not in mapping, f"'{tp.__name__}' should not be duplicated."
            mapping[tp] = op

        return cls(mapping)

    @classmethod
    def merge(cls, *handlers: "CommandHandler") -> "CommandHandler":
        return cls.new(
            *(operator for handler in handlers for operator in handler.values())
        )

    async def handle(self, command: Command, context: CommandContext) -> CommandResult:
        try:
            operator = self[type(command)]
        except KeyError as err:
            raise OperatorNotFoundError() from err
        return await operator(command, context)
