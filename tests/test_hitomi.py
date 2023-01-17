import pytest

from hanako import hitomi


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_id,expected_title",
    [
        ("1927583", "Hanako Ecchi"),
        ("2280632", "Warui Ko Hanako | 나쁜 아이 하나코"),
        ("2418097", "Roshutsu Shoujo to Zange Ana | 노출소녀와 참회구멍"),
    ],
)
async def test_load_gallery(expected_id: str, expected_title: str) -> None:
    gallery = await hitomi.load_gallery(expected_id)
    assert gallery.id == expected_id
    assert gallery.title == expected_title

    url = await hitomi.generate_download_url(gallery.files[0])
    await hitomi.download_gallery(gallery)
    assert url is None
