import abc


class Reader(abc.ABC):
    @abc.abstractmethod
    async def read(self, file_path: str) -> bytes:
        ...


class Writer(abc.ABC):
    @abc.abstractmethod
    async def write(self, byte_file: bytes, file_path: str) -> None:
        ...


class Filesystem(Reader, Writer):
    ...
