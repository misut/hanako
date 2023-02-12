import pytest

from hanako.domain import Manga
from hanako.infrastructure import (
    SqliteDatabase,
    SqliteMangaRepository,
    SqliteMangaStorage,
)


@pytest.mark.asyncio
async def test_manga(db: SqliteDatabase) -> None:
    repo = SqliteMangaRepository(db.session)
    store = SqliteMangaStorage(db.session)

    expected = [
        Manga(id="test_1", title="test manga #1", thumbnail_url="test.url#1", pages=[]),
        Manga(id="test_2", title="test manga #2", thumbnail_url="test.url#2", pages=[]),
    ]
    await store.save_one(expected[0])
    result = await repo.find_one(id=expected[0].id)
    assert result
    assert expected[0].id == result.id
    assert expected[0].title == result.title
    assert expected[0].thumbnail_url == result.thumbnail_url

    await store.save(*expected)
    await repo.find(0, 0)
