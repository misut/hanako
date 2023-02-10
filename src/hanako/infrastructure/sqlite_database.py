from urllib import parse

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from hanako.infrastructure.orm import BaseOrm


class SqliteDatabase:
    _engine: AsyncEngine
    _session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, url: str) -> None:
        parsed_url = parse.urlparse(url)
        if not parsed_url.scheme.startswith("sqlite"):
            raise ValueError(f"'{parsed_url.scheme}' URL Scheme Not Supported")

        self._engine = create_async_engine(url=url)
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    async def create_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseOrm.metadata.create_all)

    async def drop_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseOrm.metadata.drop_all)

    def session(self) -> AsyncSession:
        return self._session_factory()
