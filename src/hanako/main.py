import asyncio

from hanako import app
from hanako.command import initialize_command_context
from hanako.context import Provider
from hanako.drivers import (
    Hitomi,
    SqlDatabase,
    SqlMangaRepository,
    SqlMangaStorage,
    Subscriber,
)
from hanako.query import initialize_query_context

DEFAULT_SQLITE_URL = "sqlite:///hanako.db?check_same_thread=False"


def build_hanako() -> app.Hanako:
    database = SqlDatabase(url=DEFAULT_SQLITE_URL)
    database.create_all()

    initialize_command_context(
        Provider(Hitomi), Provider(SqlMangaStorage, session_factory=database.session)
    )
    initialize_query_context(
        Provider(SqlMangaRepository, session_factory=database.session)
    )

    hanako = app.Hanako()
    subscriber = Subscriber()
    hanako.bind(subscriber)
    return hanako


def run(debug: bool = True) -> None:
    hanako = build_hanako()
    asyncio.run(hanako.async_run(), debug=debug)
