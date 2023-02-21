from kyrie.frameworks import CommandHandler
from kyrie.monads import Null, Option, Some

from hanako import domain
from hanako.command.commands import (
    CacheManga,
    FetchManga,
    FetchMangaUsingPool,
    FetchPool,
    UpdatePool,
)
from hanako.command.context import HanakoCommandContext


async def fetch_manga(
    command: FetchManga, context: HanakoCommandContext
) -> Option[domain.MangaFetched]:
    gallery_service = context.gallery_service()
    manga_storage = context.manga_storage()

    (fetched,) = await gallery_service.fetch_galleries(command.manga_id)
    if fetched.is_err():
        return Null

    event = domain.Manga.create(**fetched.unwrap().dict())
    await manga_storage.save_one(event.entity)
    return Some(event)


async def cache_manga(
    command: CacheManga, context: HanakoCommandContext
) -> Option[domain.MangaCached]:
    manga_cache = context.manga_cache()
    manga_downloader = context.manga_downloader()
    manga_storage = context.manga_storage()

    entity = await manga_storage.find_one(id=command.manga_id)
    if not entity:
        raise ValueError(f"Manga '{command.manga_id}' Not Fetched Before")
    manga = entity.unwrap()

    downloaded = await manga_downloader.download_manga(manga)
    if downloaded.is_err():
        return Null
    page_files = downloaded.unwrap()
    cached_in = await manga_cache.write(manga, page_files)
    event = manga.cache(cached_in)

    return Some(event)


async def fetch_pool(
    command: FetchPool, context: HanakoCommandContext
) -> Option[domain.PoolFetched]:
    gallery_service = context.gallery_service()
    pool_storage = context.pool_storage()

    fetched = await gallery_service.fetch_pool(
        command.language, command.offset, command.limit
    )
    if fetched.is_err():
        return Null

    event = domain.Pool.create(**fetched.unwrap().dict())
    await pool_storage.save_one(event.entity)

    return Some(event)


async def update_pool(
    command: UpdatePool, context: HanakoCommandContext
) -> Option[domain.PoolUpdated]:
    gallery_service = context.gallery_service()
    pool_storage = context.pool_storage()

    entity = await pool_storage.find_one(id=command.pool_id)
    if not entity:
        raise ValueError(f"Pool '{command.pool_id}' Not Fetched Before")
    pool = entity.unwrap()

    gallery_pool = await gallery_service.fetch_pool(
        pool.language, pool.offset, pool.limit
    )
    if gallery_pool.is_err():
        return Null

    event = pool.update(gallery_pool.unwrap().id_list)
    await pool_storage.save_one(pool)

    return Some(event)


command_handler = CommandHandler.new(
    cache_manga,
    fetch_manga,
    fetch_pool,
    update_pool,
)
