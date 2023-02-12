import pytest
import pytest_asyncio

from hanako.infrastructure import GGjs, HttpClient, HttpHitomiService


@pytest_asyncio.fixture(name="hitomi")
async def get_hitomi() -> HttpHitomiService:
    http_client = HttpClient()
    ggjs = await GGjs.create()
    return HttpHitomiService(http_client.client, ggjs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "language,offset,limit",
    [
        ("all", 0, 10),
        ("english", 0, 10),
        ("korean", 0, 10),
    ],
)
async def test_fetch_gallery_ids(
    hitomi: HttpHitomiService, language: str, offset: int, limit: int
) -> None:
    await hitomi.fetch_gallery_ids(language, offset, limit)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_id,expected_title",
    [
        ("1927583", "Hanako Ecchi"),
        ("2280632", "Warui Ko Hanako | 나쁜 아이 하나코"),
        ("2418097", "Roshutsu Shoujo to Zange Ana | 노출소녀와 참회구멍"),
    ],
)
async def test_fetch_gallery(
    hitomi: HttpHitomiService, expected_id: str, expected_title: str
) -> None:
    gallery = await hitomi.fetch_gallery(expected_id)
    assert gallery.id == expected_id
    assert gallery.title == expected_title

    # await hitomi.download_page(gallery.id, gallery.pages[0])
