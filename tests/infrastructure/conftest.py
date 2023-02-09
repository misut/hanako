import pytest_asyncio

from hanako.infrastructure import SqliteDatabase


@pytest_asyncio.fixture(name="db")
async def initialize_db() -> SqliteDatabase:
    db = SqliteDatabase(url="sqlite+aiosqlite:///:memory:?check_same_thread=False")
    await db.drop_all()
    await db.create_all()
    return db
