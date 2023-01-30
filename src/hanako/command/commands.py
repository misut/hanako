from loguru import logger

from hanako.command.context import CommandContext
from hanako.command.handler import CommandHandler
from hanako.models import Command, IDType


def log_on_success(*_) -> None:
    logger.info("Succeeded.")


class FetchMangaIDs(Command):
    offset: int
    limit: int


async def fetch_manga_ids(
    command: FetchMangaIDs,
    context: CommandContext,
) -> list[IDType]:
    hitomi = context.hitomi()
    manga_ids = await hitomi.fetch_ids(command.offset, command.limit)
    return manga_ids


command_handler = CommandHandler.new(
    fetch_manga_ids,
)
