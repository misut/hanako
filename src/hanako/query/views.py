from kyrie.models import IDType, View


class MangaView(View):
    __entity_type__ = "Manga"

    id: IDType
    title: str
    thumbnail: str


class PoolView(View):
    __entity_type__ = "Pool"

    id: IDType
    manga_ids: list[IDType]
