from kyrie.command import CommandHandler
from kyrie.models import Command, IDType

from hanako.command.context import HanakoCommandContext


class FetchMangaIDs(Command):
    offset: int
    limit: int


async def fetch_manga_ids(
    command: FetchMangaIDs,
    context: HanakoCommandContext,
) -> list[IDType]:
    hitomi = context.hitomi()
    manga_ids = await hitomi.fetch_ids(command.offset, command.limit)
    return manga_ids


command_handler = CommandHandler.new(
    fetch_manga_ids,
)
