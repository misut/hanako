import asyncio

from hanako import app
from hanako.command import CommandContext
from hanako.drivers import Hitomi, Subscriber


def build_hanako() -> app.Hanako:
    command_context = CommandContext(hitomi=Hitomi)
    hanako = app.Hanako(command_context=command_context)

    subscriber = Subscriber()
    hanako.bind(subscriber)
    return hanako


def run(debug: bool = True) -> None:
    hanako = build_hanako()
    asyncio.run(hanako.async_run(), debug=debug)
