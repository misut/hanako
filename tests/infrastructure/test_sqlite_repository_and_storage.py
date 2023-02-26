import pytest

from hanako import domain
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
        domain.Manga(
            id=f"test_{n}",
            language="korean",
            title=f"test manga #{n}",
            thumbnail=f"image#{n}",
            artists=[],
            pages=[],
            tags=[],
        )
        for n in range(2)
    ]
    await store.save_one(expected[0])
    result = await repo.find_one(id=expected[0].id)
    assert result
    assert expected[0].id == result.id
    assert expected[0].title == result.title
    assert expected[0].thumbnail == result.thumbnail

    await store.save(*expected)
    results = await repo.find(0, len(expected))
    assert len(results) == len(expected)
