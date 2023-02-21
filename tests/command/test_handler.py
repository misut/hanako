import pytest

from hanako.command import command_handler, HanakoCommandContext, commands


@pytest.mark.asyncio
async def test_command_handler(command_context: HanakoCommandContext) -> None:
    command = commands.FetchManga(manga_id="manga_1")
    event = await command_handler.handle(command, command_context)
    event.unwrap()
