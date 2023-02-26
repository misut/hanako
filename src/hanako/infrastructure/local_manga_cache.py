import asyncio
import pathlib
from collections.abc import Sequence

from kyrie.monads import Err, Ok, Result

from hanako import domain
from hanako.command import MangaCache, ReadError, WriteError
from hanako.infrastructure.local_filesystem import LocalFilesystem


class LocalMangaCache(MangaCache):
    _cache_path: pathlib.Path
    _engine: LocalFilesystem

    def __init__(self, cache_dir: str, missing_ok: bool) -> None:
        path = pathlib.Path(cache_dir)
        if not path.exists():
            if not missing_ok:
                raise ValueError(f"Path '{cache_dir}' Not Exists")
            path.mkdir()
        if path.is_file():
            raise ValueError(f"Path '{cache_dir}' Not Directory But File")

        self._cache_path = path
        self._engine = LocalFilesystem()

    async def read(self, manga: domain.Manga) -> Result[list[bytes], ReadError]:
        if not manga.is_cached():
            return Err(ReadError(f"Manga '{manga.title}' Not Cached Before"))

        tasks = [
            asyncio.create_task(self._engine.read(page.cached_in))
            for page in manga.pages
            if page.cached_in
        ]
        return Ok([await task for task in tasks])

    async def write_one(
        self, manga: domain.Manga, page_file: bytes, page_number: int
    ) -> Result[str, WriteError]:
        manga_path = self._cache_path.joinpath(manga.id)
        if manga_path.is_file():
            return Err(WriteError(f"Path '{manga_path.name}' Not Directory But File"))
        manga_path.mkdir(exist_ok=True)
        page_path = manga_path.joinpath(manga.pages[page_number].filename)
        if page_path.exists():
            return Err(WriteError(f"Path '{page_path.name}' Already Exists"))

        await self._engine.write(page_file, str(page_path))
        return Ok(str(page_path))

    async def write(
        self, manga: domain.Manga, page_files: Sequence[bytes]
    ) -> Result[list[str], WriteError]:
        manga_path = self._cache_path.joinpath(manga.id)
        if manga_path.exists():
            raise ValueError(f"Path '{manga_path}' Already Exists")
        manga_path.mkdir(exist_ok=False)

        page_paths: list[str] = []
        async with asyncio.TaskGroup() as tg:
            for page, page_file in zip(manga.pages, page_files):
                page_path = str(manga_path.joinpath(page.filename))
                page_paths.append(page_path)
                tg.create_task(self._engine.write(page_file, page_path))
        return Ok(page_paths)
