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

    found = await manga_storage.find_one(id=command.manga_id)
    if found:
        return Null
    fetched = await gallery_service.fetch_galleries(command.manga_id)
    if fetched.is_err():
        raise fetched.unwrap_err()

    event = domain.Manga.create(**fetched.unwrap()[0].dict())
    await manga_storage.save_one(event.entity)
    return Some(event)


async def fetch_manga_using_pool(
    command: FetchMangaUsingPool, context: HanakoCommandContext
) -> list[Option[domain.MangaFetched]]:
    gallery_service = context.gallery_service()
    manga_storage = context.manga_storage()
    pool_storage = context.pool_storage()

    entity = await pool_storage.find_one(id=command.pool_id)
    if not entity:
        return []
    pool = entity.unwrap()

    if command.limit == 0:
        manga_ids = pool.id_list[command.offset :]
    else:
        manga_ids = pool.id_list[command.offset : command.offset + command.limit]
    found_list = [await manga_storage.find_one(id=manga_id) for manga_id in manga_ids]
    not_found = [
        manga_id for manga_id, found in zip(manga_ids, found_list) if not found
    ]

    fetched = await gallery_service.fetch_galleries(*not_found)
    if not fetched:
        raise fetched.unwrap_err()
    galleries_iterator = iter(fetched.unwrap())

    events: list[Option[domain.MangaFetched]] = []
    mangas: list[domain.Manga] = []
    for found in found_list:
        if found:
            events.append(Null)
            continue

        event = domain.Manga.create(**next(galleries_iterator).dict())
        events.append(Some(event))
        mangas.append(event.entity)

    await manga_storage.save(*mangas)
    return events


async def cache_manga(
    command: CacheManga, context: HanakoCommandContext
) -> Option[domain.MangaCached]:
    manga_cache = context.manga_cache()
    manga_downloader = context.manga_downloader()
    manga_storage = context.manga_storage()

    entity = await manga_storage.find_one(id=command.manga_id)
    if not entity:
        return Null
    manga = entity.unwrap()
    if manga.is_cached():
        return Null

    downloaded = await manga_downloader.download_manga(manga)
    if downloaded.is_err():
        raise downloaded.unwrap_err()
    page_files = downloaded.unwrap()
    cached_in = await manga_cache.write(manga, page_files)
    event = manga.cache(cached_in)
    await manga_storage.save_one(manga)

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
        raise fetched.unwrap_err()
    print(fetched.unwrap())

    event = domain.Pool.create(**fetched.unwrap().dict())
    await pool_storage.save_one(event.entity)

    return Some(event)


async def update_pool(
    command: UpdatePool, context: HanakoCommandContext
) -> Option[domain.PoolUpdated]:
    gallery_service = context.gallery_service()
    pool_storage = context.pool_storage()

    found = await pool_storage.find_one(id=command.pool_id)
    if not found:
        raise ValueError(f"Pool '{command.pool_id}' Not Fetched Before")
    pool = found.unwrap()

    fetched = await gallery_service.fetch_pool(pool.language, pool.offset, pool.limit)
    if fetched.is_err():
        raise fetched.unwrap_err()

    event = pool.update(fetched.unwrap().id_list)
    await pool_storage.save_one(pool)

    return Some(event)


command_handler = CommandHandler.new(
    cache_manga,
    fetch_manga,
    fetch_manga_using_pool,
    fetch_pool,
    update_pool,
)
