from contextvars import ContextVar

from kyrie.frameworks.command import (
    CommandBus,
    CommandContext,
    CommandHandler,
    EventHandler,
)
from kyrie.frameworks.query import QueryBus, QueryContext, QueryHandler

_command_bus: ContextVar[CommandBus] = ContextVar("command_bus")
_query_bus: ContextVar[QueryBus] = ContextVar("query_bus")


def initialize_command_bus(
    context: CommandContext,
    command_handler: CommandHandler,
    event_handler: EventHandler,
) -> None:
    _command_bus.set(CommandBus.new(context, command_handler, event_handler))


def initialize_query_bus(context: QueryContext, *handlers: QueryHandler) -> None:
    _query_bus.set(QueryBus.new(context, *handlers))


def command_bus() -> CommandBus:
    return _command_bus.get()


def query_bus() -> QueryBus:
    return _query_bus.get()
