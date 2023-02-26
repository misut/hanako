from kyrie.frameworks import CommandHandler
from kyrie.monads import Null, Option, Some

from hanako import domain
from hanako.command.commands import *
from hanako.command.context import HanakoCommandContext
from hanako.command.exceptions import FetchError


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
    galleries = fetched.unwrap()
    if len(galleries) == 0:
        raise FetchError(f"No Gallery With ID '{command.manga_id}'")

    event = domain.Manga.fetch(**galleries[0].dict())

    await manga_storage.save_one(event.entity)
    return Some(event)


async def fetch_manga_list(
    command: FetchMangaList, context: HanakoCommandContext
) -> list[Option[domain.MangaFetched]]:
    gallery_service = context.gallery_service()
    manga_storage = context.manga_storage()

    found_list = [
        await manga_storage.find_one(id=manga_id) for manga_id in command.manga_id_list
    ]
    not_found = [
        manga_id
        for manga_id, found in zip(command.manga_id_list, found_list)
        if not found
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
        event = domain.Manga.fetch(**next(galleries_iterator).dict())
        events.append(Some(event))
        mangas.append(event.entity)

    await manga_storage.save(*mangas)
    return events


async def cache_manga(
    command: CacheManga, context: HanakoCommandContext
) -> list[Option[domain.MangaPageCached]]:
    manga_cache = context.manga_cache()
    manga_downloader = context.manga_downloader()
    manga_storage = context.manga_storage()

    found = await manga_storage.find_one(id=command.manga_id)
    if not found:
        return []
    manga = found.unwrap()
    if manga.is_cached():
        return []

    downloaded = await manga_downloader.download_manga(manga)
    if downloaded.is_err():
        raise downloaded.unwrap_err()
    page_files = downloaded.unwrap()
    written = await manga_cache.write(manga, page_files)
    if not written:
        raise written.unwrap_err()

    cached_in_list = written.unwrap()
    events: list[Option[domain.MangaPageCached]] = []
    for page_number, cached_in in enumerate(cached_in_list):
        if manga.is_page_cached(page_number):
            events.append(Null)
            continue
        events.append(Some(manga.cache_page(page_number, cached_in)))

    await manga_storage.save_one(manga)
    return events


async def cache_manga_page(
    command: CacheMangaPage, context: HanakoCommandContext
) -> Option[domain.MangaPageCached]:
    manga_cache = context.manga_cache()
    manga_downloader = context.manga_downloader()
    manga_storage = context.manga_storage()

    found = await manga_storage.find_one(id=command.manga_id)
    if not found:
        return Null
    manga = found.unwrap()
    if manga.is_page_cached(command.page_number):
        return Null

    downloaded = await manga_downloader.download_page(manga, command.page_number)
    if not downloaded:
        raise downloaded.unwrap_err()
    page_file = downloaded.unwrap()
    written = await manga_cache.write_one(manga, page_file, command.page_number)
    if not written:
        raise written.unwrap_err()

    cached_in = written.unwrap()
    event = manga.cache_page(command.page_number, cached_in)

    await manga_storage.save_one(manga)
    return Some(event)


async def fetch_pool(
    command: FetchPool, context: HanakoCommandContext
) -> list[Option[domain.PoolEntryFetched]]:
    gallery_service = context.gallery_service()
    pool_entry_storage = context.pool_entry_storage()

    fetched = await gallery_service.fetch_pool(
        command.language, command.offset, command.limit
    )
    if not fetched:
        raise fetched.unwrap_err()

    pool = fetched.unwrap()
    events: list[Option[domain.PoolEntryFetched]] = []
    pool_entries: list[domain.PoolEntry] = []
    for manga_id in pool.id_list:
        event = domain.PoolEntry.fetch(manga_id=manga_id, language=pool.language)
        events.append(Some(event))
        pool_entries.append(event.entity)

    await pool_entry_storage.save(*pool_entries)
    return events


command_handler = CommandHandler.new(
    cache_manga,
    cache_manga_page,
    fetch_manga,
    fetch_manga_list,
    fetch_pool,
)
