import asyncio
import pathlib
from collections.abc import Sequence

from hanako import domain
from hanako.command import MangaCache
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

    async def read(self, manga: domain.Manga) -> list[bytes]:
        tasks = [
            asyncio.create_task(self._engine.read(page.cached_in))
            for page in manga.pages
            if page.cached_in
        ]
        return [await task for task in tasks]

    async def write(self, manga: domain.Manga, page_files: Sequence[bytes]) -> str:
        manga_path = self._cache_path.joinpath(manga.id)
        if manga_path.exists():
            raise ValueError(f"Path '{manga_path}' Already Exists")

        manga_path.mkdir()
        async with asyncio.TaskGroup() as tg:
            for page, page_file in zip(manga.pages, page_files):
                tg.create_task(
                    self._engine.write(
                        page_file, str(manga_path.joinpath(page.filename))
                    )
                )
        return str(manga_path)
