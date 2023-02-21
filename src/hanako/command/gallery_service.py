import abc

from kyrie.models import IDType
from kyrie.monads import Result

from hanako import domain
from hanako.command.exceptions import FetchError


class GalleryService(abc.ABC):
    @abc.abstractmethod
    async def fetch_galleries(
        self, *gallery_ids: IDType
    ) -> list[Result[domain.Gallery, FetchError]]:
        ...

    @abc.abstractmethod
    async def fetch_pool(
        self, language: str, offset: int, limit: int
    ) -> Result[domain.GalleryPool, FetchError]:
        ...
