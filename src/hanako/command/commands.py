from kyrie.command import CommandHandler
from kyrie.models import Command, IDType

from hanako import domain
from hanako.command.context import HanakoCommandContext


class FetchManga(Command):
    manga_id: IDType


async def fetch_manga(command: FetchManga, context: HanakoCommandContext) -> IDType:
    hitomi = context.hitomi()
    manga_storage = context.manga_storage()

    gallery = await hitomi.fetch_gallery(command.manga_id)
    event = domain.Manga.create(gallery.id, gallery.title)
    manga_storage.save_one(event.entity)

    return event.entity_id


class FetchPool(Command):
    language: str
    offset: int
    limit: int


async def fetch_pool(command: FetchPool, context: HanakoCommandContext) -> IDType:
    hitomi = context.hitomi()
    pool_storage = context.pool_storage()

    manga_ids = await hitomi.fetch_gallery_ids(command.offset, command.limit)
    event = domain.Pool.create(
        manga_ids, command.language, command.offset, command.limit
    )
    pool_storage.save_one(event.entity)

    return event.entity_id


command_handler = CommandHandler.new(
    fetch_manga,
    fetch_pool,
)
