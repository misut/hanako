import inspect
from collections.abc import Callable, Awaitable
from typing import TypeVar

from hanako.collections import FrozenDict
from hanako.command.commands import Command
from hanako.command.context import CommandContext

SubCommand = TypeVar("SubCommand", bound=Command)
CommandResult = TypeVar("CommandResult")
CommandOperator = Callable[[SubCommand, CommandContext], Awaitable[CommandResult]]


class OperatorNotFoundError(Exception):
    ...


class CommandHandler(FrozenDict[type, CommandOperator]):
    @staticmethod
    def _create_tpl(
        operator: CommandOperator,
    ) -> tuple[type, CommandOperator]:
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
            tpl = cls._create_tpl(operator)
            assert tpl[0] in mapping, f"'{tpl[0].__name__}' should not be duplicated."
            mapping[tpl[0]] = tpl[1]

        return cls(mapping)

    @classmethod
    def merge(cls, *handlers: "CommandHandler") -> "CommandHandler":
        return cls.new(
            *(operator for handler in handlers for operator in handler.values())
        )

    async def handle(
        self, command: SubCommand, context: CommandContext
    ) -> CommandResult:
        try:
            operator = self[type(command)]
        except KeyError as err:
            raise OperatorNotFoundError() from err

        result = await operator(command, context)

        return result
