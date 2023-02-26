from datetime import datetime

import pytest
import pytest_asyncio

from hanako import domain
from hanako.infrastructure import GGjs, HitomiMangaDownloader, HttpClient


manga_1 = domain.Manga(
    id="1927583",
    language="japanese",
    title="Hanako Ecchi",
    artists=[domain.MangaArtist(name="hozmi")],
    thumbnail="",
    pages=[
        domain.MangaPage(
            filename="1.jpg",
            hash="14e69a847940b63b7a60b967b21e0c3098572ec22d71567bffeaeb6c21d06aac",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="2.jpg",
            hash="fb8210cac57dda18c903085a1105a2294adf79cf59459ad4f38e609630a43d2e",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="3.jpg",
            hash="def463e938366aee47ff377ad45a016df2e0b867e8be23954404d6715230d3de",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="4.jpg",
            hash="3b5287dde78682b5901636004b4ac4d8a59f0dd4fe9890450a5adb0a85796c92",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="5.jpg",
            hash="6a9eba216a82ebff03f39d47614d83dca8a46f36cff552a228fbb726f4541d64",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="6.jpg",
            hash="42dd2d1e55bc40be0333f5f450e43ac59806624861137dc5f5f1a00faab5af8a",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="7.jpg",
            hash="7db10319c196cfd317891c334029f601c38a0eeb23b43feb1006c16afb1c5b63",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
        domain.MangaPage(
            filename="8.jpg",
            hash="4058fe0c11fe16274a2fcb2313ae78bffe41132c5ad8ecebf1c3ffc355bbd333",
            hasavif=True,
            haswebp=True,
            cached_in=None,
        ),
    ],
    tags=[
        domain.MangaTag(tag="schoolgirl uniform"),
        domain.MangaTag(tag="sole female"),
        domain.MangaTag(tag="very long hair"),
        domain.MangaTag(tag="dark skin"),
        domain.MangaTag(tag="first person perspective"),
        domain.MangaTag(tag="sole male"),
        domain.MangaTag(tag="teacher"),
        domain.MangaTag(tag="mosaic censorship"),
        domain.MangaTag(tag="variant set"),
    ],
    fetched_at=datetime(2023, 2, 26, 14, 27, 51, 701792),
    updated_at=datetime(2023, 2, 26, 14, 27, 51, 701792),
)


@pytest_asyncio.fixture(name="hitomi")
async def initialize_hitomi_manga_downloader() -> HitomiMangaDownloader:
    http_client = HttpClient()
    ggjs = await GGjs.create()
    return HitomiMangaDownloader(client_factory=http_client.client, gg=ggjs)


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.parametrize(
    ["manga", "page_number"],
    [(manga_1, 0)],
)
async def test_download_page(
    hitomi: HitomiMangaDownloader, manga: domain.Manga, page_number: int
) -> None:
    downloaded = await hitomi.download_page(manga, page_number)
    assert downloaded.is_ok()


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.parametrize("manga", [manga_1])
async def test_download_manga(
    hitomi: HitomiMangaDownloader, manga: domain.Manga
) -> None:
    downloaded = await hitomi.download_manga(manga)
    assert downloaded.is_ok()

    page_files = downloaded.unwrap()
    assert len(page_files) == len(manga.pages)
