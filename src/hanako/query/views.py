from kyrie.models import IDType, View


class MangaPageView(View):
    ...


class MangaView(View):
    __entity_type__ = "Manga"

    id: IDType
    title: str
