import pathlib

import aiofiles
from kyrie.interfaces import Exporter


class FileExporter(Exporter):
    async def export(self, byte_file: bytes, file_path: str) -> None:
        path = pathlib.Path(file_path)
        if path.exists():
            raise ValueError(f"'{path.name}' Already Exists")

        path.touch(exist_ok=False)
        async with aiofiles.open(file_path, "wb") as fout:
            await fout.write(byte_file)
