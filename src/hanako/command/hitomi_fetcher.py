import abc

from kyrie.models import IDType

from hanako.domain import HitomiGallery, HitomiPage


class HitomiFetcher(abc.ABC):
    @abc.abstractmethod
    async def fetch_gallery_ids(
        self, language: str, offset: int, limit: int
    ) -> list[IDType]:
        ...

    @abc.abstractmethod
    async def fetch_gallery(self, gallery_id: IDType) -> HitomiGallery:
        ...

    @abc.abstractmethod
    async def fetch_thumbnail(self, gallery: HitomiGallery) -> str:
        ...

    @abc.abstractmethod
    def generate_page_url(self, page: HitomiPage) -> str:
        ...
