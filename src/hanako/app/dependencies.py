from kyrie.context import Provider
from kyrie.frameworks import initialize_command_bus, initialize_query_bus

from hanako.command import HanakoCommandContext, command_handler, event_handler
from hanako.infrastructure import (
    GGjs,
    HttpClient,
    HttpHitomiService,
    SqliteDatabase,
    SqliteMangaRepository,
    SqliteMangaStorage,
    SqlitePoolStorage,
)
from hanako.query import HanakoQueryContext, query_handler


def initialize_dependencies() -> None:
    http_client = HttpClient()
    gg = GGjs()
    sqlite_database = SqliteDatabase(
        "sqlite+aiosqlite:///:memory:?check_same_thread=False"
    )

    command_context = HanakoCommandContext(
        hitomi_service=Provider(
            HttpHitomiService, client_factory=http_client.client, gg=gg
        ),
        manga_storage=Provider(
            SqliteMangaStorage, session_factory=sqlite_database.session
        ),
        pool_storage=Provider(
            SqlitePoolStorage, session_factory=sqlite_database.session
        ),
    )
    initialize_command_bus(command_context, command_handler, event_handler)

    query_context = HanakoQueryContext(
        manga_repository=Provider(
            SqliteMangaRepository, session_factory=sqlite_database.session
        )
    )
    initialize_query_bus(query_context, query_handler)
