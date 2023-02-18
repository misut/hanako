from typing import Any, NamedTuple, Self

from kyrie.context import Context
from kyrie.handler import BaseHandler
from kyrie.models import Command, DomainEvent, IDType
from kyrie.monads import Option


class Always(DomainEvent):
    ...


class CommandContext(Context):
    ...


class CommandHandler(BaseHandler[Command, CommandContext, Option[DomainEvent]]):
    __target_type__ = Command
    __context_type__ = CommandContext
    __result_type__ = Option[DomainEvent]


class EventHandler(BaseHandler[DomainEvent, CommandContext, None]):
    __target_type__ = DomainEvent
    __context_type__ = CommandContext
    __result_type__ = None


class CommandBus(NamedTuple):
    context: CommandContext
    command_handler: CommandHandler
    event_handler: EventHandler

    @classmethod
    def new(
        cls,
        context: CommandContext,
        command_handler: CommandHandler,
        event_handler: EventHandler,
    ) -> Self:
        return cls(
            context=context,
            command_handler=command_handler,
            event_handler=event_handler,
        )

    async def dispatch(self, command: Command, *args: Any, **kwargs: Any) -> IDType:
        result = await self.command_handler.handle(
            command, self.context, *args, **kwargs
        )

        event = result.unwrap_or(Always(entity_id=""))
        if type(event) in self.event_handler:
            await self.event_handler.handle(event, self.context, *args, **kwargs)

        return event.entity_id
