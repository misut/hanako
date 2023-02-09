import pytest

from hanako.domain import Manga
from hanako.infrastructure import (
    SqliteDatabase,
    SqliteMangaRepository,
    SqliteMangaStorage,
)


@pytest.mark.asyncio
async def test_sqlite_manga_storage(db: SqliteDatabase) -> None:
    repo = SqliteMangaRepository(db.session)
    store = SqliteMangaStorage(db.session)

    expected = [
        Manga(id="test_1", title="test manga #1"),
        Manga(id="test_2", title="test manga #2"),
    ]
    await store.save_one(expected[0])
    result = (await repo.find_one(id=expected[0].id)).unwrap()
    assert expected[0].id == result.id
    assert expected[0].title == result.title

    await store.save(*expected)
    await repo.find(0, 0)
