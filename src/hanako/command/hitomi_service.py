import abc

from kyrie.models import IDType

from hanako.domain import HitomiGallery, HitomiPage


class HitomiService(abc.ABC):
    @abc.abstractmethod
    async def fetch_gallery_ids(
        self, languae: str, offset: int, limit: int
    ) -> list[IDType]:
        ...

    @abc.abstractmethod
    async def fetch_gallery(self, gallery_id: IDType) -> HitomiGallery:
        ...

    @abc.abstractmethod
    async def download_page(self, gallery_id: IDType, page: HitomiPage) -> bytes:
        ...

    @abc.abstractmethod
    async def download_gallery(self, gallery: HitomiGallery) -> list[bytes]:
        ...
