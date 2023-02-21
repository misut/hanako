import pytest

from hanako.infrastructure import LocalFilesystem


@pytest.mark.asyncio
async def test_local_filesystem() -> None:
    lf = LocalFilesystem()
    with pytest.raises(ValueError):
        await lf.write(b"Hello, world!", "pyproject.toml")
