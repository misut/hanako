import pathlib

import aiofiles
from kyrie.interfaces import Filesystem


class LocalFilesystem(Filesystem):
    async def read(self, file_path: str) -> bytes:
        path = pathlib.Path(file_path)
        if not path.exists():
            raise ValueError(f"'{path.name}' Not Exists")
        if path.is_dir():
            raise ValueError(f"'{path.name}' Not File But Directory")

        async with aiofiles.open(file_path, "rb") as fin:
            return await fin.read()

    async def write(self, byte_file: bytes, file_path: str) -> None:
        path = pathlib.Path(file_path)
        if path.exists():
            raise ValueError(f"'{path.name}' Already Exists")

        path.touch(exist_ok=False)
        async with aiofiles.open(file_path, "wb") as fout:
            await fout.write(byte_file)
