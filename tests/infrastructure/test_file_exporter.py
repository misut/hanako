import pytest

from hanako.infrastructure import FileExporter


@pytest.mark.asyncio
async def test_file_exporter() -> None:
    fe = FileExporter()
    with pytest.raises(ValueError):
        await fe.export(b"Hello, world!", "pyproject.toml")
