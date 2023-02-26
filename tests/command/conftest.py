from collections.abc import Sequence

import pytest
from kyrie.context import Provider
from kyrie.models import IDType
from kyrie.monads import Err, Null, Ok, Option, Result, Some

from hanako import domain
from hanako.command import (
    DownloadError,
    FetchError,
    GalleryService,
    HanakoCommandContext,
    MangaCache,
    MangaDownloader,
    MangaStorage,
    PoolEntryStorage,
    ReadError,
    WriteError,
)


class GalleryServiceMock(GalleryService):
    _data: dict[IDType, domain.Gallery] = {
        "manga_1": domain.Gallery(
            id="manga_1",
            language="korean",
            title="test_manga_#1",
            thumbnail="",
            artists=[],
            pages=[],
            tags=[],
        ),
    }

    async def fetch_galleries(
        self, *gallery_ids: IDType
    ) -> Result[list[domain.Gallery], FetchError]:
        galleries: list[domain.Gallery] = []
        for gallery_id in gallery_ids:
            if gallery_id not in self._data:
                continue
            galleries.append(self._data[gallery_id])
        return Ok(galleries)

    async def fetch_pool(
        self, language: str, offset: int, limit: int
    ) -> Result[domain.GalleryPool, FetchError]:
        if language == "fetch_failed":
            return Err(FetchError(f"Fetch Error For Unit Test"))
        fetched = [
            manga_id
            for manga_id, gallery in self._data.items()
            if gallery.language == language
        ]
        if limit == 0:
            return Ok(
                domain.GalleryPool(
                    id_list=fetched[offset:],
                    language=language,
                    offset=offset,
                    limit=limit,
                )
            )
        return Ok(
            domain.GalleryPool(
                id_list=fetched[offset : offset + limit],
                language=language,
                offset=offset,
                limit=limit,
            )
        )


class MangaCacheMock(MangaCache):
    async def read(self, manga: domain.Manga) -> Result[list[bytes], ReadError]:
        raise NotImplementedError()

    async def write_one(
        self, manga: domain.Manga, page_file: bytes, page_number: int
    ) -> Result[str, WriteError]:
        if manga.id == "cache_failed":
            return Err(WriteError(f"Write Error For Unit Test"))
        return Ok(f"saved_{manga.pages[page_number].filename}")

    async def write(
        self, manga: domain.Manga, page_files: Sequence[bytes]
    ) -> Result[list[str], WriteError]:
        if manga.id == "cache_failed":
            return Err(WriteError(f"Write Error For Unit Test"))
        return Ok([f"saved_{page.filename}" for page in manga.pages])


class MangaDownloaderMock(MangaDownloader):
    async def download_page(
        self, manga: domain.Manga, page_number: int
    ) -> Result[bytes, DownloadError]:
        if manga.id == "download_failed":
            return Err(DownloadError(f"Download Error For Unit Test"))
        return Ok(b"")

    async def download_manga(
        self, manga: domain.Manga
    ) -> Result[list[bytes], DownloadError]:
        if manga.id == "download_failed":
            return Err(DownloadError(f"Download Error For Unit Test"))
        return Ok([b"" for _ in manga.pages])


class MangaStorageMock(MangaStorage):
    _data: dict[IDType, domain.Manga] = {
        "manga_2": domain.Manga(
            id="manga_2",
            language="korean",
            title="test_manga_#2",
            thumbnail="",
            artists=[],
            pages=[
                domain.MangaPage(
                    filename="1.jpg",
                    hash="",
                    hasavif=False,
                    haswebp=False,
                )
            ],
            tags=[],
        ),
        "manga_3": domain.Manga(
            id="manga_3",
            language="korean",
            title="test_manga_#3",
            thumbnail="",
            artists=[],
            pages=[
                domain.MangaPage(
                    filename="1.jpg",
                    hash="",
                    hasavif=False,
                    haswebp=False,
                ),
                domain.MangaPage(
                    filename="2.jpg",
                    hash="",
                    hasavif=False,
                    haswebp=False,
                ),
            ],
            tags=[],
        ),
        "cache_failed": domain.Manga(
            id="cache_failed",
            language="korean",
            title="",
            thumbnail="",
            artists=[],
            pages=[
                domain.MangaPage(
                    filename="1.jpg",
                    hash="",
                    hasavif=False,
                    haswebp=False,
                )
            ],
            tags=[],
        ),
        "download_failed": domain.Manga(
            id="download_failed",
            language="korean",
            title="",
            thumbnail="",
            artists=[],
            pages=[
                domain.MangaPage(
                    filename="1.jpg",
                    hash="",
                    hasavif=False,
                    haswebp=False,
                )
            ],
            tags=[],
        ),
    }

    async def find_one(self, **filters: object) -> Option[domain.Manga]:
        for manga in self._data.values():
            for key, val in filters.items():
                if getattr(manga, key) == val:
                    return Some(manga)
        return Null

    async def save(self, *entities: domain.Manga) -> None:
        for entity in entities:
            await self.save_one(entity)

    async def save_one(self, entity: domain.Manga) -> None:
        self._data[entity.id] = entity


class PoolEntryStorageMock(PoolEntryStorage):
    _data: dict[IDType, domain.PoolEntry] = {
        "manga_1": domain.PoolEntry(
            manga_id="manga_1",
            language="korean",
        ),
        "manga_2": domain.PoolEntry(
            manga_id="manga_2",
            language="korean",
        ),
        "manga_3": domain.PoolEntry(
            manga_id="manga_3",
            language="korean",
        ),
    }

    async def find_one(self, **filters: object) -> Option[domain.PoolEntry]:
        for pool_entry in self._data.values():
            for key, val in filters.items():
                if getattr(pool_entry, key) == val:
                    return Some(pool_entry)
        return Null

    async def save(self, *entities: domain.PoolEntry) -> None:
        for entity in entities:
            self._data[entity.manga_id] = entity

    async def save_one(self, entity: domain.PoolEntry) -> None:
        self._data[entity.manga_id] = entity


@pytest.fixture(name="command_context")
def initialize_command_context() -> HanakoCommandContext:
    return HanakoCommandContext(
        gallery_service=Provider(GalleryServiceMock),
        manga_cache=Provider(MangaCacheMock),
        manga_downloader=Provider(MangaDownloaderMock),
        manga_storage=Provider(MangaStorageMock),
        pool_entry_storage=Provider(PoolEntryStorageMock),
    )
