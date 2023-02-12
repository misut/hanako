from kyrie.frameworks import Always, EventHandler

from hanako.command.context import HanakoCommandContext


async def handle_always(event: Always, context: HanakoCommandContext) -> None:
    print("Wow")


event_handler = EventHandler.new(handle_always)
