import abc


class Exporter(abc.ABC):
    @abc.abstractmethod
    async def export(self, byte_file: bytes, file_path: str) -> None:
        ...
