from collections.abc import Sequence

import pytest
from kyrie.context import Provider
from kyrie.models import IDType
from kyrie.monads import Result, Option, Ok, Err

from hanako import domain
from hanako.command import (
    HanakoCommandContext,
    GalleryService,
    FetchError,
    MangaCache,
    MangaDownloader,
    DownloadError,
    MangaStorage,
    PoolStorage,
)


class GalleryServiceMock(GalleryService):
    _data: dict[IDType, domain.Gallery] = {
        "manga_1": domain.Gallery(
            id="manga_1",
            title="test_manga_#1",
            thumbnail="",
            artists=[],
            pages=[],
            tags=[],
        )
    }

    async def fetch_galleries(
        self, *gallery_ids: IDType
    ) -> list[Result[domain.Gallery, FetchError]]:
        results: list[Result[domain.Gallery, FetchError]] = []
        for gallery_id in gallery_ids:
            result: Result[domain.Gallery, FetchError]
            if gallery_id in self._data:
                result = Ok(self._data[gallery_id])
            else:
                result = Err(FetchError(f"No Gallery With ID {gallery_id}"))
            results.append(result)
        return results

    async def fetch_pool(
        self, language: str, offset: int, limit: int
    ) -> Result[domain.GalleryPool, FetchError]:
        fetched = list(self._data.keys())
        if len(fetched) < offset + limit - 1:
            return Err(FetchError("Invalid offset and limit"))
        return Ok(
            domain.GalleryPool(
                id_list=fetched[offset : offset + limit],
                language=language,
                offset=offset,
                limit=limit,
            )
        )


class MangaCacheMock(MangaCache):
    async def read(self, manga: domain.Manga) -> list[bytes]:
        raise NotImplementedError()

    async def write(self, manga: domain.Manga, page_files: Sequence[bytes]) -> str:
        raise NotImplementedError()


class MangaDownloaderMock(MangaDownloader):
    async def download_page(
        self, manga: domain.Manga, page_number: int
    ) -> Result[bytes, DownloadError]:
        raise NotImplementedError()

    async def download_manga(
        self, manga: domain.Manga
    ) -> Result[list[bytes], DownloadError]:
        raise NotImplementedError()


class MangaStorageMock(MangaStorage):
    _data: dict[IDType, domain.Manga] = {}

    async def find_one(self, **filters: object) -> Option[domain.Manga]:
        raise NotImplementedError()

    async def save(self, *entities: domain.Manga) -> None:
        for entity in entities:
            await self.save_one(entity)

    async def save_one(self, entity: domain.Manga) -> None:
        self._data[entity.id] = entity


class PoolStorageMock(PoolStorage):
    async def find_one(self, **filters: object) -> Option[domain.Pool]:
        raise NotImplementedError()

    async def save(self, *entities: domain.Pool) -> None:
        raise NotImplementedError()

    async def save_one(self, entity: domain.Pool) -> None:
        raise NotImplementedError()


@pytest.fixture(name="command_context")
def initialize_command_context() -> HanakoCommandContext:
    return HanakoCommandContext(
        gallery_service=Provider(GalleryServiceMock),
        manga_cache=Provider(MangaCacheMock),
        manga_downloader=Provider(MangaDownloaderMock),
        manga_storage=Provider(MangaStorageMock),
        pool_storage=Provider(PoolStorageMock),
    )
