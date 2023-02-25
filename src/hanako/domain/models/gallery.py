from kyrie.models import IDType, ValueObject


class GalleryArtist(ValueObject):
    name: str


class GalleryPage(ValueObject):
    filename: str
    hash: str
    hasavif: bool
    haswebp: bool


class GalleryTag(ValueObject):
    tag: str


class Gallery(ValueObject):
    id: IDType
    language: str
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
