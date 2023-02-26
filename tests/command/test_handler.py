import pytest

from hanako.command import FetchError, HanakoCommandContext, command_handler, commands
from hanako.command.exceptions import DownloadError, WriteError


@pytest.mark.asyncio
async def test_fetch_manga(command_context: HanakoCommandContext) -> None:
    command = commands.FetchManga(manga_id="manga_1")
    event = await command_handler.handle(command, command_context)
    assert not isinstance(event, list)
    event.unwrap()

    command = commands.FetchManga(manga_id="manga_1")
    event = await command_handler.handle(command, command_context)
    assert not isinstance(event, list)
    with pytest.raises(ValueError, match=r"Already Fetched"):
        event.expect("Already Fetched")

    command = commands.FetchManga(manga_id="not_exist")
    with pytest.raises(FetchError):
        await command_handler.handle(command, command_context)


@pytest.mark.asyncio
async def test_cache_manga(command_context: HanakoCommandContext) -> None:
    command = commands.CacheManga(manga_id="manga_3")
    events = await command_handler.handle(command, command_context)
    assert isinstance(events, list)
    for event in events:
        event.unwrap()

    command = commands.CacheManga(manga_id="not_exist")
    events = await command_handler.handle(command, command_context)
    assert isinstance(events, list)
    assert len(events) == 0

    command = commands.CacheManga(manga_id="manga_3")
    events = await command_handler.handle(command, command_context)
    assert isinstance(events, list)
    assert len(events) == 0

    command = commands.CacheManga(manga_id="download_failed")
    with pytest.raises(DownloadError):
        await command_handler.handle(command, command_context)

    command = commands.CacheManga(manga_id="cache_failed")
    with pytest.raises(WriteError):
        await command_handler.handle(command, command_context)


@pytest.mark.asyncio
async def test_cache_manga_page(command_context: HanakoCommandContext) -> None:
    command = commands.CacheMangaPage(manga_id="manga_2", page_number=0)
    event = await command_handler.handle(command, command_context)
    assert not isinstance(event, list)
    event.unwrap()

    command = commands.CacheMangaPage(manga_id="not_exist", page_number=0)
    event = await command_handler.handle(command, command_context)
    assert not isinstance(event, list)
    assert not event

    command = commands.CacheMangaPage(manga_id="manga_2", page_number=0)
    event = await command_handler.handle(command, command_context)
    assert not isinstance(event, list)
    assert not event

    command = commands.CacheMangaPage(manga_id="download_failed", page_number=0)
    with pytest.raises(DownloadError):
        await command_handler.handle(command, command_context)

    command = commands.CacheMangaPage(manga_id="cache_failed", page_number=0)
    with pytest.raises(WriteError):
        await command_handler.handle(command, command_context)


@pytest.mark.asyncio
async def test_fetch_pool(command_context: HanakoCommandContext) -> None:
    command = commands.FetchPool(language="korean")
    events = await command_handler.handle(command, command_context)
    assert isinstance(events, list)
    for event in events:
        event.unwrap()

    # Check Duplicate Pass
    command = commands.FetchPool(language="korean")
    await command_handler.handle(command, command_context)

    command = commands.FetchPool(language="fetch_failed")
    with pytest.raises(FetchError):
        await command_handler.handle(command, command_context)
