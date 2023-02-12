from kyrie.frameworks import CommandHandler
from kyrie.models import Command, IDType
from kyrie.monads import Option, Some, Null

from hanako import domain
from hanako.command.context import HanakoCommandContext


class FetchManga(Command):
    manga_id: IDType


async def fetch_manga(
    command: FetchManga, context: HanakoCommandContext
) -> Option[domain.MangaFetched]:
    hitomi_fetcher = context.hitomi_fetcher()
    manga_storage = context.manga_storage()

    gallery = await hitomi_fetcher.fetch_gallery(command.manga_id)
    thumbnail = await hitomi_fetcher.fetch_thumbnail(gallery)
    pages = [
        dict(url=hitomi_fetcher.generate_page_url(page), **page.dict())
        for page in gallery.pages
    ]
    event = domain.Manga.create(
        id=gallery.id,
        title=gallery.title,
        thumbnail=thumbnail,
        pages=pages,
    )
    await manga_storage.save_one(event.entity)

    return Some(event)


class FetchPool(Command):
    language: str
    offset: int
    limit: int


async def fetch_pool(
    command: FetchPool, context: HanakoCommandContext
) -> Option[domain.PoolFetched]:
    hitomi_fetcher = context.hitomi_fetcher()
    pool_storage = context.pool_storage()

    manga_ids = await hitomi_fetcher.fetch_gallery_ids(
        command.language, command.offset, command.limit
    )
    event = domain.Pool.create(
        manga_ids, command.language, command.offset, command.limit
    )
    await pool_storage.save_one(event.entity)

    return Some(event)


command_handler = CommandHandler.new(
    fetch_manga,
    fetch_pool,
)
