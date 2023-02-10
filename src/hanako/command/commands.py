from kyrie.frameworks import CommandHandler
from kyrie.models import Command, IDType

from hanako import domain
from hanako.command.context import HanakoCommandContext


class FetchManga(Command):
    manga_id: IDType


async def fetch_manga(
    command: FetchManga, context: HanakoCommandContext
) -> domain.MangaFetched:
    hitomi = context.hitomi_service()
    manga_storage = context.manga_storage()

    gallery = await hitomi.fetch_gallery(command.manga_id)
    event = domain.Manga.create(gallery.id, gallery.title)
    await manga_storage.save_one(event.entity)

    return event


class FetchPool(Command):
    language: str
    offset: int
    limit: int


async def fetch_pool(
    command: FetchPool, context: HanakoCommandContext
) -> domain.PoolFetched:
    hitomi = context.hitomi_service()
    pool_storage = context.pool_storage()

    manga_ids = await hitomi.fetch_gallery_ids(
        command.language, command.offset, command.limit
    )
    event = domain.Pool.create(
        manga_ids, command.language, command.offset, command.limit
    )
    await pool_storage.save_one(event.entity)

    return event


command_handler = CommandHandler.new(
    fetch_manga,
    fetch_pool,
)
