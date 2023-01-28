from hanako.models import Command


class FetchMangaIDs(Command):
    offset: int
    limit: int
