from hanako.models import AggregateRoot, IDType


class Manga(AggregateRoot):
    id: IDType
    title: str
