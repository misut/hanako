import pytest
import pytest_asyncio

from hanako import domain
from hanako.infrastructure import HitomiMangaDownloader, HttpClient


@pytest_asyncio.fixture(name="hitomi")
async def initialize_hitomi_manga_downloader() -> HitomiMangaDownloader:
    http_client = HttpClient()
    return HitomiMangaDownloader(client_factory=http_client.client)


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.parametrize("manga", [])
async def test_download_manga(
    hitomi: HitomiMangaDownloader, manga: domain.Manga
) -> None:
    downloaded = await hitomi.download_manga(manga)
    assert downloaded.is_ok()

    page_files = downloaded.unwrap()
    assert len(page_files) == len(manga.pages)
