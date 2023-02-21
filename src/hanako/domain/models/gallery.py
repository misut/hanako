from kyrie.models import IDType, ValueObject


class GalleryArtist(ValueObject):
    name: str


class GalleryPage(ValueObject):
    filename: str
    url: str


class GalleryTag(ValueObject):
    tag: str


class Gallery(ValueObject):
    id: IDType
    title: str
    thumbnail: str
    artists: list[GalleryArtist]
    pages: list[GalleryPage]
    tags: list[GalleryTag]


class GalleryPool(ValueObject):
    id_list: list[IDType]
    language: str
    offset: int
    limit: int
