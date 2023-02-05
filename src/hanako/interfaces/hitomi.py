import abc

from hanako.domain import HitomiGallery, HitomiPage
from hanako.models import IDType


class HitomiService(abc.ABC):
    @abc.abstractmethod
    async def fetch_ids(self, offset: int, limit: int) -> list[IDType]:
        ...

    @abc.abstractmethod
    async def fetch_gallery(self, gallery_id: IDType) -> HitomiGallery:
        ...

    @abc.abstractmethod
    async def download_page(self, gallery_id: IDType, page: HitomiPage) -> None:
        ...

    @abc.abstractmethod
    async def download_gallery(self, gallery: HitomiGallery) -> None:
        ...
