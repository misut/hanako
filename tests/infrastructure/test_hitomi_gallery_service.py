from collections.abc import Sequence

import pytest
import pytest_asyncio

from hanako import domain
from hanako.infrastructure import HitomiGalleryService, HttpClient


@pytest_asyncio.fixture(name="hitomi")
async def initialize_hitomi_gallery_service() -> HitomiGalleryService:
    http_client = HttpClient()
    return HitomiGalleryService(http_client.client)


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.parametrize(
    ["language", "offset", "limit"],
    [
        ("all", 0, 10),
        ("english", 0, 10),
        ("korean", 0, 10),
    ],
)
async def test_fetch_galleries_ids(
    hitomi: HitomiGalleryService, language: str, offset: int, limit: int
) -> None:
    fetched = await hitomi.fetch_pool(language, offset, limit)
    fetched.unwrap()


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.parametrize(
    ["expected_ids", "expected_titles"],
    [
        (
            ("1927583", "2280632", "2418097"),
            (
                "Hanako Ecchi",
                "Warui Ko Hanako | 나쁜 아이 하나코",
                "Roshutsu Shoujo to Zange Ana | 노출소녀와 참회구멍",
            ),
        ),
    ],
)
async def test_fetch_galleries(
    hitomi: HitomiGalleryService,
    expected_ids: Sequence[str],
    expected_titles: Sequence[str],
) -> None:
    fetched = await hitomi.fetch_galleries(*expected_ids)
    assert fetched

    for idx, gallery in enumerate(fetched.unwrap()):
        assert gallery.id == expected_ids[idx]
        assert gallery.title == expected_titles[idx]
