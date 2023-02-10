from kyrie.frameworks import EventHandler, NotOccured

from hanako.command.context import HanakoCommandContext


async def not_occured(event: NotOccured, context: HanakoCommandContext) -> None:
    print("Wow")


event_handler = EventHandler.new(not_occured)
